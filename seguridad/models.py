
from django.db import models
from django.contrib.auth.models import User, Group
class Modulo(models.Model):
    url = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['orden']


class ModuloGrupo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    modulos = models.ManyToManyField(Modulo)
    grupos = models.ManyToManyField(Group)
    prioridad = models.IntegerField(null=True, blank=True)
    icono = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Grupo de Módulos'
        verbose_name_plural = 'Grupos de Módulos'
        ordering = ('prioridad', 'nombre')

    def modulos_activos(self):
        return self.modulos.filter(activo=True).order_by('orden')



class Empresa(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre",default='')
    ruc = models.CharField(max_length=15, verbose_name="cedula", default='')
    direcion = models.CharField(max_length=50, verbose_name="direccion", default='')
    celular = models.CharField(max_length=50, verbose_name="celular", default='')
    image = models.ImageField(upload_to='empresa/%Y/%m/%d/', default='')
    email=models.CharField(max_length=200,verbose_name="Email",default="")
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}--{}'.format(self.nombre,self.direcion)

    class Meta:
        verbose_name = 'Grupo de Empresa'
        verbose_name_plural = 'Grupos de Empresa'
        ordering = ('nombre', 'nombre')

class Sucursal(models.Model):
    razonsocial = models.CharField(max_length=200, verbose_name="razonsocial",default='')
    ruc = models.CharField(max_length=15, verbose_name="ruc", default='')
    direcion = models.CharField(max_length=50, verbose_name="direccion", default='')
    celular = models.CharField(max_length=50, verbose_name="celular", default='')
    image = models.ImageField(upload_to='sucursal/%Y/%m/%d/', default='')
    email=models.CharField(max_length=200,verbose_name="Email",default="")
    status = models.BooleanField(default=True)
    canton = models.CharField(max_length=15, verbose_name="Ciudad", default='')
    provincia = models.CharField(max_length=15, verbose_name="provincia", default='')
    sucursal_id =  models.IntegerField(default=0)
    elim = models.BooleanField(default=True)

    def __str__(self):
        return '{}--{}'.format(self.razonsocial,self.direcion)

    class Meta:
        verbose_name = 'Grupo de Sucursal'
        verbose_name_plural = 'Grupos de Sucursal'
        ordering = ('razonsocial', 'razonsocial')


class Empleado(models.Model):
    cedula = models.CharField(max_length=15, verbose_name="cedula", default='')
    direcion = models.CharField(max_length=50, verbose_name="direccion", default='')
    celular = models.CharField(max_length=50, verbose_name="celular", default='')
    image = models.ImageField(upload_to='empleado/%Y/%m/%d/', default='')
    fecha = models.DateTimeField(default='', verbose_name="Fecha Ingreso", blank=True)
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return '{}--{}'.format(self.cedula,self.direcion)

    class Meta:
        verbose_name = 'Grupo de Empleado'
        verbose_name_plural = 'Grupos de Empleados'
        ordering = ('id', 'id')

class Fotouser(models.Model):
    pass