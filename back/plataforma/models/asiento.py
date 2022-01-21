from django.db import models
from .bus import Bus
from django.core.validators import MaxValueValidator, MinValueValidator

class Asiento(models.Model):
  bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
  numero = models.IntegerField(
    validators = [
      MaxValueValidator(11),
      MinValueValidator(1)
      ]
  )
  ocupado = models.BooleanField(default=False, null=False)

  class Meta:
    unique_together = [['numero', 'bus']]
    db_table = "asiento"
