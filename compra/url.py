from django.urls import path
from compra.view_compra import compra
from compra.view_proveedor import  proveedor

urlpatterns = [
path('proveedor/' ,proveedor ,name='proveedor'),

path('compra/' ,compra ,name='compra'),
]