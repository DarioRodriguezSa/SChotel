from django.shortcuts import render
from habitaciones.models import habitacion, estado
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url="auth/login/")
def home(request):
    query = request.GET.get('q', '')

    # Filtrar habitaciones que están ocupadas
    estado_ocupada = estado.objects.get(nombre='Ocupada')
    habitaciones_list = habitacion.objects.filter(
        estado=estado_ocupada
    )

    # Si hay una búsqueda, filtrar también por el número de habitación
    if query:
        habitaciones_list = habitaciones_list.filter(
            Q(nohabitacion__icontains=query)
        )

    context = {
        "active_icon": "habitaciones",
        "habitaciones": habitaciones_list,
        "query": query,
    }
    return render(request, "inicio/home.html", context)