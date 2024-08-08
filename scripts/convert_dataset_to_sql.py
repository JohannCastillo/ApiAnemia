import csv
import os
import sys
import django
from datetime import datetime
import warnings

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiAnemia.settings')
django.setup()
warnings.filterwarnings("ignore", category=RuntimeWarning, message="DateTimeField .* received a naive datetime")

from api.models import Nivel_Anemia, Diagnostico

def get_diagnostico_obj_by_csv(row):
    edad_meses = row['EdadMeses']
    peso = row['Peso']
    talla = row['Talla']
    hemoglobina = row['Hemoglobina']
    cred = 'true' if row['Cred'] == 1 else 'false'
    suplementacion = 'true' if row['Suplementacion'] == 1 else 'false'
    diagnostico = row['Dx_anemia']
    dx_anemia_id  = Nivel_Anemia.objects.get(nivel=diagnostico).id
    created_at = row['FechaAtencion']
    # Formato de fecha atencion: 1/22/2019 -> yyyy-MM-dd
    try:
        formatted_fecha = datetime.strptime(created_at, '%Y-%m-%d').strftime('%Y-%m-%d')
    except Exception:
        formatted_fecha = datetime.strptime(created_at, '%m/%d/%Y').strftime('%Y-%m-%d')

    return {
        'edad_meses': edad_meses,
        'peso': peso,
        'talla': talla,
        'hemoglobina': hemoglobina,
        'cred': cred,
        'suplementacion': suplementacion,
        'dx_anemia_id': dx_anemia_id,
        'created_at': formatted_fecha,
        'updated_at': formatted_fecha,
        'paciente_id': 1
    }


def convert_to_postgre_sql_insert(file_path, output_sql):
    with open(file_path, newline='', encoding='utf-8') as csvfile, open(output_sql, 'w', encoding='utf-8') as sqlfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            diagnostico_obj = get_diagnostico_obj_by_csv(row)
            edad_meses = diagnostico_obj['edad_meses']
            peso = diagnostico_obj['peso']
            talla = diagnostico_obj['talla']
            hemoglobina = diagnostico_obj['hemoglobina']
            cred = diagnostico_obj['cred']
            suplementacion = diagnostico_obj['suplementacion']
            dx_anemia_id = diagnostico_obj['dx_anemia_id']
            formatted_fecha = diagnostico_obj['formatted_fecha']

            insert_stmnt = f"INSERT INTO public.api_diagnostico (edad_meses, peso, talla, hemoglobina, cred, suplementacion, dx_anemia_id, created_at, updated_at, paciente_id) VALUES({edad_meses}, {peso}, {talla}, {hemoglobina}, {cred}, {suplementacion}, {dx_anemia_id}, '{formatted_fecha}', '{formatted_fecha}', 1);"
            
            sqlfile.write(insert_stmnt + '\n')

def insert_diagnosticos(diagnosticos_file):
    with open(diagnosticos_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            diagnostico_obj = get_diagnostico_obj_by_csv(row)
            diagnostico_obj['suplementacion'] = diagnostico_obj['suplementacion'].lower() == 'true'
            diagnostico_obj['cred'] = diagnostico_obj['cred'].lower() == 'true'
            newDiagnostico = Diagnostico(**diagnostico_obj)
            newDiagnostico.save()
        print("Diagnosticos guardados con éxito")

if __name__ == "__main__":
    file_path = 'df_limpio.csv'  # Reemplaza con la ruta a tu archivo CSV
    output_sql_file = 'diagnosticos.sql'
    # convert_to_postgre_sql_insert(file_path, output_sql_file)
    insert_diagnosticos(file_path)
    print("Datos cargados con éxito")