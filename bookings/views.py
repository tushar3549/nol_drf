from datetime import timedelta
from decimal import Decimal
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from properties.models import RatePlan
from .models import Booking, Guest
from .serializers import BookingSerializer, QuoteSerializer

def _date_range(start, end):
    cur=start
    while cur<end:
        yield cur
        cur+=timedelta(days=1)
        
# class QuoteView(APIView):
#     permission_classes=[permissions.AllowAny]
#     def post(self, request, version):
#         s=QuoteSerializer(data=request.data); s.is_valid(raise_exception=True)
#         rp=RatePlan.objects.get(pk=s.validated_data['rate_plan_id'])
#         nights=list(_date_range(s.validated_data['check_in'], s.validated_data['check_out']))
#         nightly=[Decimal(rp.nightly_price) for _ in nights]
#         subtotal=sum(nightly, Decimal('0.00'))
#         taxes=(subtotal*Decimal('0.10')).quantize(Decimal('1.00'))
#         total=subtotal+taxes
#         code=f"BK-{get_random_string(8).upper()}"
#         return Response({'code':code,'currency':rp.currency,'nights':len(nights),'nightly_prices':[str(n) for n in nightly],'subtotal':str(subtotal),'taxes':str(taxes),'total':str(total)})
    
class QuoteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, version):
        s = QuoteSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        rp = RatePlan.objects.select_related('room_type__property').get(pk=s.validated_data['rate_plan_id'])
        # validate alignment
        if rp.room_type_id != s.validated_data['room_type_id'] or rp.room_type.property_id != s.validated_data['property_id']:
            return Response({"detail":"rate_plan does not belong to given room_type/property"}, status=400)

        nights = list(_date_range(s.validated_data['check_in'], s.validated_data['check_out']))
        nightly = [Decimal(rp.nightly_price) for _ in nights]
        subtotal = sum(nightly, Decimal('0.00'))
        taxes = (subtotal * Decimal('0.10')).quantize(Decimal('1.00'))
        total = subtotal + taxes

        return Response({
            'currency': rp.currency,
            'nights': len(nights),
            'nightly_prices': [str(n) for n in nightly],
            'subtotal': str(subtotal),
            'taxes': str(taxes),
            'total': str(total),
        })

    
# class BookingCreateView(APIView):
#     permission_classes=[permissions.AllowAny]
#     def post(self, request, version):
#         required=['code','property','room_type','rate_plan','check_in','check_out','subtotal','taxes','total']
#         for k in required:
#             if k not in request.data: return Response({'detail':f'{k} is required'}, status=400)
#         b=Booking.objects.create(code=request.data['code'], user=request.user if request.user.is_authenticated else None,
#             property_id=request.data['property'], room_type_id=request.data['room_type'], rate_plan_id=request.data['rate_plan'],
#             check_in=request.data['check_in'], check_out=request.data['check_out'], subtotal=request.data['subtotal'], taxes=request.data['taxes'], total=request.data['total'], currency=request.data.get('currency','KRW'))
#         for g in request.data.get('guests', []): Guest.objects.create(booking=b, **g)
#         return Response(BookingSerializer(b).data, status=status.HTTP_201_CREATED)
    

class BookingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, version):
        required = ['property','room_type','rate_plan','check_in','check_out']
        for k in required:
            if k not in request.data:
                return Response({'detail': f'{k} is required'}, status=400)

        # fetch & validate alignment
        rp = RatePlan.objects.select_related('room_type__property').get(pk=request.data['rate_plan'])
        if int(request.data['room_type']) != rp.room_type_id or int(request.data['property']) != rp.room_type.property_id:
            return Response({"detail":"rate_plan does not belong to given room_type/property"}, status=400)

        # dates
        check_in = request.data['check_in']
        check_out = request.data['check_out']
        from datetime import date
        ci = date.fromisoformat(check_in)
        co = date.fromisoformat(check_out)
        if ci >= co:
            return Response({"detail":"check_out must be after check_in"}, status=400)

        nights = (co - ci).days
        subtotal = Decimal(rp.nightly_price) * nights
        taxes = (subtotal * Decimal('0.10')).quantize(Decimal('1.00'))
        total = subtotal + taxes

        b = Booking.objects.create(
            user=request.user,
            property_id=request.data['property'],
            room_type_id=request.data['room_type'],
            rate_plan_id=request.data['rate_plan'],
            check_in=check_in, check_out=check_out,
            adults=int(request.data.get('adults', 2)),
            children=int(request.data.get('children', 0)),
            currency=request.data.get('currency', rp.currency),
            subtotal=subtotal, taxes=taxes, total=total,
        )

        for g in request.data.get('guests', []):
            Guest.objects.create(booking=b, **g)

        return Response(BookingSerializer(b).data, status=status.HTTP_201_CREATED)

    
class BookingDetailView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self, request, version, code):
        try: b=Booking.objects.get(code=code)
        except Booking.DoesNotExist: return Response({'detail':'Not found'}, status=404)
        return Response(BookingSerializer(b).data)
class MyBookingsView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, version):
        qs=Booking.objects.filter(user=request.user).order_by('-created_at')
        return Response(BookingSerializer(qs, many=True).data)
