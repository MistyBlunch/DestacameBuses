from django.urls import path
from django.urls import path
from . import queries

urlpatterns = [
  path('choferbus/', queries.ChoferBusApiView.as_view()),
  path('choferesavailables/', queries.ChoferesAvailablesApiView.as_view()),
]
