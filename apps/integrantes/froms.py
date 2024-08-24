from django import forms
from .models import MiembroGrupoUSAR
class MiembroForm(forms.ModelForm):
    class Meta:
        model = MiembroGrupoUSAR
        fields = ['nombre', 'puesto', 'edad', 'genero', 'cedula', 'componente', 
                  'asignacion_operacional', 'eps', 'arl', 'rh', 'curso_basico', 
                  'curso_sci', 'curso_svb', 'curso_crecl', 'curso_svt', 
                  'curso_matpel', 'curso_macom', 'curso_revert', 'curso_bra']
        
