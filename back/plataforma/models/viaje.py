from django.db import models
from .bus import Bus
from .pasajero import Pasajero
from .trayecto import Trayecto

class Viaje(models.Model):
  bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
  trayecto = models.ForeignKey(Trayecto, on_delete=models.CASCADE)
  pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)

  class Meta:
    db_table = "viaje"