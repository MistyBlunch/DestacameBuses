from django.urls import path
from . import queries

urlpatterns = [
  path('chofer-bus/', queries.ChoferBusApiView.as_view()),
  path('choferes-availables/', queries.ChoferesAvailablesApiView.as_view()),
  path('viajes-details/', queries.ViajesDetailsApiView.as_view()),
  path('trayectos-details/', queries.TrayectosDetailsApiView.as_view()),
#  path('trayectos-promedios-pasajeros/', queries.TrayectosPromediosPasajerosApiView.as_view()),
  path('trayectos-partida-llegada-horas/<str:partida>&<str:llegada>/', queries.TrayectosPartidaLlegadaHorasApiView.as_view()),
  path('asientos-availables/<str:bus>/', queries.AsientosAvailablesApiView.as_view()),
]
