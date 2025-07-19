from django.db import migrations
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def forward_migration(apps, schema_editor):
    DietaryPreference = apps.get_model('nutrition', 'DietaryPreference')
    

    for pref in DietaryPreference.objects.exclude(excluded_ingredients__isnull=True):
        try:
            data = json.loads(pref.excluded_ingredients)
            if isinstance(data, list) and len(data) == 1:
                pref.excluded_ingredients = json.dumps(data[0])
                pref.save()
                logger.info(f"Updated excluded_ingredients for DietaryPreference id={pref.id}")
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Skipped excluded_ingredients for id={pref.id}: {str(e)}")
    
  
    for pref in DietaryPreference.objects.exclude(favorite_cuisines__isnull=True):
        try:
            data = json.loads(pref.favorite_cuisines)
            if isinstance(data, list) and len(data) == 1:
                pref.favorite_cuisines = json.dumps(data[0])
                pref.save()
                logger.info(f"Updated favorite_cuisines for DietaryPreference id={pref.id}")
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Skipped favorite_cuisines for id={pref.id}: {str(e)}")
    
    for pref in DietaryPreference.objects.exclude(preferred_meal_types__isnull=True):
        try:
            data = json.loads(pref.preferred_meal_types)
            if isinstance(data, list) and len(data) == 1:
                pref.preferred_meal_types = json.dumps(data[0])
                pref.save()
                logger.info(f"Updated preferred_meal_types for DietaryPreference id={pref.id}")
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Skipped preferred_meal_types for id={pref.id}: {str(e)}")

def reverse_migration(apps, schema_editor):
    DietaryPreference = apps.get_model('nutrition', 'DietaryPreference')
 
    for pref in DietaryPreference.objects.exclude(excluded_ingredients__isnull=True):
        try:
            data = json.loads(pref.excluded_ingredients)
            if not isinstance(data, list):
                pref.excluded_ingredients = json.dumps([data])
                pref.save()
                logger.info(f"Reversed excluded_ingredients for DietaryPreference id={pref.id}")
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Skipped excluded_ingredients for id={pref.id}: {str(e)}")
    
    for pref in DietaryPreference.objects.exclude(favorite_cuisines__isnull=True):
        try:
            data = json.loads(pref.favorite_cuisines)
            if not isinstance(data, list):
                pref.favorite_cuisines = json.dumps([data])
                pref.save()
                logger.info(f"Reversed favorite_cuisines for DietaryPreference id={pref.id}")
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Skipped favorite_cuisines for id={pref.id}: {str(e)}")
    
    for pref in DietaryPreference.objects.exclude(preferred_meal_types__isnull=True):
        try:
            data = json.loads(pref.preferred_meal_types)
            if not isinstance(data, list):
                pref.preferred_meal_types = json.dumps([data])
                pref.save()
                logger.info(f"Reversed preferred_meal_types for DietaryPreference id={pref.id}")
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Skipped preferred_meal_types for id={pref.id}: {str(e)}")

class Migration(migrations.Migration):
    dependencies = [
        ('nutrition', '0002_alter_dietarypreference_dietary_type_and_more'),
    ]

    operations = [
        migrations.RunPython(
            code=forward_migration,
            reverse_code=reverse_migration,
        ),
    ]