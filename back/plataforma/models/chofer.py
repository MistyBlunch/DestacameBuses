from django.db import models

class Chofer(models.Model):
  dni = models.CharField(max_length=10, primary_key=True)
  nombre = models.CharField(max_length=80)
  apellido = models.CharField(max_length=80)

  class Meta:
    db_table = "chofer"