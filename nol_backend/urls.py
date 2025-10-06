from django.contrib import admin
from django.urls import path, include
urlpatterns=[path('admin/', admin.site.urls),path('api/<str:version>/', include([path('auth/', include('accounts.urls')),path('', include('searchapp.urls')),path('accommodations/', include('properties.urls')),path('bookings/', include('bookings.urls')),path('payments/', include('payments.urls')),path('reviews/', include('reviews.urls')),path('me/', include('accounts.me_urls')),]))]
