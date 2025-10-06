from django.urls import path
from .views import QuoteView, BookingCreateView, BookingDetailView, MyBookingsView
urlpatterns=[path('quote/', QuoteView.as_view()), path('', BookingCreateView.as_view()), path('<str:code>/', BookingDetailView.as_view()), path('mine/', MyBookingsView.as_view())]
