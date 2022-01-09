from django.db import models
from .asiento import Asiento

class Pasajero(models.Model):
  dni = models.CharField(max_length=10, primary_key=True)
  asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
  nombre = models.CharField(max_length=30)
  apellido = models.CharField(max_length=30)

  class Meta:
    db_table = "pasajero"