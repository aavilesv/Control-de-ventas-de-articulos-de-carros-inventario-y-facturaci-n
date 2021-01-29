from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sistemafinal.funciones import addUserData, MiPaginador
from django.db import transaction
from django.shortcuts import render, redirect
from inventario.models import  Articulo
@login_required(login_url='/seguridad/login/')
def inventario(request):
    data ={
        'titulo':'CONSULTA DE ARTÍCULO -FULL AUTO MILAGRO',
        'model': 'ARTÍCULO',
        'ruta':'/inventario/inventario/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        ceo = 0.12
                        if not 'iva' in request.POST:
                            ceo = 0
                        preci = (float(request.POST['precio']) * ceo) + float(request.POST['precio'])
                        articu = Articulo(nombre=request.POST['articulo'].upper(),
                                          descripcion=request.POST['descripcion'].capitalize(),
                                          cantidad=request.POST['cantidad']
                                          , iva=ceo, subtotal=request.POST['precio'], precio=round(preci, 0),
                                          image=request.FILES['image'])
                        articu.save()
                    if action == 'edit':
                        ceo = 0.12
                        if not 'iva' in request.POST:
                            ceo = 0
                        preci = (float(request.POST['precio']) * ceo) + float(request.POST['precio'])
                        arti = Articulo.objects.select_related().get(pk=request.POST['id'])
                        arti.nombre = request.POST['articulo'].upper()
                        arti.descripcion = request.POST['descripcion'].capitalize()
                        arti.cantidad = request.POST['cantidad']
                        arti.iva = ceo
                        arti.subtotal = request.POST['precio']
                        arti.precio = round(preci, 0)
                        arti.image = request.FILES['image']
                        arti.save()
                    if action == 'elim':
                        id = request.POST['id']
                        articul=Articulo.objects.get(pk=int(id))
                        articul.status=False
                        articul.save()
            except Exception as ex:
                messages.error(request, 'Error, dato ya registrado')
            return redirect('/scmi/articulo/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'edit':
                id = request.GET['id']
                data['id'] = id
                articulos= Articulo.objects.get(pk=id)
                data['articulos']=articulos
            return render(request, 'facturacion/articulo_from.html', data)
        else:
            # Viaja por get cuando hay busqueda con criterio
            criterio = None
            if 'criterio' in request.GET:
                criterio = request.GET['criterio'].upper()
            if criterio:
                # Entra por criterio de busqueda
                articulo = Articulo.objects.filter(nombre__contains=criterio,status=True)
                data['criterio'] = criterio
            else:
                # La primera vez viaje por get sin criterio: consulta todos los datos
                articulo= Articulo.objects.filter(status=True)
                data['articulos']=articulo
            #Pagineo
            paging = MiPaginador(articulo, 4)
            p = 1
            try:
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                page = paging.page(p)
            except:
                page = paging.page(p)
            data['paging'] = paging
            data['rangospaging'] = paging.rangos_paginado(p)
            data['page'] = page
            data['articulos'] = page.object_list
            return render(request, 'inventario/articulo.html', data)
