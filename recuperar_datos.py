import os
import django
import pandas as pd
import numpy as np  # Importa numpy para manejar NaN

# Configura el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "usar_l_ns.settings")
django.setup()

# Importa tu modelo después de configurar Django
from apps.integrantes.models import MiembroGrupoUSAR

def import_data():
    # Lee el archivo Excel
    df = pd.read_excel('PERSONAL USAR NORTE DE SANTANDER MAYO 8 2024 (2).xlsx', sheet_name='BOGOTA 2024')
    df = df.iloc[1:]
    
    # Reemplaza NaN con None
    df = df.where(pd.notnull(df), None)
    
    lista_diccionarios = df.to_dict(orient='records')
    print(lista_diccionarios)
    for datos in lista_diccionarios:
        cedula = datos['CEDULA']
        if pd.isna(cedula):  
            cedula = None 
        
        if cedula is not None: 
            miembro_grupo_usar = MiembroGrupoUSAR(
                nombre=datos['NOMBRE'],
                genero=datos['GENERO'],
                cedula=str(cedula), 
                componente=datos['COMPONENTE'],
                asignacion_operacional=datos['ASIGNACION OPERACIONAL'],
                eps=datos['EPS'],
                arl=datos['ARL'],
                rh=datos['RH'],
                # direccion_domicilio=datos['DIRECCION DOMICILIO'],
                # telefono_celular=str(datos['TELEFONO CELULAR']),
                # email=datos['EMAIL'],
            )
            miembro_grupo_usar.save()
        
    print('Datos importados exitosamente')

if __name__ == "__main__":
    file_path = 'PERSONAL USAR NORTE DE SANTANDER MAYO 8 2024 (2).xlsx'  # Reemplaza con la ruta real de tu archivo
    import_data()
