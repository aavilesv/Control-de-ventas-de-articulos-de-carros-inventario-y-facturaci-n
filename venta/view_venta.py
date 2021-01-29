from django.contrib.auth.models import User
from django.db.models import Q
from inventario.models import Articulo
from sistemafinal.funciones import addUserData, render_to_pdf
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction ,IntegrityError
from seguridad.models import Empleado, Sucursal, Empresa
from django.utils.html import strip_tags
import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from venta.models import Venta, Cliente, DetalleVenta
@login_required(login_url='/seguridad/login/')
def venta(request):
    data ={
        'titulo':'Consulta de ventas -FULL AUTO MILAGRO',
        'model': 'Venta',
        'ruta':'/venta/venta/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():

                    if action == 'elim':
                        venta = Venta.objects.get(pk=int(request.POST['id']))
                        venta.status = False
                        venta.usermodificardor, venta.userfechamodificador= int(request.user.id),datetime.datetime.now()

                        venta.save()
                        e = Empleado.objects.get(user=request.user)

                        for item in DetalleVenta.objects.filter(venta=venta):

                            print(item.articulo.id)
                            if Articulo.objects.filter(sucursal=Sucursal.objects.get(pk=e.sucursal.id)).exists():
                                print('entrar')
                                arct=(Articulo.objects.get(pk=int(item.articulo.id)))
#                                arct= Articulo.objects.get(Q(sucursal=Sucursal.objects.filter(pk=e.sucursal.id)) & Q(pk=int(item.articulo.id)))
                                arct.stock += int(item.cantidad)
                                arct.save()


            except Exception as ex:
                messages.error(request, str(ex))
            return redirect('/venta/venta/')
    # Por primera vez viaja por Get
    elif 'action' in request.GET:
        action = request.GET['action']
        data['action'] = action
        if action == 'cargaventa':
            try:
                with transaction.atomic():
                    ventajson = json.loads(request.GET['venta'])
                    vent = Venta()
                    vent.cliente,vent.iva = Cliente.objects.get(pk=int(ventajson['cliente'])),round(float(ventajson['subtotal']) * 0.12)
                    vent.subtotal ,vent.total  = round(float(ventajson['subtotal'])), round(float(ventajson['total']))
                    vent.fechaventa,vent.descuento = datetime.datetime.now(),0
                    vent.user = (request.user)
                    vent.userfecha=datetime.datetime.now()
                    e=Empleado.objects.get(user=request.user)
                    vent.sucursal = Sucursal.objects.get(pk=e.sucursal.id)
                    vent.usermodificardor,vent.userfechamodificador,vent.empresa = 0,datetime.datetime.now(), Empresa.objects.get(pk=1)
                    vent.save()

                    for item in ventajson['items']:

                        if Articulo.objects.filter(id=int(item['id'])).exists():
                            detalle = DetalleVenta()
                            detalle.venta,detalle.articulo = vent, Articulo.objects.get(pk=int(item['id']))
                            detalle.cantidad,detalle.total  =int(item['cantidad']), float(item['precio'])
                            arct = Articulo.objects.get(pk=int(item['id']))
                            arct.stock -= int(item['cantidad'])
                            arct.save()
                            detalle.preciototal = round(float(item['precio'])*int(item['cantidad']))
                            detalle.save()
                    # asunto = 'Compra en Taller Herrera'
                    # email_from = settings.EMAIL_HOST_USER
                    # data['detalle'] = Detallecompra.objects.filter(factura=facturar)
                    # data['empresa'] = Empresa.objects.get(user=request.user)
                    # email_to = [cliente.email]
                    # datos = {
                    #     'factura': facturar,
                    #     'detalle': Detallecompra.objects.filter(factura=facturar),
                    #     'sucursal': Empresa.objects.get(user=request.user),
                    # }
                    # html_message = render_to_string('facturacion/correoenvio.html', datos)
                    # plain_message = strip_tags(html_message)
                    # send_mail(asunto, plain_message, email_from, email_to, html_message=html_message,
                    #           fail_silently=True)
                    return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
            except IntegrityError as ex:

                return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                    content_type="application/json")
        if action == 'add':
            data['cliente'],data['articul'] = Cliente.objects.filter(status=True),Articulo.objects.filter(precio__gte=1,elim=True)
            return render(request, 'venta/venta_form.html', data)

        if action == 'ver':
            id = request.GET['id']
            v=Venta.objects.get(pk=id)
            data['venta'],data['detalle'] =v,DetalleVenta.objects.filter(venta=Venta.objects.get(pk=id)).order_by('articulo_id')

            return render(request, 'venta/venta_visualizar.html', data)


    elif 'imprimeunidad' in request.GET:
        id = request.GET['id']
        v=Venta.objects.get(pk=int(id))
        t = "0"
        for i in range(9-len(str(v.id))):
            t+="0"
        factura = {

            'venta': DetalleVenta.objects.filter(venta=Venta.objects.get(pk=id)).order_by('articulo_id'),
            'empresa': Empresa.objects.first(),
            'facturaa':v,
            'model': 'Factura: '+t+str(v.id)
        }
        pdf = render_to_pdf('venta/pdffacturaunidad.html', factura)
        return HttpResponse(pdf, content_type='application/pdf')

    elif 'imprime' in request.GET:

        cliente = {

            'venta': Venta.objects.all(),
            'empresa': Empresa.objects.first(),
            'model': 'Factura'
        }
        pdf = render_to_pdf('venta/pdfventa.html', cliente)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        # Viaja por get
        data['venta'] =  Venta.objects.all().order_by('id')
        return render(request, 'venta/Venta.html', data)
