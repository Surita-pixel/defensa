from django.db import models

class MiembroGrupoUSAR(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    puesto = models.CharField(max_length=100, null=True)
    edad = models.IntegerField(null=True)
    genero = models.CharField(max_length=20, null=True)
    cedula = models.CharField(max_length=20,  null=True)
    componente = models.CharField(max_length=50, null=True)
    asignacion_operacional = models.CharField(max_length=100, null=True)
    eps = models.CharField(max_length=50, null=True)
    arl = models.CharField(max_length=50, null=True)
    rh = models.CharField(max_length=100, null=True)

    # # Vacunas
    # fiebre_amarilla = models.BooleanField(default=False)
    # tetano = models.BooleanField(default=False)
    # hepatitis_a = models.BooleanField(default=False)
    # hepatitis_b = models.BooleanField(default=False)
    # influenza = models.BooleanField(default=False)
    # covid = models.BooleanField(default=False)

    # direccion_domicilio = models.TextField(null=True)
    # telefono_celular = models.CharField(max_length=20, null=True)
    # email = models.EmailField(null=True)

    # # Contacto de emergencia
    # contacto_emergencia_nombre = models.CharField(max_length=100, null=True)
    # contacto_emergencia_telefono = models.CharField(max_length=20, null=True)
    # contacto_emergencia_parentesco = models.CharField(max_length=50, null=True)

    # # Certificados (puedes ajustar según necesidades)
    # certificado_cbdcc = models.BooleanField(default=False)
    # certificado_cbdcc_fecha = models.DateField(null=True, blank=True)

    # # Información adicional
    # fecha_nacimiento = models.DateField(null=True)
    # lugar_nacimiento = models.CharField(max_length=100, null=True)
    # licencia_conduccion_tipo = models.CharField(max_length=50, blank=True, null=True)

    curso_basico = models.BooleanField(default=False)
    curso_sci = models.BooleanField(default=False)
    curso_svb = models.BooleanField(default=False)
    curso_crecl = models.BooleanField(default=False)
    curso_svt = models.BooleanField(default=False)
    curso_matpel = models.BooleanField(default=False)
    curso_macom = models.BooleanField(default=False)
    curso_revert = models.BooleanField(default=False)
    curso_bra = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
