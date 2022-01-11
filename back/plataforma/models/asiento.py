from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Asiento(models.Model):
  bus = models.BigIntegerField()
  numero = models.IntegerField(
    validators = [
      MaxValueValidator(11),
      MinValueValidator(1)
      ]
  )
  ocupado = models.BooleanField(default=False)

  class Meta:
    unique_together = [['numero', 'bus']]
    db_table = "asiento"
