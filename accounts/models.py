from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import TimeStampedModel
class User(AbstractUser, TimeStampedModel):
    phone=models.CharField(max_length=32, blank=True)
    avatar=models.URLField(blank=True)
    language=models.CharField(max_length=8, default='ko')
    currency=models.CharField(max_length=3, default='KRW')
