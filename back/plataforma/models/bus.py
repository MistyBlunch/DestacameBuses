from django.db import models
from .chofer import Chofer
from django.conf import settings

class Bus(models.Model):
  chofer = models.OneToOneField(
    Chofer,
    on_delete=models.CASCADE,
  )
  capacidad = models.IntegerField(default=10)

  class Meta:
    db_table = "bus"