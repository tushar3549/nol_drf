from django.db import models
from common.models import TimeStampedModel
from locations.models import City
class Amenity(TimeStampedModel):
    name=models.CharField(max_length=64)
    icon=models.CharField(max_length=64, blank=True)
    def __str__(self): return self.name
class Property(TimeStampedModel):
    class Category(models.TextChoices):
        HOTEL='hotel','Hotel'; APARTHOTEL='aparthotel','Aparthotel'; RESORT='resort','Resort'
    name=models.CharField(max_length=120)
    category=models.CharField(max_length=20, choices=Category.choices, default=Category.HOTEL)
    city=models.ForeignKey(City, on_delete=models.PROTECT, related_name='properties')
    address=models.CharField(max_length=255, blank=True)
    lat=models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng=models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    rating=models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count=models.PositiveIntegerField(default=0)
    base_price=models.DecimalField(max_digits=12, decimal_places=2)
    discount_percent=models.PositiveIntegerField(default=0)
    amenities=models.ManyToManyField(Amenity, blank=True, related_name='properties')
    def __str__(self): return self.name
class PropertyPhoto(TimeStampedModel):
    property=models.ForeignKey(Property, on_delete=models.CASCADE, related_name='photos')
    image_url=models.URLField()
class RoomType(TimeStampedModel):
    property=models.ForeignKey(Property, on_delete=models.CASCADE, related_name='room_types')
    name=models.CharField(max_length=120)
    max_guests=models.PositiveIntegerField(default=2)
    beds=models.CharField(max_length=64, blank=True)
class RatePlan(TimeStampedModel):
    room_type=models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rate_plans')
    name=models.CharField(max_length=120, default='Standard')
    currency=models.CharField(max_length=3, default='KRW')
    nightly_price=models.DecimalField(max_digits=12, decimal_places=2)
    breakfast_included=models.BooleanField(default=False)
    free_cancellation=models.BooleanField(default=False)
    free_wifi=models.BooleanField(default=True)
class InventoryCalendar(TimeStampedModel):
    rate_plan=models.ForeignKey(RatePlan, on_delete=models.CASCADE, related_name='calendar')
    date=models.DateField()
    price=models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    available=models.PositiveIntegerField(default=5)
    class Meta: unique_together=('rate_plan','date')
