"""
URL configuration for usar_l_ns project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.integrantes.views import OrganigramaView,VoluntariosView,VoluntarioDetail,MiembroGrupoUSARCreateView, MiembroGrupoUSARUpdateView, eliminar_voluntario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', OrganigramaView.as_view()),
    path('voluntarios/', VoluntariosView.as_view(), name='voluntarios'),
    path('voluntario/<int:pk>/', VoluntarioDetail.as_view(), name='voluntario_detail'),
    path('voluntario/nuevo/', MiembroGrupoUSARCreateView.as_view(), name='crear_miembro'),
    path('voluntario/editar/<int:pk>/', MiembroGrupoUSARUpdateView.as_view(), name='editar_miembro'),
    path('voluntario/eliminar/<int:pk>/', eliminar_voluntario, name='eliminar_miembro'),
]
