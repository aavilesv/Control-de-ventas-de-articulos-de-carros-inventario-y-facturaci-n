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
def usuariote(request):
    data ={
        'titulo':'Consulta de usuarios -FULL AUTO MILAGRO',
        'model': 'Usuario',
        'ruta':'/seguridad/usuariote/',
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
                        us = User.objects.create_user(username=request.POST['username'],
                                                      first_name=request.POST['first_name'],
                                                      last_name=request.POST['last_name'],
                                                      email=request.POST['email'],
                                                      password=request.POST['password'],
                                                      is_active=True, is_staff=False, is_superuser=False)
                        us.groups.add(Group.objects.get(pk=int(request.POST['group'])))
                        empleado = Empleado()
                        empleado.direcion,empleado.cedula,empleado.celular =request.POST['direcion'], request.POST['cedula'], request.POST['celular']
                        empleado.sucursal, empleado.image,empleado.fecha =  Sucursal.objects.get(pk=int(request.POST['sucursal'])),request.FILES['image'],datetime.datetime.now()
                        empleado.user,empleado.group =us,Group.objects.get(pk=int(request.POST['group']))
                        empleado.save()

                    if action == 'edit':
                        empleado = Empleado.objects.get(pk=int(request.POST['id']))
                        us=User.objects.get(pk=int(empleado.user.id))
                        if (request.POST['chancontr']) == '1':
                            us.set_password(request.POST['password'])
                        us.username, us.email,us.first_name = request.POST['username'],request.POST['email'],request.POST['first_name']
                        us.last_name ,us.username= request.POST['last_name'], request.POST['username']
                        us.save()
                        if not empleado.user.is_superuser:
                            usuario = User.groups.through.objects.get(user=us)
                            usuario.group=Group.objects.get(pk=int(request.POST['group']))
                            usuario.save()
                            empleado.group=Group.objects.get(pk=int(request.POST['group']))
                        empleado.user,empleado.direcion,empleado.cedula   =us,request.POST['direcion'], request.POST['cedula']
                        empleado.celular = request.POST['celular']
                        empleado.sucursal  = Sucursal.objects.get(pk=int(request.POST['sucursal']))
                        if 'image' in request.FILES:
                            empleado.image = request.FILES['image']
                        empleado.save()

                    if action == 'elim':
                        empleado = Empleado.objects.get(pk=int(request.POST['id']))
                        User.objects.get(pk=empleado.user_id)
                        empleado.status = False
                        empleado.save()
                        u=User.objects.get(pk=empleado.user_id)
                        u.is_active=False
                        u.save()


            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/seguridad/usuariote/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            data['action'] = request.GET['action']
            if not (request.GET['action'] == 'add' or request.GET['action'] == 'verificar'):
                data['id'] = request.GET['id']
                data['empleado'] = Empleado.objects.get(pk=int(request.GET['id']))
            data['sucursal'],data['group'] = Sucursal.objects.filter(elim=True), Group.objects.all()
            if request.GET['action'] == 'verificar':
                try:
                    with transaction.atomic():
                        if 'username' in request.GET:
                            if not User.objects.get(username=request.GET['username']):
                                return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
                            else:
                                return HttpResponse(json.dumps({"resp": False, "mensaje": "contraseña no valida"}),
                                                    content_type="application/json")
                except IntegrityError as ex:
                    return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                        content_type="application/json")
            return render(request, 'seguridad/usuariotemodal.html', data)
        elif 'imprime' in request.GET:

            usuario = {

                'usuario':Empleado.objects.filter(status=True), 'empresa': Empresa.objects.first(),'model':'Usuario'
            }
            pdf = render_to_pdf('seguridad/pdfusuario.html', usuario)
            return HttpResponse(pdf, content_type='application/pdf')

        else:
            # Viaja por get
            data['empleado'] = Empleado.objects.filter(status=True)
            return render(request, 'seguridad/usuariote.html', data)
