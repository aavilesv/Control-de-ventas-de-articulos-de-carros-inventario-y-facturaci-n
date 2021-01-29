from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from compra.models import Proveedor
from seguridad.models import Empresa
from sistemafinal.funciones import addUserData, render_to_pdf
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

@login_required(login_url='/seguridad/login/')
def proveedor(request):
    data ={
        'titulo':'Consulta de proveedores -FULL AUTO MILAGRO',
        'model': 'Proveedor',
        'ruta':'/compra/proveedor/',
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

                        proveedo = Proveedor()
                        proveedo.direccion = request.POST['direccion']
                        proveedo.email = request.POST['email']
                        proveedo.nombre = request.POST['nombre']
                        proveedo.ced_ruc = request.POST['ced_ruc']
                        proveedo.telefono = request.POST['telefono']
                        proveedo.save()

                    if action == 'edit':

                        proveedo = Proveedor.objects.get(pk=int(request.POST['id']))
                        proveedo.direccion = request.POST['direccion']
                        proveedo.email = request.POST['email']
                        proveedo.nombre = request.POST['nombre']
                        proveedo.ced_ruc = request.POST['ced_ruc']
                        proveedo.telefono = request.POST['telefono']
                        proveedo.save()


                    if action == 'elim':
                        proveedo = Proveedor.objects.get(pk=int(request.POST['id']))
                        proveedo.status = False
                        proveedo.save()

            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/compra/proveedor/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'edit' or action == 'elim' or action == 'ver':
                id = request.GET['id']
                data['id'] = id
                proveedor = Proveedor.objects.get(pk=id)
                data['proveedo'] = proveedor


            return render(request, 'compra/proveedor_modal.html', data)
        elif 'imprime' in request.GET:

            proveedor = {

                'proveedor':Proveedor.objects.filter(status=True), 'empresa': Empresa.objects.first(),'model':'Proveedor'
            }
            pdf = render_to_pdf('compra/pdfproveedor.html', proveedor)
            return HttpResponse(pdf, content_type='application/pdf')


        else:
            # Viaja por get
            proveedor = Proveedor.objects.filter(status=True)
            data['proveedor'] = proveedor
            return render(request, 'compra/Proveedor.html', data)
