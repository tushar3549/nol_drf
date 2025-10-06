from django.urls import path
from .views import CreatePaymentIntent, ConfirmPaymentMock
urlpatterns=[path('intent/', CreatePaymentIntent.as_view()), path('<int:pk>/confirm/', ConfirmPaymentMock.as_view())]
