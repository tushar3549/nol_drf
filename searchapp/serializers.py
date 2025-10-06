from rest_framework import serializers
from properties.serializers import PropertyCardSerializer
class HomeSectionSerializer(serializers.Serializer):
    title=serializers.CharField(); items=PropertyCardSerializer(many=True)
class SearchResultSerializer(serializers.Serializer):
    count=serializers.IntegerField(); items=PropertyCardSerializer(many=True)
class MapMarkerSerializer(serializers.Serializer):
    id=serializers.IntegerField(); lat=serializers.FloatField(); lng=serializers.FloatField(); label_price=serializers.CharField()
