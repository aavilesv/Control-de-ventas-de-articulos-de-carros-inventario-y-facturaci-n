from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sistemafinal.funciones import addUserData
from django.db import transaction
from django.shortcuts import render, redirect
from seguridad.models import  Empresa
@login_required(login_url='/seguridad/login/')
def empresa(request):
    data ={
        'titulo':'Consulta de empresa -FULL AUTO MILAGRO',
        'model': 'Empresa',
        'ruta':'/seguridad/empresa/',
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
                    if action == 'edit':
                        empr = Empresa.objects.select_related().get(pk=request.POST['id'])
                        empr.nombre,empr.ruc,empr.direcion  = request.POST['nombre'], request.POST['ruc'],request.POST['direcion']
                        empr.celular,empr.email  = request.POST['celular'],request.POST['email']
                        if 'image' in request.FILES:
                            empr.image = request.FILES['image']
                        empr.save()
            except Exception as ex:
                messages.error(request, 'Error, dato ya registrado')
            return redirect('/seguridad/empresa/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'edit':
                data['id'] = request.GET['id']
                data['empresa']=Empresa.objects.get(pk=int(request.GET['id']))
            return render(request, 'seguridad/empresa_form.html', data)
        else:
            #primera vez viaja por get : consulta todos los datos
            empresa= Empresa.objects.filter(status=True)
            data['empresa']=empresa
            return render(request, 'seguridad/empresa.html', data)
