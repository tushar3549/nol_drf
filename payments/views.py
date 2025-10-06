import secrets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Payment
from .serializers import PaymentIntentSerializer
class CreatePaymentIntent(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request, version):
        s=PaymentIntentSerializer(data=request.data); s.is_valid(raise_exception=True)
        payment=Payment.objects.create(booking=s.validated_data.get('booking'), provider=s.validated_data.get('provider','mock'), currency=s.validated_data.get('currency','KRW'), amount=s.validated_data['amount'], client_secret=secrets.token_urlsafe(32))
        return Response(PaymentIntentSerializer(payment).data, status=status.HTTP_201_CREATED)
class ConfirmPaymentMock(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request, version, pk):
        try: p=Payment.objects.get(pk=pk)
        except Payment.DoesNotExist: return Response({'detail':'Not found'}, status=404)
        p.status=Payment.Status.SUCCEEDED; p.save(); return Response(PaymentIntentSerializer(p).data)
