#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
# python manage.py collectstatic --no-input

# Apply any outstanding database migrations
# Flush databse
# python manage.py flush --no-input
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser --no-input

# Load ubigeos data only once
python scripts/load_ubigeos.py