from django.db import models
from common.models import TimeStampedModel
class Country(TimeStampedModel):
    code=models.CharField(max_length=2, unique=True)
    name=models.CharField(max_length=64)
    def __str__(self): return self.name
class City(TimeStampedModel):
    country=models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name=models.CharField(max_length=64)
    lat=models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng=models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    class Meta: unique_together=('country','name')
    def __str__(self): return f"{self.name}, {self.country.code}"
