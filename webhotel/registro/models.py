from django.db import models
from clientes.models import cliente
from habitaciones.models import habitacion

 
class registrohabitaciones(models.Model):
    clienteregistro = models.ForeignKey(cliente, on_delete=models.CASCADE)
    habitacionregistro= models.ForeignKey(habitacion, on_delete=models.CASCADE)
    entrada = models.DateTimeField(max_length=50, verbose_name="Entrada")
    salida = models.DateTimeField(max_length=50, null=True, verbose_name="Salida")
    
    
    def __str__(self):
        return self.nombre
    
    class Meta:
       db_table ='registrohabitacion'
       verbose_name= 'registrohabitacion'
       verbose_name_plural= 'registrohabitaciones'
       ordering = ['-id']      




