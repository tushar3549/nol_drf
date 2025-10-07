# from django.contrib import admin
# from django.urls import path, include
# urlpatterns=[path('admin/', admin.site.urls),path('api/<str:version>/', include([path('auth/', include('accounts.urls')),path('', include('searchapp.urls')),path('accommodations/', include('properties.urls')),path('bookings/', include('bookings.urls')),path('payments/', include('payments.urls')),path('reviews/', include('reviews.urls')),path('me/', include('accounts.me_urls')),]))]

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_v1_patterns = [
    path('auth/', include('accounts.urls')),
    path('', include('searchapp.urls')),
    path('accommodations/', include('properties.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('me/', include('accounts.me_urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="NOL API",
        default_version='v1',
        description="NOL accommodation booking API documentation",
        terms_of_service="https://nol.yanolja.com/",
        contact=openapi.Contact(email="support@nol.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[path('api/v1/', include(api_v1_patterns))], 
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/<str:version>/', include(api_v1_patterns)),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
