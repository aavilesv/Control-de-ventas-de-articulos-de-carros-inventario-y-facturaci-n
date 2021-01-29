from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from seguridad.models import Empresa
from sistemafinal.funciones import addUserData, render_to_pdf
from django.db import transaction
from django.shortcuts import render, redirect
from inventario.models import Marca
@login_required(login_url='/seguridad/login/')
def marca(request):
    data ={
        'titulo':'Consulta de marca -FULL AUTO MILAGRO',
        'model': 'Marca',
        'ruta':'/inventario/marca/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        marca = Marca()
                        marca.nombre,marca.descripcion = request.POST['nombre'],request.POST['descripcion']

                        staa = True
                        if not 'status' in request.POST:
                            staa = False
                        marca.status = staa
                        marca.save()
                    if action == 'edit':
                        marca = Marca.objects.select_related().get(pk=request.POST['id'])
                        marca.nombre,marca.descripcion  = request.POST['nombre'],request.POST['descripcion']
                        staa = True
                        if not 'status' in request.POST:
                            staa = False
                        marca.status = staa
                        marca.save()
                    if action == 'elim':
                        id = request.POST['id']
                        marca=Marca.objects.get(pk=int(id))
                        marca.elim=False
                        marca.save()
            except Exception as ex:
                messages.error(request, 'Error, dato ya registrado')
            return redirect('/inventario/marca/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'edit' or action == 'elim':
                data['id'] = request.GET['id']
                data['marca']=Marca.objects.get(pk=int(request.GET['id']))
            return render(request, 'inventario/marca_modal.html', data)
        elif 'imprime' in request.GET:

            marca = {

                'marca': Marca.objects.filter(status=True), 'empresa': Empresa.objects.first(),
                'model': 'Marca'
            }
            pdf = render_to_pdf('inventario/pdfmarca.html', marca)
            return HttpResponse(pdf, content_type='application/pdf')


        else:
            # Viaja por get
            data['marca']=Marca.objects.filter(elim=True)
            return render(request, 'inventario/marca.html', data)
