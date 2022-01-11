from django.db import models
from .bus import Bus
from .pasajero import Pasajero
from .trayecto import Trayecto
from .asiento import Asiento

class Viaje(models.Model):
  trayecto = models.ForeignKey(Trayecto, on_delete=models.CASCADE)
  pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
  asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)

  class Meta:
    db_table = "viaje"
    unique_together = [['pasajero', 'trayecto'], ['pasajero', 'asiento']]