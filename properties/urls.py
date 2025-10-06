from django.urls import path
from .views import AccommodationDetailView, RoomsForDatesView
urlpatterns=[path('<int:pk>/', AccommodationDetailView.as_view()), path('<int:pk>/rooms/', RoomsForDatesView.as_view())]
