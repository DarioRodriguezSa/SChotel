from django.db import models


class genero(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True, verbose_name="Nombre")


    def __str__(self):
        return self.nombre
    
    class Meta:
       db_table ='genero'
       verbose_name= 'genero'
       verbose_name_plural= 'generos'
       ordering = ['id']       



class cliente(models.Model):
    nombre = models.CharField(max_length=50, null=False,  verbose_name="Nombre")
    apellido = models.CharField(max_length=50, null=False,  verbose_name="Apellido")
    dpi = models.CharField(max_length=50, null=False, verbose_name="Dpi")
    telefono = models.CharField(max_length=50, null=False,  verbose_name="Telefono")
    genero = models.ForeignKey(genero, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    class Meta:
       db_table ='cliente'
       verbose_name= 'cliente'
       verbose_name_plural= 'clientes'
       ordering = ['-id']      



