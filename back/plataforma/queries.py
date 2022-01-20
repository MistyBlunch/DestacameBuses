from rest_framework.views import APIView
from django.core import serializers
from rest_framework.response import Response
from .models import Bus, Chofer
from .serializers import BusSerializer
import json

class ChoferBusApiView(APIView):
  def get(self, request, format=None):
    buses = Bus.objects.all().prefetch_related('chofer')
    serializer = BusSerializer(buses, many=True)

    for i in serializer.data:
      i['chofer']['dni_nombre'] = i['chofer']['dni'] + " - " + i['chofer']['nombre'] + " " + i['chofer']['apellido']
    return Response(serializer.data, status=200)


class ChoferesAvailablesApiView(APIView):
  def get(self, request, format=None):
    exclude_choferes = []

    buses = Bus.objects.all()
    bus_serializer = BusSerializer(buses, many=True)

    for i in bus_serializer.data:
      exclude_choferes.append(i['chofer']['dni'])

    choferes = Chofer.objects.exclude(dni__in=exclude_choferes)

    json_serialized = serializers.serialize("json", choferes)
    return Response({'results': json.loads(json_serialized)})


class TrayectosBusesApiView(APIView):
  def get(self, request, format=None):
    exclude_choferes = []

    buses = Bus.objects.all()
    bus_serializer = BusSerializer(buses, many=True)

    for i in bus_serializer.data:
      exclude_choferes.append(i['chofer']['dni'])

    choferes = Chofer.objects.exclude(dni__in=exclude_choferes)

    json_serialized = serializers.serialize("json", choferes)
    return Response({'results': json.loads(json_serialized)})
