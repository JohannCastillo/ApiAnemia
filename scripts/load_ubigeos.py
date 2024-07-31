import csv
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiAnemia.settings')
django.setup()

from api.models import Departamento, Provincia, Distrito

def load_data_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            departamento_nombre = row['DepartamentoREN']
            provincia_nombre = row['ProvinciaREN']
            distrito_nombre = row['DistritoREN']

            # Obtener o crear el departamento
            departamento, created = Departamento.objects.get_or_create(departamento=departamento_nombre)

            # Obtener o crear la provincia
            provincia, created = Provincia.objects.get_or_create(provincia=provincia_nombre, departamento=departamento)

            # Obtener o crear el distrito
            distrito, created = Distrito.objects.get_or_create(distrito=distrito_nombre, provincia=provincia)

            print(f"Departamento: {departamento.departamento}, Provincia: {provincia.provincia}, Distrito: {distrito.distrito}")

if __name__ == "__main__":
    file_path = 'ubigeos.csv'  # Reemplaza con la ruta a tu archivo CSV
    # Limpiar departamentos que ya existan
    Departamento.objects.all().delete()
    load_data_from_csv(file_path)
    print("Datos cargados con éxito")