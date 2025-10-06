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
class QuoteView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request, version):
        s=QuoteSerializer(data=request.data); s.is_valid(raise_exception=True)
        rp=RatePlan.objects.get(pk=s.validated_data['rate_plan_id'])
        nights=list(_date_range(s.validated_data['check_in'], s.validated_data['check_out']))
        nightly=[Decimal(rp.nightly_price) for _ in nights]
        subtotal=sum(nightly, Decimal('0.00'))
        taxes=(subtotal*Decimal('0.10')).quantize(Decimal('1.00'))
        total=subtotal+taxes
        code=f"BK-{get_random_string(8).upper()}"
        return Response({'code':code,'currency':rp.currency,'nights':len(nights),'nightly_prices':[str(n) for n in nightly],'subtotal':str(subtotal),'taxes':str(taxes),'total':str(total)})
class BookingCreateView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request, version):
        required=['code','property','room_type','rate_plan','check_in','check_out','subtotal','taxes','total']
        for k in required:
            if k not in request.data: return Response({'detail':f'{k} is required'}, status=400)
        b=Booking.objects.create(code=request.data['code'], user=request.user if request.user.is_authenticated else None,
            property_id=request.data['property'], room_type_id=request.data['room_type'], rate_plan_id=request.data['rate_plan'],
            check_in=request.data['check_in'], check_out=request.data['check_out'], subtotal=request.data['subtotal'], taxes=request.data['taxes'], total=request.data['total'], currency=request.data.get('currency','KRW'))
        for g in request.data.get('guests', []): Guest.objects.create(booking=b, **g)
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
