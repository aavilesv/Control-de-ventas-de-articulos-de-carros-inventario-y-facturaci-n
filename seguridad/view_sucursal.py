from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

from sistemafinal.funciones import addUserData, render_to_pdf
from django.db import transaction
from django.shortcuts import render, redirect
from seguridad.models import Sucursal, Empresa
@login_required(login_url='/seguridad/login/')
def sucursal(request):
    data ={
        'titulo':'Consulta de Sucursales -FULL AUTO MILAGRO',
        'model': 'Sucursal',
        'ruta':'/seguridad/sucursal/',
        'user': request.user.username,
    }
    addUserData(request, data)
    segurid = User.groups.through.objects.get(user_id=request.user.id)
    if segurid.group.name == 'Empleado':
        return redirect('/seguridad/login/')
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        sucursa =Sucursal()
                        sucursa.razonsocial,sucursa.ruc,sucursa.direcion = request.POST['razonsocial'],request.POST['ruc'],request.POST['direcion']
                        sucursa.celular, sucursa.image,sucursa.email = request.POST['celular'],request.FILES['image'],request.POST['email']
                        if not 'status' in request.POST:
                            sucursa.status = False
                        sucursa.sucursal_id,sucursa.canton, sucursa.provincia  = int(Empresa.objects.count()),request.POST['canton'].capitalize(),request.POST['provincia'].capitalize()
                        sucursa.save()
                    if action == 'edit':
                            sucursa = Sucursal.objects.select_related().get(pk=request.POST['id'])
                            sucursa.razonsocial, sucursa.ruc, sucursa.direcion = request.POST['razonsocial'],request.POST['ruc'], request.POST['direcion']
                            sucursa.celular, sucursa.email = request.POST['celular'], request.POST['email']
                            if not 'status' in request.POST:
                                sucursa.status =False
                            if 'status' in request.POST:
                                sucursa.status = True
                            if 'image' in request.FILES:
                                sucursa.image = request.FILES['image']
                            sucursa.sucursal_id, sucursa.canton, sucursa.provincia = int(Empresa.objects.count()),request.POST['canton'].capitalize(),request.POST['provincia'].capitalize()
                            sucursa.save()
                    if action == 'elim':
                        id = request.POST['id']

                        sucursa=Sucursal.objects.get(pk=int(id))
                        sucursa.elim=False
                        sucursa.save()

            except Exception as ex:
                messages.error(request, str(ex)+'Error, dato ya registrado')
            return redirect('/seguridad/sucursal/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'edit' or action == 'elim' or action == 'ver':

                data['id'] = request.GET['id']
                data['sucursal']=Sucursal.objects.get(pk=int(request.GET['id']))

            return render(request, 'seguridad/sucrusal_modal.html', data)
        elif 'imprime' in request.GET:

            sucursales = {

                'sucursal':Sucursal.objects.filter(elim=True), 'empresa': Empresa.objects.first(),'model':'Sucursal'
            }
            pdf = render_to_pdf('seguridad/pdfsucursal.html', sucursales)
            return HttpResponse(pdf, content_type='application/pdf')

        else:
            # La primera vez viaje por get sin criterio: consulta todos los datos
            data['sucursal']=Sucursal.objects.filter(elim=True)
        return render(request, 'seguridad/sucursal.html', data)
