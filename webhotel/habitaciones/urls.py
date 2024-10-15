from django.urls import path
from . import views


app_name = "habitaciones"
urlpatterns = [
    path('habitaciones/', views.agregar_habitaciones, name="agregar_habitaciones"),
    path('listar_habitaciones/', views.listar_h, name="lista_habitacion"),
    path('delete/<str:habitacion_id>/', views.eliminar_habitaciones, name='eliminar_habitacion'),
    path('update/<int:habitacion_id>/', views.actualizar_habitacion, name='habitaciones_actuali'),

]
