from django.db import models
from .chofer import Chofer
from django.db.models.signals import post_save
from django.dispatch import receiver

class Bus(models.Model):
  placa = models.CharField(max_length=10, null=False, unique=True)
  chofer = models.OneToOneField(
    Chofer,
    on_delete=models.CASCADE,
  )
  capacidad = models.IntegerField(default=10, null=False)

  class Meta:
    db_table = "bus"
