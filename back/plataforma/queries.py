from rest_framework.views import APIView
from django.core import serializers
from rest_framework.response import Response
from .models import Bus, Chofer, Viaje, Pasajero, Trayecto, Asiento
from .serializers import BusSerializer, ViajeSerializer, PasajeroSerializer, TrayectoSerializer, AsientoSerializer
import datetime
import json

class ChoferBusApiView(APIView):
  def get(self, request, format=None):
    buses = Bus.objects.all().prefetch_related('chofer')
    serializer = BusSerializer(buses, many=True)

    for i in serializer.data:
      i['chofer']['dni_nombre'] = i['chofer']['dni'] + ' - ' + i['chofer']['nombre'] + ' ' + i['chofer']['apellido']
    return Response(serializer.data, status=200)


class ChoferesAvailablesApiView(APIView):
  def get(self, request, format=None):
    exclude_choferes = []

    buses = Bus.objects.all()
    bus_serializer = BusSerializer(buses, many=True)

    for i in bus_serializer.data:
      exclude_choferes.append(i['chofer']['dni'])

    choferes = Chofer.objects.exclude(dni__in=exclude_choferes)

    json_serialized = serializers.serialize('json', choferes)
    return Response({'results': json.loads(json_serialized)})


class ViajesDetailsApiView(APIView):
  def get(self, request, format=None):
    viajes = Viaje.objects.all()
    serializer = ViajeSerializer(viajes, many=True)

    for i in serializer.data:
      i['pasajero']['dni_nombre'] = i['pasajero']['dni'] + ' - ' + i['pasajero']['nombre'] + ' ' + i['pasajero']['apellido']

      horario = datetime.datetime.strptime(i['trayecto']['horario'],'%Y-%m-%dT%H:%M:%SZ')
      new_format = '%Y-%m-%d %H:%M:%S'

      i['trayecto']['horario'] = horario.strftime(new_format)
      
    return Response(serializer.data, status=200)


class PasajerosDetailsApiView(APIView):
  def get(self, request, format=None):
    pasajeros = Pasajero.objects.all()
    serializer = PasajeroSerializer(pasajeros, many=True)

    for i in serializer.data:
      i['dni_nombre'] = i['dni'] + ' - ' + i['nombre'] + ' ' + i['apellido']
    return Response(serializer.data, status=200)


class TrayectosDetailsApiView(APIView):
  def get(self, request, format=None):
    trayectos = Trayecto.objects.distinct('lugar_partida','lugar_llegada')
    serializer = TrayectoSerializer(trayectos, many=True)

    for i in serializer.data:
      i['bus']['chofer']['dni_nombre'] = i['bus']['chofer']['dni'] + ' - ' + i['bus']['chofer']['nombre'] + ' ' + i['bus']['chofer']['apellido']
      i['partida_destino'] = i['lugar_partida'] + ' - ' + i['lugar_llegada']
    return Response(serializer.data, status=200)


class TrayectosPartidaLlegadaHorasApiView(APIView):
  def get(request, self, partida, llegada, format=None):
    data = []
    horario_id = {}
    queryset = Trayecto.objects.filter(lugar_partida__iexact=partida, lugar_llegada__iexact=llegada)

    for i in queryset:
      horario = datetime.datetime.strptime(str(i.horario),'%Y-%m-%d %H:%M:%S%z')
      new_format = '%Y-%m-%d %H:%M:%S'

      horario_id["id"] = i.id
      horario_id["horario"] = horario.strftime(new_format)

      data.append(horario_id)
      horario_id = {}

    data_json = json.dumps(data)
    return Response({'results': json.loads(data_json)})


class AsientosAvailablesApiView(APIView):
  def get(self, request, bus, format=None):
    queryset = Asiento.objects.filter(bus=bus, ocupado=False)
    serializer = AsientoSerializer(queryset, many=True)

    return Response(serializer.data, status=200)


class TrayectosPromediosPasajerosApiView(APIView):
  def get(request, self, format=None):
    data = []
    # queryset = Trayecto.objects.filter(lugar_partida__iexact=partida, lugar_llegada__iexact=llegada)
    queryset = Trayecto.objects.all()
    serializer = TrayectoSerializer(queryset, many=True)

    data_json = json.dumps(data)
    return Response(serializer.data, status=200)
