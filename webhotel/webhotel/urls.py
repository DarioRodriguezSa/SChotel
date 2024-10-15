
from django.contrib import admin
from django.urls import path, include
from inicio import views as view_m

urlpatterns = [
     path('SCHotel/', admin.site.urls),
     path('inicios/', include('inicio.urls')),
     path('', include('auntenticacion.urls')),
     path('clientes/', include('clientes.urls')),
     path('habitaciones/', include('habitaciones.urls')),
     path('registro/', include('registro.urls')),
     path('rerservaciones/', include('reservaciones.urls')),
     #path('admin/', admin.site.urls),
     path('',view_m.home, name="home"),
]
