from django.urls import path
from . import views


app_name = "registro"
urlpatterns = [
    path('registro/', views.agregar_registro, name="agregar_registro"),
    path('listar_registro/', views.listar_r, name="lista_registro"),
    path('delete/<str:registro_id>/', views.eliminar_registro, name='eliminar_registro'),
    path('update/<int:registro_id>/', views.actualizar_registro, name='registro_actuali'),

]
