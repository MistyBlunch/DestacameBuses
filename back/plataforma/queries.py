from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BusSerializer
from .models import Bus
import json

class ChoferBusApiView(APIView):
  def get(self, request, format=None):
    query = Bus.objects.select_related('chofer')
    json_serialized = serializers.serialize("json", query)
    print(query[0].chofer.nombre)
    print(query[1].chofer.nombre)

    return Response({'results': json.loads(json_serialized)})
