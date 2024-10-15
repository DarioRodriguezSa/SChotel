from django.db import models

class categoria(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True, verbose_name="Nombre")


    def __str__(self):
        return self.nombre
    
    class Meta:
       db_table ='categoria'
       verbose_name= 'categoria'
       verbose_name_plural= 'categorias'
       ordering = ['id']       


class estado(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True, verbose_name="Nombre")


    def __str__(self):
        return self.nombre
    
    class Meta:
       db_table ='estado'
       verbose_name= 'estado'
       verbose_name_plural= 'estados'
       ordering = ['id']   




class habitacion(models.Model):
    nohabitacion = models.CharField(max_length=50, null=False,  verbose_name="Nohabitacion")
    categoria = models.ForeignKey(categoria, on_delete=models.CASCADE)
    estado = models.ForeignKey(estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    class Meta:
       db_table ='habitacion'
       verbose_name= 'habitacion'
       verbose_name_plural= 'habitaciones'
       ordering = ['-id']      
