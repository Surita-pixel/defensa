from django.shortcuts import render
from django.views.generic import ListView
from .import models
class OrgaigramaView(ListView):
    model=models.MiembroGrupoUSAR
    template_name='organigrama.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["voluntarios"] = models.MiembroGrupoUSAR.objects.all().values('pk','nombre', 'puesto', 'genero','cedula','componente','asignacion_operacional').order_by('nombre')
        return context
    