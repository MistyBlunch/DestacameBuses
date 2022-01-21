from django.db import models

class Chofer(models.Model):
  dni = models.CharField(max_length=10, null=False)
  nombre = models.CharField(max_length=80, null=False)
  apellido = models.CharField(max_length=80, null=False)

  class Meta:
    db_table = "chofer"