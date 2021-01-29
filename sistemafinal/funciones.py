from django.core.paginator import Paginator
from django.utils.timezone import now
from io import BytesIO # nos ayuda a convertir un html en pdf
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from sistemafinal.config import LOGO_SISTEMA, NOMBRE_SISTEMA, NOMBRE_AUTOR, NOMBRE_INSTITUCION
from seguridad.models import ModuloGrupo, Empleado

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def addUserData(request, data):
    data['hoy'] = now
    data['usuario'] = request.user
    data['logo'] = LOGO_SISTEMA
    data['sistema'] = NOMBRE_SISTEMA
    data['institucion'] = NOMBRE_INSTITUCION
    data['autor'] = NOMBRE_AUTOR
    data['grupos'] = ModuloGrupo.objects.filter(grupos__in=request.user.groups.all()).order_by('prioridad')
    data['foto']=Empleado.objects.get(user=request.user)
    data['grupo'] = request.user.groups.all()[0]



class MiPaginador(Paginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, rango=1):
        super(MiPaginador, self).__init__(object_list, per_page, orphans=orphans,
                                          allow_empty_first_page=allow_empty_first_page)
        self.rango = rango
        self.paginas = []
        self.primera_pagina = False
        self.ultima_pagina = False

    def rangos_paginado(self, pagina):
        left = pagina - self.rango
        right = pagina + self.rango
        if left < 1:
            left = 1
        if right > self.num_pages:
            right = self.num_pages
        self.paginas = range(left, right + 1)
        self.primera_pagina = True if left > 1 else False
        self.ultima_pagina = True if right < self.num_pages else False
        self.ellipsis_izquierda = left - 1
        self.ellipsis_derecha = right + 1