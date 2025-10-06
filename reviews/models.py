from django.db import models
from common.models import TimeStampedModel
from accounts.models import User
from properties.models import Property
class Review(TimeStampedModel):
    property=models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating=models.PositiveSmallIntegerField()
    content=models.TextField(blank=True)
    class Meta: unique_together=('property','user')
