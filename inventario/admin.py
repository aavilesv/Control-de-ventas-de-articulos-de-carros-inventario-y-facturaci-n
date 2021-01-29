from django.contrib import admin


from inventario.models import  Marca,Articulo,Kardex,Inventario


admin.site.register(Marca)
admin.site.register(Articulo)
admin.site.register(Kardex)
admin.site.register(Inventario)