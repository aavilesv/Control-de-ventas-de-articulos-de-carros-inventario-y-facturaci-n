from django.db import models

# Create your models here.
from seguridad.models import Sucursal


class Marca(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre",default='')
    descripcion = models.CharField(max_length=200,verbose_name="Descripción",default='')
    status = models.BooleanField(default=True)
    elim = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.nombre)
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre']


class Articulo(models.Model):
    marca = models.ForeignKey(Marca,on_delete=models.PROTECT)
    nombre = models.CharField(max_length=200, verbose_name="Nombre", default='')
    descripcion = models.CharField(max_length=200,verbose_name="Descripción",default='')
    precio = models.DecimalField(decimal_places=2,verbose_name="Precio", max_digits=19,default=0)
    stock = models.IntegerField(default=0,verbose_name="stock")
    iva = models.DecimalField(decimal_places=0, verbose_name="Iva", max_digits=19, default=0)
    subtotal = models.DecimalField(decimal_places=0, verbose_name="Subtotal", max_digits=19, default=0)
    descuento = models.DecimalField(decimal_places=0, verbose_name="Descuento", max_digits=19, default=0)
    status = models.BooleanField(default=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='articulo/%Y/%m/%d/', default='')
    elim  = models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'
        ordering = ['nombre']


class Kardex(models.Model):
    Descripcion = models.CharField(max_length=200, verbose_name="Nombre", default='')
    fechaingreso = models.DateTimeField(default='', verbose_name="Fecha Ingreso", blank=True)
    cantidad = models.IntegerField(default=0,verbose_name="Stock")
    fechasalida = models.DateTimeField(default='', verbose_name="Fecha Ingreso", blank=True)
    prioridad = models.IntegerField(null=True, blank=True)
    iva = models.DecimalField(decimal_places=0, verbose_name="Iva",max_digits=19,default=0)
    preciocompra = models.DecimalField(decimal_places=0,verbose_name="Precio Compra", max_digits=19,default=0)
    precioventa = models.DecimalField(decimal_places=0,verbose_name="Precio Venta", max_digits=19,default=0)
    user = models.IntegerField(default=0,verbose_name="Usuario")
    userfecha = models.DateTimeField(default='', verbose_name="Fechausuario")
    usermodificardor = models.IntegerField(default=0,verbose_name="Descuento")
    userfechamodificador = models.DateTimeField(default='', verbose_name="Fechamodificada")
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}-{}'.format(self.fechacompra,self.subtotal)
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']

class Inventario(models.Model):
    kardex = models.ForeignKey(Kardex,on_delete=models.PROTECT)
    articulo = models.ForeignKey(Articulo,on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['articulo']


