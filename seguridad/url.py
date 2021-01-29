from django.urls import path
from seguridad.view_empresa import empresa
from seguridad.view_usuariote import usuariote
from seguridad.view_sucursal import sucursal
from seguridad.view_estadistica import estadistica

from seguridad.views import  login_session,logout_user
from seguridad.viewrecuperar import recuperar
from seguridad.perfil import perfil
urlpatterns = [
path('login/' ,login_session ,name='login'),
path('logout/', logout_user ,name='logout'),
path('recuperar/', recuperar ,name='recuperar'),
path('perfil/', perfil ,name='perfil'),
path('perfil/', perfil ,name='perfil'),
path('estadistica/', estadistica ,name='estadistica'),

path('sucursal/' ,sucursal ,name='sucursal'),
path('empresa/', empresa ,name='empresa'),
path('usuariote/', usuariote ,name='usuariote'),
]