import pandas as pd
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "usar_l_ns.settings")
django.setup()
from django.core.exceptions import ObjectDoesNotExist
from apps.integrantes.models import MiembroGrupoUSAR

def actualizar_cursos():
    # Leer el archivo Excel
    df = pd.read_excel('CURSOS USAR (1).xlsx')
    
    # Imprimir los nombres de las columnas para verificar
    print("Columnas en el archivo Excel:")
    print(df.columns.tolist())

    # Mapeo de nombres de columnas a campos del modelo
    cursos_mapeo = {
        'CURSO BASICO ': 'curso_basico',
        'SCI': 'curso_sci',
        'SVB': 'curso_svb',
        'CRECL': 'curso_crecl',
        'SVT': 'curso_svt',
        'MATPEL': 'curso_matpel',
        'MACOM': 'curso_macom',
        'REVERT': 'curso_revert',
        'BRA': 'curso_bra'
    }

    # Iterar sobre cada fila del DataFrame
    for index, row in df.iterrows():
        nombre_completo = row['NOMBRES Y APELLIDOS']
        
        try:
            # Intentar obtener el miembro por nombre
            miembro = MiembroGrupoUSAR.objects.get(nombre=nombre_completo)
            
            # Actualizar los cursos
            for columna, campo_modelo in cursos_mapeo.items():
                if columna in df.columns:
                    # Establecer True si es 'SI', False en cualquier otro caso
                    valor = str(row[columna]).strip().upper() == 'SI'
                    setattr(miembro, campo_modelo, valor)
                else:
                    print(f"La columna '{columna}' no existe en el Excel.")
                    
            # Guardar los cambios
            miembro.save()
            print(f"Actualizado: {nombre_completo}")
        
        except ObjectDoesNotExist:
            print(f"No se encontró el miembro: {nombre_completo}")

    print("Proceso completado.")

# Ejecutar la función
if __name__ == "__main__":
    actualizar_cursos()