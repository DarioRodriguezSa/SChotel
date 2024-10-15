from django.contrib import admin

from .models import categoria, estado

@admin.register(categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    search_fields = ('nombre',)

@admin.register(estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    search_fields = ('nombre',)


