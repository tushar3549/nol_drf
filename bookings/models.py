from django.db import models
from common.models import TimeStampedModel
from accounts.models import User
from properties.models import Property, RoomType, RatePlan
import uuid

def gen_code():
    return "NOL" + uuid.uuid4().hex[:8].upper()


class Booking(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING='pending'; CONFIRMED='confirmed'; CANCELLED='cancelled'
    # code=models.CharField(max_length=24, unique=True)
    code = models.CharField(max_length=24, unique=True, default=gen_code, editable=False)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    property=models.ForeignKey(Property, on_delete=models.PROTECT, related_name='bookings')
    room_type=models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='bookings')
    rate_plan=models.ForeignKey(RatePlan, on_delete=models.PROTECT, related_name='bookings')
    check_in=models.DateField(); check_out=models.DateField()
    adults=models.PositiveSmallIntegerField(default=2); children=models.PositiveSmallIntegerField(default=0)
    currency=models.CharField(max_length=3, default='KRW')
    subtotal=models.DecimalField(max_digits=12, decimal_places=2)
    taxes=models.DecimalField(max_digits=12, decimal_places=2)
    total=models.DecimalField(max_digits=12, decimal_places=2)
    status=models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
class Guest(TimeStampedModel):
    booking=models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='guests')
    full_name=models.CharField(max_length=120); email=models.EmailField(blank=True); phone=models.CharField(max_length=32, blank=True)
