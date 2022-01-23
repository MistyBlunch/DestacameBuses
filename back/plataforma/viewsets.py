from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Chofer, Bus, Asiento, Pasajero, Trayecto, Viaje
from .serializers import ChoferSerializer, BusSerializer, AsientoSerializer, PasajeroSerializer, TrayectoSerializer, ViajeSerializer

class ChoferViewSet(viewsets.ModelViewSet):
  queryset = Chofer.objects.all()
  serializer_class = ChoferSerializer


class ChoferViewSet(viewsets.ModelViewSet):
  queryset = Chofer.objects.all()
  serializer_class = ChoferSerializer


class AsientoViewSet(viewsets.ModelViewSet):
  queryset = Asiento.objects.all()
  serializer_class = AsientoSerializer

class BusViewSet(viewsets.ModelViewSet):
  queryset = Bus.objects.all()
  serializer_class = BusSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    for i in range(int(request.data['capacidad'])):
      Asiento.objects.create(
        bus= Bus.objects.get(placa=request.data['placa']), 
        numero=i+1, 
        ocupado=False
      )

    return Response(serializer.data, status=status.HTTP_201_CREATED)


class PasajeroViewSet(viewsets.ModelViewSet):
  queryset = Pasajero.objects.all()
  serializer_class = PasajeroSerializer


class TrayectoViewSet(viewsets.ModelViewSet):
  queryset = Trayecto.objects.all()
  serializer_class = TrayectoSerializer


class ViajeViewSet(viewsets.ModelViewSet):
  queryset = Viaje.objects.all()
  serializer_class = ViajeSerializer
