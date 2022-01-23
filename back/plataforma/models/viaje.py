from django.utils import timezone
from django.db import models
from .pasajero import Pasajero
from .trayecto import Trayecto
from .asiento import Asiento

class Viaje(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
  trayecto = models.ForeignKey(Trayecto, on_delete=models.CASCADE)
  asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)

  class Meta:
    db_table = "viaje"
    unique_together = [['pasajero', 'created']]