from rest_framework import serializers
from .models import Property, PropertyPhoto, Amenity, RoomType, RatePlan
from decimal import Decimal
class AmenitySerializer(serializers.ModelSerializer):
    class Meta: model=Amenity; fields=['id','name','icon']
class PhotoSerializer(serializers.ModelSerializer):
    class Meta: model=PropertyPhoto; fields=['image_url']
class PropertyCardSerializer(serializers.ModelSerializer):
    photos=PhotoSerializer(many=True, read_only=True)
    min_price=serializers.SerializerMethodField()
    class Meta:
        model=Property
        fields=['id','name','category','rating','review_count','city_id','lat','lng','base_price','discount_percent','min_price','photos']
    def get_min_price(self,obj):
        from decimal import Decimal
        if obj.discount_percent:
            off=(Decimal(obj.base_price)*Decimal(obj.discount_percent)/Decimal('100')).quantize(Decimal('1.00'))
            return str(Decimal(obj.base_price)-off)
        return str(obj.base_price)
class RatePlanSerializer(serializers.ModelSerializer):
    class Meta: model=RatePlan; fields=['id','name','currency','nightly_price','breakfast_included','free_cancellation','free_wifi']
class RoomTypeSerializer(serializers.ModelSerializer):
    rate_plans=RatePlanSerializer(many=True, read_only=True)
    class Meta: model=RoomType; fields=['id','name','max_guests','beds','rate_plans']
class PropertyDetailSerializer(serializers.ModelSerializer):
    photos=PhotoSerializer(many=True, read_only=True)
    amenities=AmenitySerializer(many=True, read_only=True)
    room_types=RoomTypeSerializer(many=True, read_only=True)
    class Meta:
        model=Property
        fields=['id','name','category','address','city_id','lat','lng','rating','review_count','base_price','discount_percent','amenities','photos','room_types']
