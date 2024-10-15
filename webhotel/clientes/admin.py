from django.contrib import admin
from .models import genero

@admin.register(genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    search_fields = ('nombre',)
