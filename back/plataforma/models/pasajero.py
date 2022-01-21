from django.db import models
from .asiento import Asiento

class Pasajero(models.Model):
  dni = models.CharField(max_length=10, null=False)
  nombre = models.CharField(max_length=30, null=False)
  apellido = models.CharField(max_length=30, null=False)

  class Meta:
    db_table = "pasajero"