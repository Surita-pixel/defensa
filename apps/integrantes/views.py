from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .import models
class OrgaigramaView(ListView):
    model=models.MiembroGrupoUSAR
    template_name='organigrama.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["voluntarios"] = models.MiembroGrupoUSAR.objects.all().values('pk','nombre', 'puesto', 'genero','cedula','componente','asignacion_operacional').order_by('nombre')
        return context
    
    
class VoluntariosView(ListView):
    model = models.MiembroGrupoUSAR
    template_name = 'voluntarios_detail.html'
    context_object_name = 'voluntarios'
    paginate_by = 10  # Número de elementos por página

    def get_queryset(self):
        return models.MiembroGrupoUSAR.objects.all().order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class VoluntarioDetail(DetailView):
    model=models.MiembroGrupoUSAR
    context_object_name='voluntario'
    template_name='voluntario.html'