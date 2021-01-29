from django.urls import path
from inventario.view_articulo import articulo
from inventario.view_inventario import inventario
from inventario.view_marca import marca

urlpatterns = [
    path('articulo/' ,articulo ,name='articulo'),
path('marca/' ,marca ,name='marca'),
    path('inventario/', inventario, name='inventario'),

]