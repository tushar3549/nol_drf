from django.urls import path
from .views import PropertyReviewsView, CreateReviewView
urlpatterns=[path('<int:property_id>/', PropertyReviewsView.as_view()), path('<int:property_id>/create/', CreateReviewView.as_view())]
