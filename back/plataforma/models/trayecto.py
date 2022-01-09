from django.db import models

class Trayecto(models.Model):
  horario = models.DateTimeField(auto_now=False, auto_now_add=False)
  lugar_partida = models.CharField(max_length=50)
  lugar_llegada = models.CharField(max_length=50)

  
  class Meta:
    db_table = "trayecto"