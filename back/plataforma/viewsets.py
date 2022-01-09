from rest_framework import viewsets
from .models import Chofer, Bus, Asiento, Pasajero, Trayecto, Viaje
from .serializers import ChoferSerializer, BusSerializer, AsientoSerializer, PasajeroSerializer, TrayectoSerializer, ViajeSerializer

class ChoferViewSet(viewsets.ModelViewSet):
  queryset = Chofer.objects.all()
  serializer_class = ChoferSerializer


class ChoferViewSet(viewsets.ModelViewSet):
  queryset = Chofer.objects.all()
  serializer_class = ChoferSerializer


class BusViewSet(viewsets.ModelViewSet):
  queryset = Bus.objects.all()
  serializer_class = BusSerializer


class AsientoViewSet(viewsets.ModelViewSet):
  queryset = Asiento.objects.all()
  serializer_class = AsientoSerializer


class PasajeroViewSet(viewsets.ModelViewSet):
  queryset = Pasajero.objects.all()
  serializer_class = PasajeroSerializer


class TrayectoViewSet(viewsets.ModelViewSet):
  queryset = Trayecto.objects.all()
  serializer_class = TrayectoSerializer


class ViajeViewSet(viewsets.ModelViewSet):
  queryset = Viaje.objects.all()
  serializer_class = ViajeSerializer