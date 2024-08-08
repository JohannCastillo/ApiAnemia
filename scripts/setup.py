"""
Este script hace una carga inicial de los datos
IMPORANTANTE: El script debe ser ejecutado en una instancia de la base de datos sin datos y 
con las tablas creadas por las migraciones al ejecutar 'python manage.py makemigrations' y 'python manage.py migrate'
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiAnemia.settings')
django.setup()

from api.models import Nivel_Anemia, Departamento
from scripts.load_ubigeos import load_data_from_csv


def create_niveles_anemia():
    niveles = [
        'Anemia Severa',
        'Anemia Leve',
        'Anemia Moderada',
        'Normal'
    ]
    for nivel in niveles:
        Nivel_Anemia.objects.create(nivel=nivel)
  
if __name__ == "__main__":
    # Verificar si no se han ejecutados las migraciones
    try:
    # Cargar ubigeos
        print("Cargando ubigeos...")
        load_data_from_csv(file_path='ubigeos.csv')
        print("Ubigeos cargados con éxito")

        # Crear niveles anemia
        print("Creando niveles anemia...")
        create_niveles_anemia()
        print("Niveles anemia creados con éxito")
    except Exception as e:
        print(f"Error: {e}")
        print("Si no se han ejecutado las migraciones, prueba 'python manage.py makemigrations' y 'python manage.py migrate' para corregirlo")
