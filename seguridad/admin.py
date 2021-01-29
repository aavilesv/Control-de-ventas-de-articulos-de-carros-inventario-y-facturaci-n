from django.contrib import admin

from seguridad.models import Modulo, ModuloGrupo,Empleado,Empresa,Sucursal,Fotouser

admin.site.register(Modulo)
admin.site.register(Empleado)
admin.site.register(Empresa)
admin.site.register(ModuloGrupo)
admin.site.register(Sucursal)
admin.site.register(Fotouser)
# Register your models here.
