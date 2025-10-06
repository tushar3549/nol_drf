from django.urls import path
from .views import HomeView, SearchView, MapView
urlpatterns=[path('home/', HomeView.as_view()), path('search/', SearchView.as_view()), path('search/map/', MapView.as_view())]
