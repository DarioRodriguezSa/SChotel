from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import  genero
from .models import cliente
from django.contrib.auth.decorators import login_required


@login_required(login_url="auth/login/")

def agregar_clientes(request):
    generos = genero.objects.all()

    if request.method == 'POST':
        data = request.POST
        nombre = data.get('nombre')
        apellidos = data.get('apellidos')
        dpi = data.get('di')  
        telefono = data.get('telefono')
        genero_id = data.get('genero')

        # Validaciones
        if not nombre or not apellidos or not dpi or not telefono or not genero_id:
            messages.error(request, 'Todos los campos son obligatorios.', extra_tags="danger")
            return redirect('clientes:agregar_clientes')

        # Verificar si el cliente ya existe
        if cliente.objects.filter(nombre=nombre, apellido=apellidos).exists():
            messages.error(request, 'Ya existe un Cliente con los mismos nombres y apellidos.', extra_tags="danger")
            return redirect('clientes:agregar_clientes')

        if cliente.objects.filter(dpi=dpi).exists():
            messages.error(request, 'Ya existe un Cliente con el mismo DPI.', extra_tags="danger")
            return redirect('clientes:agregar_clientes')

        # Crear nuevo cliente
        try:
            genero_obj = genero.objects.get(pk=genero_id)

            nuevo_cliente = cliente(
                nombre=nombre,
                apellido=apellidos,
                dpi=dpi,
                telefono=telefono,
                genero=genero_obj,
            )
            nuevo_cliente.save()

            messages.success(request, 'Cliente creado con éxito!', extra_tags="success")
            return redirect('clientes:lista_cliente')  # Redirigir a la lista de clientes

        except genero.DoesNotExist:
            messages.error(request, 'Género no válido.', extra_tags="danger")
            return redirect('clientes:agregar_clientes')
        except Exception as e:
            messages.error(request, 'Error al crear el Cliente: ' + str(e), extra_tags="danger")
            return redirect('clientes:agregar_clientes')

    return render(request, "miembro/miembros.html", {'generos': generos})


def listar_c(request):
    query = request.GET.get('q', '')
    clientes_list = cliente.objects.filter(
        Q(nombre__icontains=query) |
        Q(dpi__icontains=query) |
        Q(genero__nombre__icontains=query)
    )

    context = {
        "active_icon": "clientes",
        "clientes": clientes_list,  # Asegúrate de que este nombre coincida
        "query": query,
    }
    return render(request, "miembro/listar_miembros.html", context)



@login_required(login_url="auth/login/")
def eliminar_clientes(request, cliente_id):
    try:
        Cliente = cliente.objects.get(pk=cliente_id)
        Cliente.delete()
        messages.success(request, '¡Cliente eliminado!', extra_tags="success")
        return redirect('clientes:lista_cliente')  
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la eliminación!' + str(e), extra_tags="danger")
        return redirect('clientes:lista_cliente')
    



@login_required(login_url="auth/login/")
def actualizar_cliente(request, cliente_id):
    try:
        Cliente = cliente.objects.get(id=cliente_id)
        generos = genero.objects.all()
        context = {
            'generos': generos,
            'cliente': Cliente,  # Pasar el objeto Miembro
        }

        if request.method == 'POST':
            data = request.POST

            # Actualiza los campos del objeto Miembro
            Cliente.nombre = data['nombre']
            Cliente.apellido = data['apellidos']
            Cliente.genero = genero.objects.get(pk=data['genero'])
            nuevo_di = data['dpi']
            if nuevo_di != Cliente.dpi:
                # El DI ha cambiado, verificar si ya existe
                if cliente.objects.filter(dpi=nuevo_di).exclude(id=cliente_id).exists():
                    messages.error(request, 'Ya existe un Cliente con el mismo DPI.', extra_tags="danger")
                    return render(request, 'miembro/actualizar_miembros.html', context=context)
                
            if cliente.objects.filter(nombre=data['nombre'], apellido=data['apellidos']).exclude(id=cliente_id).exists():
                messages.error(request, 'Ya existe un Cliente con el mismo nombre y apellido.', extra_tags="danger")
                return render(request, 'miembro/actualizar_miembros.html', context=context)

            Cliente.dpi = nuevo_di
            Cliente.telefono = data['telefono']


            # Guarda los cambios
            Cliente.save()

            messages.success(request, 'Cliente actualizado con éxito!', extra_tags="success")

            return redirect('clientes:lista_cliente')  # Redirige a la lista de miembros después de actualizar

        return render(request, 'miembro/actualizar_miembros.html', context=context)

    except cliente.DoesNotExist:
        messages.error(request, 'El miembro no existe', extra_tags="danger")
        return redirect('clientes:lista_cliente')

    except Exception as e:
        messages.error(request, '¡Hubo un error durante la actualización: ' + str(e), extra_tags="danger")
        return render(request, 'miembro/actualizar_miembros.html', context=context)
