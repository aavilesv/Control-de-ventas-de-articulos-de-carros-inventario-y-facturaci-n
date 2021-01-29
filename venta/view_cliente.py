from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from compra.models import Proveedor
from seguridad.models import Empresa
from sistemafinal.funciones import addUserData, render_to_pdf
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from venta.models import Cliente


@login_required(login_url='/seguridad/login/')
def cliente(request):
    data ={
        'titulo':'Consulta de Clientes -FULL AUTO MILAGRO',
        'model': 'Cliente',
        'ruta':'/venta/cliente/',
        'user': request.user.username,
    }
    addUserData(request, data)
    segurid=User.groups.through.objects.get(user_id=request.user.id)

    if segurid.group.name == 'Empleado':
        return redirect('/seguridad/login/')
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':

                        clien = Cliente()
                        clien.direccion,clien.email,clien.nombre = request.POST['direccion'],request.POST['email'], request.POST['nombre']
                        clien.ced_ruc, clien.telefono = request.POST['ced_ruc'],request.POST['telefono']
                        clien.save()

                    if action == 'edit':

                        clien = Cliente.objects.get(pk=int(request.POST['id']))
                        clien.direccion, clien.email, clien.nombre = request.POST['direccion'], request.POST['email'],request.POST['nombre']
                        clien.ced_ruc, clien.telefono = request.POST['ced_ruc'], request.POST['telefono']
                        clien.save()


                    if action == 'elim':
                        clien = Cliente.objects.get(pk=int(request.POST['id']))
                        clien.status = False
                        clien.save()

            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/venta/cliente/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            data['action'] = request.GET['action']
            if not request.GET['action'] == 'add':
                data['id'],data['client']  = request.GET['id'],Cliente.objects.get(pk=int(request.GET['id']))
            return render(request, 'venta/cliente_modal.html', data)
        elif 'imprime' in request.GET:

            cliente = {

                'cliente': Cliente.objects.filter(status=True).exclude(nombre__icontains='Consumidor Final'), 'empresa': Empresa.objects.first(),
                'model': 'Cliente'
            }
            pdf = render_to_pdf('venta/pdfcliente.html', cliente)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            # Viaja por get
            data['cliente'] = Cliente.objects.filter(status=True)
            return render(request, 'venta/cliente.html', data)
