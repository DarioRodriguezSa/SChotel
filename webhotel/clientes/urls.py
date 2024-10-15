from django.urls import path
from . import views


app_name = "clientes"
urlpatterns = [
    path('clientes/', views.agregar_clientes, name="agregar_clientes"),
    path('listar_clientes/', views.listar_c, name="lista_cliente"),
    path('delete/<str:cliente_id>/', views.eliminar_clientes, name='eliminar_cliente'),
    path('update/<int:cliente_id>/', views.actualizar_cliente, name='clientes_actuali'),

]
