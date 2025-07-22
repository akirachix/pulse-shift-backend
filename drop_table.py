import os
import django
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pulse_shift_backend.settings")
django.setup()

with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS nutrition_dietarypreference")
print("Dropped nutrition_dietarypreference table.")
