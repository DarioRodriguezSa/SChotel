from django.urls import path
from . import views


app_name = "reservaciones"
urlpatterns = [
    path('reservacion/', views.agregar_reservacion, name="agregar_reservacion"),
    path('listar_reservacion/', views.listar_re, name="lista_reservacion"),
    path('delete/<str:reservacion_id>/', views.eliminar_reservacion, name='eliminar_reservacion'),
    path('update/<int:reservacion_id>/', views.actualizar_reservacion, name='reservacion_actuali'),

]
