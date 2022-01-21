from django.db import models
from .bus import Bus

class Trayecto(models.Model):
  bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
  horario = models.DateTimeField(auto_now=False, auto_now_add=False, null=False)
  lugar_partida = models.CharField(max_length=50, null=False)
  lugar_llegada = models.CharField(max_length=50, null=False)

  class Meta:
    db_table = "trayecto"
    unique_together = [['horario', 'bus']]