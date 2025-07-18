from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0002_alter_dietarypreference_dietary_type_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            UPDATE nutrition_dietarypreference
            SET excluded_ingredients = (
                SELECT json_extract(value, '$') 
                FROM json_each(excluded_ingredients)
                WHERE json_array_length(excluded_ingredients) = 1
            )
            WHERE excluded_ingredients IS NOT NULL;

            UPDATE nutrition_dietarypreference
            SET favorite_cuisines = (
                SELECT json_extract(value, '$') 
                FROM json_each(favorite_cuisines)
                WHERE json_array_length(favorite_cuisines) = 1
            )
            WHERE favorite_cuisines IS NOT NULL;

            UPDATE nutrition_dietarypreference
            SET preferred_meal_types = (
                SELECT json_extract(value, '$') 
                FROM json_each(preferred_meal_types)
                WHERE json_array_length(preferred_meal_types) = 1
            )
            WHERE preferred_meal_types IS NOT NULL;
            """,
            reverse_sql="""
            UPDATE nutrition_dietarypreference
            SET excluded_ingredients = json_array(excluded_ingredients)
            WHERE excluded_ingredients IS NOT NULL;

            UPDATE nutrition_dietarypreference
            SET favorite_cuisines = json_array(favorite_cuisines)
            WHERE favorite_cuisines IS NOT NULL;

            UPDATE nutrition_dietarypreference
            SET preferred_meal_types = json_array(preferred_meal_types)
            WHERE preferred_meal_types IS NOT NULL;
            """
        ),
    ]