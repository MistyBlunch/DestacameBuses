from django.db import models
from .chofer import Chofer
from .asiento import Asiento
from django.db.models.signals import post_save
from django.dispatch import receiver

class Bus(models.Model):
  chofer = models.OneToOneField(
    Chofer,
    on_delete=models.CASCADE,
  )
  capacidad = models.IntegerField(default=10)

  class Meta:
    db_table = "bus"


@receiver(post_save, sender=Bus)
def my_handler(sender, instance, **kwargs):
  for i in range(instance.capacidad):
    Asiento.objects.create(bus=instance.id, numero=i, ocupado=False)