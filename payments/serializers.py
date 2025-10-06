from rest_framework import serializers
from .models import Payment
class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta: model=Payment; fields=['id','booking','provider','currency','amount','client_secret','status']; read_only_fields=['client_secret','status']
