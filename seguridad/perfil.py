from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from sistemafinal.funciones import addUserData, render_to_pdf
import datetime
from seguridad.models import Empleado, Sucursal, Empresa
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction, IntegrityError

@login_required(login_url='/seguridad/login/')
def perfil(request):
    data ={
        'titulo':'Perfil-FULL AUTO MILAGRO',
        'model': 'Usuario',
        'ruta':'/seguridad/perfil/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():

                    if action == 'edit':
                        empleado = Empleado.objects.get(user=request.user)
                        us=User.objects.get(pk=int(empleado.user.id))
                        if (request.POST['chancontr']) == '1':
                            us.set_password(request.POST['password'])
                        print(request.POST['username'])
                        us.username, us.email,us.first_name = request.POST['username'],request.POST['email'],request.POST['first_name']
                        us.last_name ,us.username= request.POST['last_name'], request.POST['username']
                        us.save()

                        empleado.user,empleado.direcion,empleado.cedula   =us,request.POST['direcion'], request.POST['cedula']
                        empleado.celular = request.POST['celular']
                        if 'image' in request.FILES:
                            empleado.image = request.FILES['image']
                        empleado.save()

            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/seguridad/perfil/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            data['action'] = request.GET['action']
            if not (request.GET['action'] == 'add' or request.GET['action'] == 'verificar'):
                data['id'] = request.GET['id']
                data['empleado'] = Empleado.objects.get(user=request.user)
            return render(request, 'seguridad/perfil_form.html', data)
        else:
            # Viaja por get

            data['empleado'] = Empleado.objects.get(user=request.user)
            return render(request, 'seguridad/perfil.html', data)
