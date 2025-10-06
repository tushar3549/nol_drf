from rest_framework import serializers
from .models import Booking, Guest
class GuestSerializer(serializers.ModelSerializer):
    class Meta: model=Guest; fields=['full_name','email','phone']
class BookingSerializer(serializers.ModelSerializer):
    guests=GuestSerializer(many=True, required=False)
    class Meta:
        model=Booking
        fields=['id','code','property','room_type','rate_plan','check_in','check_out','adults','children','currency','subtotal','taxes','total','status','guests']
        read_only_fields=['status']
class QuoteSerializer(serializers.Serializer):
    property_id=serializers.IntegerField(); room_type_id=serializers.IntegerField(); rate_plan_id=serializers.IntegerField()
    check_in=serializers.DateField(); check_out=serializers.DateField(); adults=serializers.IntegerField(default=2); children=serializers.IntegerField(default=0)
