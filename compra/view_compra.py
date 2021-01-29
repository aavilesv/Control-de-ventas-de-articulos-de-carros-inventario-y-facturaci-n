from django.contrib.auth.models import User
from compra.models import Compra, Proveedor, Detallecompra
from inventario.models import Articulo
from seguridad.models import Empresa
from sistemafinal.funciones import addUserData, render_to_pdf
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction ,IntegrityError
import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required(login_url='/seguridad/login/')
def compra(request):
    data ={
        'titulo':'Consulta de compras -FULL AUTO MILAGRO',
        'model': 'Compra',
        'ruta':'/compra/compra/',
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

                    if action == 'elim':
                        compra = Compra.objects.get(pk=int(request.POST['id']))
                        compra.status = False
                        compra.usermodificardor, compra.userfechamodificador= int(request.user.id),datetime.datetime.now()
                        compra.save()

            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/compra/compra/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'cargacompra':
                try:
                    with transaction.atomic():
                        comprajson,  compra = json.loads(request.GET['compra']), Compra()


                        compra.proveedor,compra.iva = Proveedor.objects.get(pk=int(comprajson['cliente'])),0
                        compra.subtotal ,compra.total  = round(float(comprajson['subtotal'])), round(float(comprajson['total']))
                        compra.fechacompra,compra.descuento = datetime.datetime.now(),0
                        compra.user,compra.userfecha =request.user,datetime.datetime.now()
                        compra.usermodificardor,compra.userfechamodificador = 0,datetime.datetime.now()
                        compra.save()

                        for item in comprajson['items']:
                            if Articulo.objects.filter(id=int(item['id'])).exists():
                                detalle,arct = Detallecompra(),Articulo.objects.get(pk=int(item['id']))
                                detalle.compra,detalle.articulo,detalle.cantidad= compra, Articulo.objects.get(pk=int(item['id'])),int(item['cantidad'])
                                detalle.total, detalle.preciototal  =float(item['precio']), round(float(item['precio'])*int(item['cantidad']))

                                arct.stock += int(item['cantidad'])
                                arct.save()

                                detalle.save()
                        return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
                except IntegrityError as ex:

                    return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                        content_type="application/json")
            if action == 'add':
                data['proveedo'],data['articul'] = Proveedor.objects.filter(status=True),Articulo.objects.filter(elim=True)
                return render(request, 'compra/compra_form_principal.html', data)

            if action == 'ver':
                id = request.GET['id']
                data['compra'],data['detalle'] = Compra.objects.get(pk=id),Detallecompra.objects.filter(compra=Compra.objects.get(pk=id))

            return render(request, 'compra/compra_form_principal.html', data)
        elif 'imprimeunidad' in request.GET:
            id = request.GET['id']
            v = Compra.objects.get(pk=int(id))
            t = "0"
            for i in range(9 - len(str(v.id))):
                t += "0"
            compra = {

                'compra': Detallecompra.objects.filter(compra=Compra.objects.get(pk=id)).order_by('articulo_id'),
                'empresa': Empresa.objects.first(),
                'facturaa': v,
                'model': 'Compra: ' +t+ str(v.id)
            }
            pdf = render_to_pdf('compra/pdfcompraunidad.html', compra)
            return HttpResponse(pdf, content_type='application/pdf')

        elif 'imprime' in request.GET:

            proveedor = {

                'compra': Compra.objects.all(), 'empresa': Empresa.objects.first(),
                'model': 'Compra'
            }
            pdf = render_to_pdf('compra/pdfcompra.html', proveedor)
            return HttpResponse(pdf, content_type='application/pdf')


        else:
            # Viaja por get
            compra = Compra.objects.all()
            data['compra'] = compra
            return render(request, 'compra/Compra.html', data)
