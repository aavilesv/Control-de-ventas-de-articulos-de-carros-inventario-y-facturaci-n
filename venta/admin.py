from django.contrib import admin

from venta.models import  Cliente,Venta,DetalleVenta


admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(DetalleVenta)

