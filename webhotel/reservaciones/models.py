from django.db import models
from clientes.models import cliente
from habitaciones.models import habitacion

 
class reservacion(models.Model):
    clientereservacion = models.ForeignKey(cliente, on_delete=models.CASCADE)
    habitacionreservacion= models.ForeignKey(habitacion, on_delete=models.CASCADE)
    fechareservacion = models.DateField(max_length=50, null=False, verbose_name="Fechareservacion")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
       db_table ='reservacion'
       verbose_name= 'reservacion'
       verbose_name_plural= 'reservaciones'
       ordering = ['-id']      


