

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0001_initial'),
    ]

    operations = [

        migrations.AlterField(
            model_name='DietaryPreference',
            name='dietary_type',
            field=models.CharField(choices=[('VEGAN', 'Vegan'), ('KETO', 'Keto'), ('Paleo', 'Paleo'), ('GLUTEN_FREE', 'Gluten-Free'), ('DAIRY_FREE', 'Dairy-Free'), ('OTHER', 'Other')], max_length=50),
        ),

        migrations.AlterField(
            model_name='DietaryPreference',
            name='nutritional_goal',
            field=models.CharField(choices=[('WEIGHT_LOSS', 'Weight Loss'), ('MUSCLE_GAIN', 'Muscle Gain'), ('MAINTENANCE', 'Maintenance'), ('HEALTHY_EATING', 'Healthy Eating')], max_length=50),
        ),

        migrations.AddField(
            model_name='DietaryPreference',
            name='temp_excluded_ingredients',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='DietaryPreference',
            name='temp_favorite_cuisines',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='DietaryPreference',
            name='temp_preferred_meal_types',
            field=models.JSONField(blank=True, default=list, null=True),
        ),

        migrations.RunSQL(
            sql="""
            UPDATE nutrition_dietarypreference
            SET temp_excluded_ingredients = (
                CASE
                    WHEN excluded_ingredients IS NOT NULL AND excluded_ingredients != ''
                    THEN json_array(excluded_ingredients)
                    ELSE json_array()
                END
            );

            UPDATE nutrition_dietarypreference
            SET temp_favorite_cuisines = (
                CASE
                    WHEN favorite_cuisines IS NOT NULL AND favorite_cuisines != ''
                    THEN json_array(favorite_cuisines)
                    ELSE json_array()
                END
            );

            UPDATE nutrition_dietarypreference
            SET temp_preferred_meal_types = (
                CASE
                    WHEN preferred_meal_types IS NOT NULL AND preferred_meal_types != ''
                    THEN json_array(preferred_meal_types)
                    ELSE json_array()
                END
            );
            """,
            reverse_sql="""
            UPDATE nutrition_dietarypreference
            SET excluded_ingredients = (
                SELECT json_group_array(value) FROM json_each(temp_excluded_ingredients)
            )
            WHERE temp_excluded_ingredients IS NOT NULL;

            UPDATE nutrition_dietarypreference
            SET favorite_cuisines = (
                SELECT json_group_array(value) FROM json_each(temp_favorite_cuisines)
            )
            WHERE temp_favorite_cuisines IS NOT NULL;

            UPDATE nutrition_dietarypreference
            SET preferred_meal_types = (
                SELECT json_group_array(value) FROM json_each(temp_preferred_meal_types)
            )
            WHERE temp_preferred_meal_types IS NOT NULL;
            """
        ),

        migrations.RemoveField(
            model_name='DietaryPreference',
            name='excluded_ingredients',
        ),
        migrations.RemoveField(
            model_name='DietaryPreference',
            name='favorite_cuisines',
        ),
        migrations.RemoveField(
            model_name='DietaryPreference',
            name='preferred_meal_types',
        ),

        migrations.RenameField(
            model_name='DietaryPreference',
            old_name='temp_excluded_ingredients',
            new_name='excluded_ingredients',
        ),
        migrations.RenameField(
            model_name='DietaryPreference',
            old_name='temp_favorite_cuisines',
            new_name='favorite_cuisines',
        ),
        migrations.RenameField(
            model_name='DietaryPreference',
            old_name='temp_preferred_meal_types',
            new_name='preferred_meal_types',
        ),
    ]