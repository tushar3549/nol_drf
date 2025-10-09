from decimal import Decimal
from django.db.models import Q, Min
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from properties.models import Property
from properties.serializers import PropertyCardSerializer

def _recommended_queryset():
    return Property.objects.all().order_by('-discount_percent', '-rating', '-review_count')

class HomeView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, version):
        banners = [{'image_url': 'https://picsum.photos/1200/400', 'title': 'Welcome to NOL', 'link': '#'}]
        recommended = _recommended_queryset()[:10]
        return Response({
            'navbar': {'logo': 'NOL', 'has_search': True},
            'banners': banners,
            'today_recommended': PropertyCardSerializer(recommended, many=True).data,
            'recent_searches': []
        })

class SearchView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, version):
        qs = Property.objects.all()

        q = request.query_params.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(address__icontains=q))

        city_id = request.query_params.get('city_id')
        if city_id:
            qs = qs.filter(city_id=city_id)

        # map viewport bounding box
        bbox = request.query_params.get('bbox')
        if bbox:
            try:
                lat1, lng1, lat2, lng2 = [float(x) for x in bbox.split(',')]
                qs = qs.filter(
                    lat__gte=min(lat1, lat2), lat__lte=max(lat1, lat2),
                    lng__gte=min(lng1, lng2), lng__lte=max(lng1, lng2)
                )
            except Exception:
                pass

        # filters (all from RatePlan fields)
        if request.query_params.get('breakfast') == '1':
            qs = qs.filter(room_types__rate_plans__breakfast_included=True)

        if request.query_params.get('free_cancellation') == '1':
            qs = qs.filter(room_types__rate_plans__free_cancellation=True)

        if request.query_params.get('free_wifi') == '1':
            qs = qs.filter(room_types__rate_plans__free_wifi=True)

        # price range → RatePlan.nightly_price
        pmin = request.query_params.get('price_min')
        pmax = request.query_params.get('price_max')
        if pmin:
            qs = qs.filter(room_types__rate_plans__nightly_price__gte=Decimal(pmin))
        if pmax:
            qs = qs.filter(room_types__rate_plans__nightly_price__lte=Decimal(pmax))

        # use min(rate_plans.nightly_price) for cards/sorting
        qs = qs.annotate(min_price=Min('room_types__rate_plans__nightly_price')).distinct()

        sort = request.query_params.get('sort', 'recommended')
        if sort == 'price_asc':
            qs = qs.order_by('min_price', 'id')
        elif sort == 'price_desc':
            qs = qs.order_by('-min_price', 'id')
        else:
            qs = qs.order_by('-discount_percent', '-rating', '-review_count')

        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * size
        end = start + size

        return Response({
            'count': qs.count(),
            'items': PropertyCardSerializer(qs[start:end], many=True).data
        })

class MapView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, version):
        bbox = request.query_params.get('bbox')
        if not bbox:
            return Response({'detail': 'bbox required'}, status=400)
        lat1, lng1, lat2, lng2 = [float(x) for x in bbox.split(',')]

        qs = (Property.objects
              .filter(lat__gte=min(lat1, lat2), lat__lte=max(lat1, lat2),
                      lng__gte=min(lng1, lng2), lng__lte=max(lng1, lng2))
              .annotate(min_price=Min('room_types__rate_plans__nightly_price'))
              .values('id', 'lat', 'lng', 'min_price')[:200])

        items = [{
            'id': r['id'],
            'lat': float(r['lat'] or 0),
            'lng': float(r['lng'] or 0),
            'label_price': str(r['min_price'] or 0),
        } for r in qs]
        return Response({'items': items})





























# from decimal import Decimal
# from django.db.models import Q
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions
# from properties.models import Property
# from properties.serializers import PropertyCardSerializer

# def _recommended_queryset():
#     return Property.objects.all().order_by('-discount_percent','-rating','-review_count')
# class HomeView(APIView):
#     permission_classes=[permissions.AllowAny]
#     def get(self, request, version):
#         banners=[{'image_url':'https://picsum.photos/1200/400','title':'Welcome to NOL','link':'#'}]
#         recommended=_recommended_queryset()[:10]
#         return Response({'navbar':{'logo':'NOL','has_search':True}, 'banners':banners, 'today_recommended':PropertyCardSerializer(recommended, many=True).data, 'recent_searches':[]})
# class SearchView(APIView):
#     permission_classes=[permissions.AllowAny]
#     def get(self, request, version):
#         qs=Property.objects.all()
#         q=request.query_params.get('q')
#         if q: qs=qs.filter(Q(name__icontains=q)|Q(address__icontains=q))
#         city_id=request.query_params.get('city_id')
#         if city_id: qs=qs.filter(city_id=city_id)
#         bbox=request.query_params.get('bbox')
#         if bbox:
#             try:
#                 lat1,lng1,lat2,lng2=[float(x) for x in bbox.split(',')]
#                 qs=qs.filter(lat__gte=min(lat1,lat2), lat__lte=max(lat1,lat2), lng__gte=min(lng1,lng2), lng__lte=max(lng1,lng2))
#             except Exception: pass
#         if request.query_params.get('breakfast')=='1': qs=qs.filter(room_types__rate_plans__breakfast_included=True)
#         if request.query_params.get('free_cancellation')=='1': qs=qs.filter(room_types__rate_plans__free_cancellation=True)
#         if request.query_params.get('free_wifi')=='1': qs=qs.filter(room_types__rate_plans__free_wifi=True)
#         pmin=request.query_params.get('price_min'); pmax=request.query_params.get('price_max')
#         if pmin: qs=qs.filter(base_price__gte=Decimal(pmin))
#         if pmax: qs=qs.filter(base_price__lte=Decimal(pmax))
#         qs=qs.distinct()
#         sort=request.query_params.get('sort','recommended')
#         if sort=='price_asc': qs=qs.order_by('base_price')
#         elif sort=='price_desc': qs=qs.order_by('-base_price')
#         else: qs=qs.order_by('-discount_percent','-rating','-review_count')
#         page=int(request.query_params.get('page',1)); size=int(request.query_params.get('page_size',20))
#         start=(page-1)*size; end=start+size
#         return Response({'count':qs.count(),'items':PropertyCardSerializer(qs[start:end], many=True).data})
# class MapView(APIView):
#     permission_classes=[permissions.AllowAny]
#     def get(self, request, version):
#         bbox=request.query_params.get('bbox')
#         if not bbox: return Response({'detail':'bbox required'}, status=400)
#         lat1,lng1,lat2,lng2=[float(x) for x in bbox.split(',')]
#         qs=Property.objects.filter(lat__gte=min(lat1,lat2), lat__lte=max(lat1,lat2), lng__gte=min(lng1,lng2), lng__lte=max(lng1,lng2))[:200]
#         items=[{'id':p.id,'lat':float(p.lat or 0),'lng':float(p.lng or 0),'label_price':str(p.base_price)} for p in qs]
#         return Response({'items':items})
