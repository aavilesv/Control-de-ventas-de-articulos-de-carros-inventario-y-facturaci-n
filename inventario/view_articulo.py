from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from seguridad.models import Sucursal, Empresa
from sistemafinal.funciones import addUserData, render_to_pdf
from django.db import transaction
from django.shortcuts import render, redirect
from inventario.models import Articulo, Marca
@login_required(login_url='/seguridad/login/')
def articulo(request):
    data ={
        'titulo':'Consulta de artículos -FULL AUTO MILAGRO',
        'model': 'Artículo',
        'ruta':'/inventario/articulo/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        articulo =Articulo()

                        articulo.marca, articulo.image  = Marca.objects.get(pk=int(request.POST['marca'])), request.FILES['image']
                        articulo.nombre,articulo.descripcion  = request.POST['nombre'],request.POST['descripcion']
                        articulo.stock,articulo.iva,articulo.precio  = int(request.POST['stock']), float(request.POST['iva']),float(request.POST['precio'])
                        articulo.descuento,articulo.sucursal,articulo.subtotal= float(request.POST['descuento']),Sucursal.objects.get(pk=int(request.POST['sucursal'])),float(request.POST['subtotal'])
                        if not 'status' in request.POST:
                            articulo.status =False
                        articulo.save()

                    if action == 'edit':

                        articulo = Articulo.objects.select_related().get(pk=request.POST['id'])
                        articulo.marca = Marca.objects.get(pk=int(request.POST['marca']))
                        articulo.nombre,articulo.descripcion  = request.POST['nombre'],request.POST['descripcion']
                        articulo.stock,articulo.iva,articulo.precio  = int(request.POST['stock']), float(request.POST['iva']),float(request.POST['precio'])
                        articulo.descuento,articulo.sucursal,articulo.subtotal= float(request.POST['descuento']),Sucursal.objects.get(pk=int(request.POST['sucursal'])),float(request.POST['subtotal'])
                        if 'image' in request.FILES:
                            articulo.image = request.FILES['image']
                        if not 'status' in request.POST:
                            articulo.status = False
                        if 'status' in request.POST:
                            articulo.status = True
                        articulo.save()

                    if action == 'elim':

                        articul=Articulo.objects.get(pk=int(request.POST['id']))
                        articul.elim=False
                        articul.save()
            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/inventario/articulo/')
    else:
        # Por primera vez viaja por Get
        data['articulo'], data['sucursal'],data['buscarid'] = Articulo.objects.filter(elim=True), Sucursal.objects.filter(elim=True),0
        if 'sucursa' in request.GET:
            if Articulo.objects.filter(sucursal__id=int(request.GET['sucursa'])).exists():
                data['articulo'],data['buscarid'],data['sucursale'] = Articulo.objects.filter(sucursal=Sucursal.objects.get(pk=int(request.GET['sucursa']))),int(request.GET['sucursa']),Sucursal.objects.get(pk=int(request.GET['sucursa']))

            elif not (Articulo.objects.filter(sucursal__id=int(request.GET['buscarid'])).exists())  and (int(request.GET['sucursa']) !=0):
                messages.info(request, 'No se hay articulos en esta sucursal')

        elif 'imprime' in request.GET:
            if 'buscarid' in request.GET:
                if Articulo.objects.filter(sucursal__id=int(request.GET['buscarid'])).exists():
                    articulos = Articulo.objects.filter(sucursal=Sucursal.objects.get(pk=int(request.GET['buscarid'])),elim=True)
                    articulo = {

                        'articulo': articulos, 'empresa':  Empresa.objects.first(),'model': 'Articulo'
                    }
                    pdf = render_to_pdf('inventario/pdfarticulo.html', articulo)
                    return HttpResponse(pdf, content_type='application/pdf')
                elif int(request.GET['buscarid']) == 0:
                    articulos = Articulo.objects.filter(elim=True)

                    articulo = {

                        'articulo': articulos, 'empresa': Empresa.objects.first(),'model': 'Articulo'
                    }
                    pdf = render_to_pdf('inventario/pdfarticulo.html', articulo)
                    return HttpResponse(pdf, content_type='application/pdf')

        elif 'action' in request.GET:
            data['action'] = request.GET['action']
            if not (request.GET['action'] == 'add') :
                data['id'] = request.GET['id']
                data['articulo']= Articulo.objects.get(pk=int(request.GET['id']))
            data['marc'],data['sucursa']=Marca.objects.filter(elim=True),Sucursal.objects.filter(elim=True)
            return render(request, 'inventario/articulo_modal.html', data)

        return render(request, 'inventario/articulo.html', data)
