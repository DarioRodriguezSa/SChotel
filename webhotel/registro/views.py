from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import registrohabitaciones
from clientes.models import cliente
from habitaciones.models import habitacion, estado
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import transaction

@login_required(login_url="auth/login/")
def agregar_registro(request):
    Clientes = cliente.objects.all()
    estado_ocupada = get_object_or_404(estado, nombre='Ocupada')
    
    # Obtener el estado "Desocupada" por su nombre
    estado_desocupada = get_object_or_404(estado, nombre='Desocupada')

    # Filtrar las habitaciones por estado "Desocupada"
    Habitaciones = habitacion.objects.filter(estado=estado_desocupada)

    if request.method == 'POST':
        cliente_id = request.POST.get('Clientes')
        habitacion_id = request.POST.get('Habitaciones')
        salida = request.POST.get('salida')  # Este puede ser opcional

        # Establecer fecha y entrada automáticamente
        entrada = timezone.now()  # Fecha y hora actuales

        # Validaciones
        if not all([cliente_id, habitacion_id]):
            messages.error(request, 'Los campos Cliente y Habitacion son obligatorios.', extra_tags="danger")
            return redirect('registro:agregar_registro')


        # Crear nuevo registro
        try:
            with transaction.atomic():  # Asegura que ambas operaciones se completen correctamente
                registro = registrohabitaciones(
                    clienteregistro_id=cliente_id,
                    habitacionregistro_id=habitacion_id,
                    entrada=entrada,
                    salida=salida if salida else None,  # Almacena 'None' si no hay salida
                )
                registro.save()

                # Cambiar el estado de la habitación a "Ocupada"
                habitacion_obj = get_object_or_404(habitacion, id=habitacion_id)
                habitacion_obj.estado = estado_ocupada
                habitacion_obj.save()

            messages.success(request, 'Registro de habitación creado con éxito y habitación marcada como ocupada!', extra_tags="success")
            return redirect('registro:lista_registro')

        except Exception as e:
            messages.error(request, 'Error al crear el registro: ' + str(e), extra_tags="danger")
            return redirect('registro:agregar_registro')

    return render(request, "registro/registro.html", {'Clientes': Clientes, 'Habitaciones': Habitaciones})



def listar_r(request):
    query = request.GET.get('q', '')
    registros_list = registrohabitaciones.objects.filter(
        Q(clienteregistro__nombre__icontains=query) |
        Q(habitacionregistro__nohabitacion__icontains=query) |
        Q(entrada__icontains=query) |
        Q(salida__icontains=query)    
    )

    context = {
        "active_icon": "registro_habitacion",
        "registros": registros_list,
        "query": query,
    }
    return render(request, "registro/listar_registro.html", context)




@login_required(login_url="auth/login/")
def eliminar_registro(request, registro_id):
    try:
        registro = registrohabitaciones.objects.get(pk=registro_id)
        habitacion_obj = registro.habitacionregistro  # Obtener la habitación asociada

        # Cambiar el estado de la habitación a "Desocupada"
        estado_desocupada = get_object_or_404(estado, nombre='Desocupada')
        habitacion_obj.estado = estado_desocupada
        habitacion_obj.save()

        # Eliminar el registro
        registro.delete()
        messages.success(request, '¡Registro de habitación eliminado y habitación marcada como desocupada!', extra_tags="success")

    except registrohabitaciones.DoesNotExist:
        messages.error(request, 'El registro no existe.', extra_tags="danger")
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la eliminación! ' + str(e), extra_tags="danger")

    return redirect('registro:lista_registro')





@login_required(login_url="auth/login/")
def actualizar_registro(request, registro_id):
    try:
        registro = registrohabitaciones.objects.get(id=registro_id)

        if request.method == 'POST':
            # Cambiar el estado de la habitación a "Desocupada"
            estado_desocupada = get_object_or_404(estado, nombre='Desocupada')
            habitacion_anterior = registro.habitacionregistro
            
            if habitacion_anterior:
                habitacion_anterior.estado = estado_desocupada
                habitacion_anterior.save()

            # Actualiza la salida a la fecha y hora actuales
            registro.salida = timezone.now()  # Establece la salida a la fecha y hora actuales
            registro.save()

            # Mostrar mensaje de éxito
            messages.success(request, 'Habitación desocupada y registro cerrado con éxito!', extra_tags="success")

            # Redirigir a la lista de registros
            return redirect('registro:lista_registro')

    except registrohabitaciones.DoesNotExist:
        messages.error(request, 'El registro no existe.', extra_tags="danger")
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la actualización: ' + str(e), extra_tags="danger")

    return redirect('registro:lista_registro')