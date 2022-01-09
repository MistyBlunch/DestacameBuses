from .chofer import Chofer
from .bus import Bus
from .asiento import Asiento
from .pasajero import Pasajero
from .trayecto import Trayecto
from .viaje import Viaje
from django.contrib import admin

admin.site.register([Chofer, Bus, Asiento, Pasajero, Trayecto, Viaje])