from django.db import models
from common.models import TimeStampedModel
from bookings.models import Booking
class Payment(TimeStampedModel):
    class Status(models.TextChoices):
        REQUIRES_CONFIRMATION='requires_confirmation'; SUCCEEDED='succeeded'; FAILED='failed'; CANCELED='canceled'
    booking=models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    provider=models.CharField(max_length=32, default='mock')
    currency=models.CharField(max_length=3, default='KRW')
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    client_secret=models.CharField(max_length=64, unique=True)
    status=models.CharField(max_length=32, choices=Status.choices, default=Status.REQUIRES_CONFIRMATION)
