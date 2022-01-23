from rest_framework import serializers
from plataforma.models import Chofer, Bus, Asiento, Pasajero, Trayecto, Viaje

class ChoferSerializer(serializers.ModelSerializer):
  class Meta:
    model = Chofer
    fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
  chofer_id = serializers.IntegerField(write_only=True)

  class Meta:
    model = Bus
    fields = ("id", "placa", "capacidad", "chofer", "chofer_id")
    depth = 1


class AsientoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Asiento
    fields = '__all__'


class PasajeroSerializer(serializers.ModelSerializer):
  class Meta:
    model = Pasajero
    fields = '__all__'


class TrayectoSerializer(serializers.ModelSerializer):
  bus_id = serializers.IntegerField(write_only=True)
  horario = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=["%Y-%m-%d %H:%M:%S"])

  class Meta:
    model = Trayecto
    fields = ("id", "horario", "lugar_partida", "lugar_llegada", "bus", "bus_id")
    depth = 2


class ViajeSerializer(serializers.ModelSerializer):
  trayecto_id = serializers.IntegerField(write_only=True)
  pasajero_id = serializers.IntegerField(write_only=True)
  asiento_id = serializers.IntegerField(write_only=True)
  created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=["%Y-%m-%d %H:%M:%S"])
  

  class Meta:
    model = Viaje
    fields = ("id", "created", "trayecto", "trayecto_id", "pasajero", "pasajero_id", "asiento", "asiento_id")
    depth = 2