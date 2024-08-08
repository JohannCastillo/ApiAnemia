import csv
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiAnemia.settings')
django.setup()


def convert_to_postgre_sql_insert(file_path, output_sql):
    with open(file_path, newline='', encoding='utf-8') as csvfile, open(output_sql, 'w', encoding='utf-8') as sqlfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            edad_meses = row['EdadMeses']
            peso = row['Peso']
            talla = row['Talla']
            hemoglobina = row['Hemoglobina']
            cred = 'true' if row['Cred'] == 1 else 'false'
            suplementacion = 'true' if row['Suplementacion'] == 1 else 'false'
            diagnostico = row['Dx_anemia']
            created_at = row['FechaAtencion']
            # Formato de fehca atencion: 1/22/2019 -> yyyy-MM-dd
            try:
                formatted_fecha = datetime.strptime(created_at, '%Y-%m-%d').strftime('%Y-%m-%d')
            except Exception:
                formatted_fecha = datetime.strptime(created_at, '%m/%d/%Y').strftime('%Y-%m-%d')


            insert_stmnt = f"INSERT INTO public.api_diagnostico (edad_meses, peso, talla, hemoglobina, cred, suplementacion, dx_anemia, created_at, updated_at, paciente_id) VALUES({edad_meses}, {peso}, {talla}, {hemoglobina}, {cred}, {suplementacion}, '{diagnostico}', '{formatted_fecha}', '{formatted_fecha}', 1);"
            
            sqlfile.write(insert_stmnt + '\n')

if __name__ == "__main__":
    file_path = 'df_limpio.csv'  # Reemplaza con la ruta a tu archivo CSV
    output_sql_file = 'diagnosticos.sql'
    convert_to_postgre_sql_insert(file_path, output_sql_file)
    print("Datos cargados con éxito")