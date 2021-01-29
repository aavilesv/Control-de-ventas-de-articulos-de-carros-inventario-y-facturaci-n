from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.functions import Upper
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from psycopg2._psycopg import IntegrityError


from inventario.models import Articulo, Marca
from seguridad.models import Sucursal
from sistemafinal.funciones import addUserData
from venta.models import Venta,Cliente,DetalleVenta
from compra.models import Compra, Proveedor

from django.db.models import FloatField

from django.db.models import Sum, Count, Max,Min,Avg


@login_required(login_url='/seguridad/login/')
def index(request):
    data = {
        'titulo': 'Empresa -FULL AUTO MILAGRO',
        'saludo': 'Bienvenido',
    }
    addUserData(request,data)
    data['venta']=Venta.objects.count()
    data['articulo']=Articulo.objects.filter(elim=True).count()
    data['compra']=Compra.objects.count()
    data['user']=User.objects.count()
    data['sucursal']=Sucursal.objects.filter(elim=True).count()
    data['marca']=Marca.objects.count()
    data['cliente']=Cliente.objects.filter(status=True).count()
    data['proveedor']=Proveedor.objects.filter(status=True).count()



    data['articulomax']=DetalleVenta.objects.values('articulo__nombre','cantidad').annotate(Sum('cantidad')).aggregate(Sum('total'))

    print(DetalleVenta.objects.values('articulo__nombre').order_by('articulo__nombre').annotate(Total=Sum('cantidad')))
    data['uh']=DetalleVenta.objects.values('articulo__nombre').order_by('articulo__nombre').annotate(Total=Sum('cantidad'))
    #print(Articulo.objects.values('det').order_by('nombre').annotate(Total=Sum('cantidad')))

    def current_date_format(month):
        months = (
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
        "Diciembre")
        month = months[month - 1]
        return month

    data['cliente'],data['compra'],data['venta']=Cliente.objects.exclude(nombre__icontains='Consumir Final').count(),Compra.objects.count(),Venta.objects.count()


    return render(request, 'main/index.html', data)





def login_session(request):
    data = {'titulo': 'Inicio de sesión -FULL AUTO MILAGRO'}
    success_url = reverse_lazy('index')
    if request.user.is_authenticated:
         return HttpResponseRedirect(success_url)
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST['usuario'],password=request.POST['password'])
        data['resp'] = False
        if user is not None:
            if user.is_active:
                login(request, user)
                data['resp'] = True
                data['user'] = user.username

            else:
                data['error'] = 'Usuario no esta Activo'
        else:
            data['error'] = 'El Usuario es Incorrecto'
        return JsonResponse(data)
    else:
        data['sistema'] = 'TALLER HERRERA'
        data['logo'] = "fas fa-spinner fa-spin"
        data['institucion'] = 'CAROLINA HERRERA'
        return render(request, 'seguridad/login.html', data)


def logout_user(request):
    logout(request)
    return redirect('/seguridad/login/')