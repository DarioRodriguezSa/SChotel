from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import  categoria, estado
from .models import habitacion
from django.contrib.auth.decorators import login_required


@login_required(login_url="auth/login/")

def agregar_habitaciones(request):
    categorias = categoria.objects.all()
    estados = estado.objects.all()

    if request.method == 'POST':
        data = request.POST
        nohabitacion = data.get('nohabitacion')
        estado_id = data.get('estado')
        categoria_id = data.get('categoria')

        # Validaciones


        # Verificar si el cliente ya existe
        if habitacion.objects.filter(nohabitacion=nohabitacion).exists():
            messages.error(request, 'Ya existe la habitacion.', extra_tags="danger")
            return redirect('habitaciones:agregar_habitaciones')



        # Crear nuevo cliente
        try:
            categoria_obj = categoria.objects.get(pk=categoria_id)
            estado_obj = estado.objects.get(pk=estado_id)

            nuevo_cliente = habitacion(
                nohabitacion=nohabitacion,
                estado=estado_obj,
                categoria=categoria_obj,
            )
            nuevo_cliente.save()

            messages.success(request, 'Miembro creado con éxito!', extra_tags="success")
            return redirect('habitaciones:lista_habitacion')  # Redirigir a la lista de clientes

        except categoria.DoesNotExist:
            messages.error(request, 'Género no válido.', extra_tags="danger")
            return redirect('habitaciones:agregar_habitaciones')
        except estado.DoesNotExist:
            messages.error(request, 'Género no válido.', extra_tags="danger")
            return redirect('habitaciones:agregar_habitaciones')
        except Exception as e:
            messages.error(request, 'Error al crear el miembro: ' + str(e), extra_tags="danger")
            return redirect('habitaciones:agregar_habitaciones')

    return render(request, "habitacion/habitaciones.html", {'categorias': categorias, 'estados': estados})


def listar_h(request):
    query = request.GET.get('q', '')
    habitaciones_list = habitacion.objects.filter(
        Q(nohabitacion__icontains=query) |
        Q(estado__nombre__icontains=query) |
        Q(categoria__nombre__icontains=query)
    )

    context = {
        "active_icon": "habitaciones",
        "habitaciones": habitaciones_list,  # Asegúrate de que este nombre coincida
        "query": query,
    }
    return render(request, "habitacion/listar_habitaciones.html", context)



@login_required(login_url="auth/login/")
def eliminar_habitaciones(request, habitacion_id):
    try:
        Habitacion = habitacion.objects.get(pk=habitacion_id)
        Habitacion.delete()
        messages.success(request, '¡Habitacion eliminada!', extra_tags="success")
        return redirect('habitaciones:lista_habitacion')  
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la eliminación!' + str(e), extra_tags="danger")
        return redirect('habitaciones:lista_habitacion')
    



@login_required(login_url="auth/login/")
def actualizar_habitacion(request, habitacion_id):
    try:
        habitacion_instance = habitacion.objects.get(id=habitacion_id)
        categorias = categoria.objects.all()
        estados = estado.objects.all()
        context = {
            'estados': estados,
            'categorias': categorias,
            'habitacion': habitacion_instance,
        }

        if request.method == 'POST':
            data = request.POST

            # Actualiza los campos del objeto Habitacion
            habitacion_instance.nohabitacion = data['nohabitacion']
            habitacion_instance.estado = estado.objects.get(pk=data['estado'])
            habitacion_instance.categoria = categoria.objects.get(pk=data['categoria'])
        
            # Verifica si existe otra habitación con el mismo nohabitacion
            if habitacion.objects.filter(nohabitacion=data['nohabitacion']).exclude(id=habitacion_id).exists():
                messages.error(request, 'Ya existe una habitación con el mismo número.', extra_tags="danger")
                return render(request, 'habitacion/actualizar_habitaciones.html', context=context)

            # Guarda los cambios
            habitacion_instance.save()

            messages.success(request, 'Habitación actualizada con éxito!', extra_tags="success")
            return redirect('habitaciones:lista_habitacion')

        return render(request, 'habitacion/actualizar_habitaciones.html', context=context)

    except habitacion.DoesNotExist:
        messages.error(request, 'La habitación no existe', extra_tags="danger")
        return redirect('habitaciones:lista_habitacion')

    except Exception as e:
        messages.error(request, '¡Hubo un error durante la actualización: ' + str(e), extra_tags="danger")
        return render(request, 'habitacion/actualizar_habitaciones.html', context=context)