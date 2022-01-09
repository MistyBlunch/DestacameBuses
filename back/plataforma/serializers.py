from rest_framework import serializers
from plataforma.models import Chofer, Bus, Asiento, Pasajero, Trayecto, Viaje

class ChoferSerializer(serializers.ModelSerializer):
  class Meta:
    model = Chofer
    fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
  class Meta:
    model = Bus
    fields = '__all__'


class AsientoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Asiento
    fields = '__all__'


class PasajeroSerializer(serializers.ModelSerializer):
  class Meta:
    model = Pasajero
    fields = '__all__'


class TrayectoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Trayecto
    fields = '__all__'


class ViajeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Viaje
    fields = '__all__'