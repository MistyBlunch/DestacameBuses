from rest_framework import routers
from plataforma.viewsets import ChoferViewSet, BusViewSet, AsientoViewSet, PasajeroViewSet, TrayectoViewSet, ViajeViewSet

router = routers.DefaultRouter()
router.register(r'chofer', ChoferViewSet)
router.register(r'bus', BusViewSet)
router.register(r'asiento', AsientoViewSet)
router.register(r'pasajero', PasajeroViewSet)
router.register(r'trayecto', TrayectoViewSet)
router.register(r'viaje', ViajeViewSet)