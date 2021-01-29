from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from inventario.models import Articulo


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre",default='')
    direccion = models.CharField(max_length=200,verbose_name="Dirección",default='')
    telefono = models.CharField(max_length=10,verbose_name="Telefono",default='')
    ced_ruc = models.CharField(max_length=14, verbose_name="Cedula o Ruc",default='')
    email=models.CharField(max_length=200,verbose_name="Email",default="")
    status = models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.nombre)
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']


class Compra(models.Model):
    fechacompra = models.DateTimeField(default='', verbose_name="Fecha", blank=True)
    iva = models.DecimalField(decimal_places=0, verbose_name="Iva",max_digits=19,default=0)
    subtotal = models.DecimalField(decimal_places=0,verbose_name="Subtotal", max_digits=19,default=0)
    total = models.DecimalField(decimal_places=0,verbose_name="Total", max_digits=19,default=0)
    descuento = models.DecimalField(decimal_places=0,verbose_name="Descuento", max_digits=19,default=0)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.PROTECT)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    userfecha = models.DateTimeField(default='', verbose_name="Fechausuario")
    usermodificardor = models.IntegerField(default=0,verbose_name="Fechausuariomodifcador")
    userfechamodificador = models.DateTimeField(default='', verbose_name="Fechamodificada")
    status = models.BooleanField(default=True)
    tipocomprobante = models.IntegerField(default=0,verbose_name="Tipo de comrobante")
    impuesto = models.DecimalField(decimal_places=0,verbose_name="Descuento", max_digits=19,default=0)


    def __str__(self):
        return '{}-{}'.format(self.fechacompra,self.subtotal)
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']

class Detallecompra(models.Model):
    compra = models.ForeignKey(Compra,on_delete=models.PROTECT)
    articulo = models.ForeignKey(Articulo,on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=0,verbose_name="Cantidad")
    total = models.DecimalField(decimal_places=0,verbose_name="Total", max_digits=19,default=0)
    preciototal = models.DecimalField(decimal_places=0,verbose_name="Precio Total", max_digits=19,default=0)

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        ordering = ['id']
