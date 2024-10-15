from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import reservacion
from clientes.models import cliente
from habitaciones.models import habitacion, estado
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import transaction

@login_required(login_url="auth/login/")
def agregar_reservacion(request):
    Clientes = cliente.objects.all()
    estado_ocupada = get_object_or_404(estado, nombre='Ocupada')
    
    # Obtener el estado "Desocupada" por su nombre
    estado_desocupada = get_object_or_404(estado, nombre='Desocupada')

    # Filtrar las habitaciones por estado "Desocupada"
    Habitaciones = habitacion.objects.filter(estado=estado_desocupada)

    if request.method == 'POST':
        cliente_id = request.POST.get('Clientes')
        habitacion_id = request.POST.get('Habitaciones')
        fechareservacion = request.POST.get('fechareservacion')  # Este puede ser opcional

        # Establecer fecha y entrada automáticamente
         # Fecha y hora actuales

        # Validaciones
        if not all([cliente_id, habitacion_id]):
            messages.error(request, 'Los campos Cliente y Habitacion son obligatorios.', extra_tags="danger")
            return redirect('reservaciones:agregar_reservacion')


        # Crear nuevo registro
        try:
            with transaction.atomic():  # Asegura que ambas operaciones se completen correctamente
                registro = reservacion(
                    clientereservacion_id=cliente_id,
                    habitacionreservacion_id=habitacion_id,
                    fechareservacion=fechareservacion,
     
                )
                registro.save()

                # Cambiar el estado de la habitación a "Ocupada"
                habitacion_obj = get_object_or_404(habitacion, id=habitacion_id)
                habitacion_obj.estado = estado_ocupada
                habitacion_obj.save()

            messages.success(request, 'Reservacion de habitación creado con éxito y habitación marcada como ocupada!', extra_tags="success")
            return redirect('reservaciones:lista_reservacion')

        except Exception as e:
            messages.error(request, 'Error al crear el registro: ' + str(e), extra_tags="danger")
            return redirect('reservaciones:agregar_reservacion')

    return render(request, "reservacion/reservacion.html", {'Clientes': Clientes, 'Habitaciones': Habitaciones})



def listar_re(request):
    query = request.GET.get('q', '')
    reservacion_list = reservacion.objects.filter(
        Q(clientereservacion__nombre__icontains=query) |
        Q(habitacionreservacion__nohabitacion__icontains=query) |
        Q(fechareservacion__icontains=query)    
    )

    context = {
        "active_icon": "reservacion_habitacion",
        "reservaciones": reservacion_list,  # Cambiar a 'reservaciones'
        "query": query,
    }
    return render(request, "reservacion/listar_reservacion.html", context)




@login_required(login_url="auth/login/")
def eliminar_reservacion(request, reservacion_id):
    try:
        registro = reservacion.objects.get(pk=reservacion_id)
        habitacion_obj = registro.habitacionreservacion  # Obtener la habitación asociada

        # Cambiar el estado de la habitación a "Desocupada"
        estado_desocupada = get_object_or_404(estado, nombre='Desocupada')
        habitacion_obj.estado = estado_desocupada
        habitacion_obj.save()

        # Eliminar el registro
        registro.delete()
        messages.success(request, '¡Reservacion de habitación eliminado y habitación marcada como desocupada!', extra_tags="success")

    except reservacion.DoesNotExist:
        messages.error(request, 'El registro no existe.', extra_tags="danger")
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la eliminación! ' + str(e), extra_tags="danger")

    return redirect('reservaciones:lista_reservacion')





@login_required(login_url="auth/login/")
def actualizar_reservacion(request, reservacion_id):
    try:
        registro = reservacion.objects.get(id=reservacion_id)

        if request.method == 'POST':
            # Cambiar el estado de la habitación a "Desocupada"
            estado_desocupada = get_object_or_404(estado, nombre='Desocupada')
            habitacion_anterior = registro.habitacionreservacion
            
            if habitacion_anterior:
                habitacion_anterior.estado = estado_desocupada
                habitacion_anterior.save()

         

         
            messages.success(request, 'Habitación desocupada y registro cerrado con éxito!', extra_tags="success")

            # Redirigir a la lista de registros
            return redirect('reservaciones:lista_reservacion')

    except reservacion.DoesNotExist:
        messages.error(request, 'El registro no existe.', extra_tags="danger")
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la actualización: ' + str(e), extra_tags="danger")

    return redirect('reservaciones:lista_reservacion')