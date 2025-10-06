from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Property, RoomType
from .serializers import PropertyDetailSerializer, RoomTypeSerializer
class AccommodationDetailView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self, request, version, pk):
        prop=Property.objects.prefetch_related('photos','amenities','room_types__rate_plans').get(pk=pk)
        return Response(PropertyDetailSerializer(prop).data)
class RoomsForDatesView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self, request, version, pk):
        if not request.query_params.get('check_in') or not request.query_params.get('check_out'):
            return Response({'detail':'check_in & check_out required (YYYY-MM-DD)'}, status=400)
        room_types=RoomType.objects.filter(property_id=pk).prefetch_related('rate_plans')
        return Response(RoomTypeSerializer(room_types, many=True).data)
