from django.urls import path
from venta.view_venta import venta
from venta.view_cliente import cliente

urlpatterns = [
path('venta/' ,venta ,name='venta'),
path('cliente/' ,cliente ,name='cliente'),


]