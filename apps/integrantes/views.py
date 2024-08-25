from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.db import IntegrityError
from django.db.models import Q


from .froms import MiembroForm

from .import models
class OrganigramaView(ListView):
    model = models.MiembroGrupoUSAR
    template_name = 'organigrama.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voluntarios = models.MiembroGrupoUSAR.objects.all().values('pk', 'nombre', 'puesto', 'genero', 'cedula', 'componente', 'asignacion_operacional').order_by('nombre')
        
        context["voluntarios"] = voluntarios
        context["voluntarios_seguridad"] = voluntarios.filter(
            Q(componente__icontains='seguridad') | Q(componente__icontains='SEGURIDAD')
        )
        context["voluntarios_busqueda_rescate"] = voluntarios.filter(
            Q(componente__icontains='RESCATISTA') | Q(componente__icontains='BUSQUEDA Y RESCATE')
        )
        context["voluntarios_planeacion"] = voluntarios.filter(
            Q(componente__icontains='planeación') | Q(componente__icontains='PLANEACIÓN') |
            Q(componente__icontains='planeacion') | Q(componente__icontains='PLANEACION')
        )
        context["voluntarios_logistica"] = voluntarios.filter(
            Q(componente__icontains='logístico') | Q(componente__icontains='LOGÍSTICO') |
            Q(componente__icontains='logistico') | Q(componente__icontains='LOGISTICO')
        )
        context["voluntarios_operaciones"] = voluntarios.filter(
            Q(componente__icontains='operaciones') | Q(componente__icontains='OPERACIONES')
        )
        context["voluntarios_unidad_medica"] = voluntarios.filter(
            Q(componente__icontains='salud') | Q(componente__icontains='SALUD') 
        )
        context["voluntarios_comunicacion"] = voluntarios.filter(
            Q(componente__icontains='comunicación') | Q(componente__icontains='COMUNICACIÓN') |
            Q(componente__icontains='comunicacion') | Q(componente__icontains='COMUNICACION')
        )
        
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
    
class MiembroGrupoUSARCreateView(CreateView):
    model = models.MiembroGrupoUSAR
    template_name = 'form_miembro.html'
    form_class=MiembroForm
    success_url = reverse_lazy('voluntarios')

    def form_valid(self, form):
        messages.success(self.request, 'Miembro creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error en {field}: {error}')
        return super().form_invalid(form)

class MiembroGrupoUSARUpdateView(UpdateView):
    model = models.MiembroGrupoUSAR
    template_name = 'form_miembro.html'
    form_class=MiembroForm
    success_url = reverse_lazy('voluntarios')
    

    def form_valid(self, form):
        messages.success(self.request, 'Miembro actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error en {field}: {error}')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        miembro = self.get_object()  # Obtenemos el objeto que se está editando
        context['miembro'] = miembro
        return context


def eliminar_voluntario(request, pk):
    voluntario = get_object_or_404(models.MiembroGrupoUSAR, pk=pk)
    voluntario.delete()
    return redirect('voluntarios')  