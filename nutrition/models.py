from  django.db import  models
from django.contrib.postgres.fields import ArrayField
from users.models import Customer


class DietaryPreference(models.Model):
    DIETARY_TYPES = [
        ('VEGAN', 'Vegan'),
        ('KETO', 'Keto'),
        ('PALEO', 'Paleo'),
        ('GLUTEN_FREE', 'Gluten-Free'),
        ('DAIRY_FREE', 'Dairy-Free'),
        ('OTHER', 'Other'),
    ]

    NUTRITIONAL_GOALS = [
        ('WEIGHT_LOSS', 'Weight Loss'),
        ('MUSCLE_GAIN', 'Muscle Gain'),
        ('MAINTENANCE', 'Maintenance'),
        ('HEALTHY_EATING', 'Healthy Eating'),
    ]

    customer = models.ForeignKey('users.Customer', on_delete=models.CASCADE, null=True, blank=True)
    dietary_type = models.CharField(max_length=50, choices=DIETARY_TYPES)
    excluded_ingredients = models.JSONField(  
        default=list,
        blank=True,
        null=True
    )
    favorite_cuisines = models.JSONField( 
        default=list,
        blank=True,
        null=True
    )
    preferred_meal_types = models.JSONField( 
        default=list,
        blank=True,
        null=True
    )
    nutritional_goal = models.CharField(max_length=50, choices=NUTRITIONAL_GOALS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.dietary_type}"

    
class MealPlan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    base_preference = models.ForeignKey(
        DietaryPreference,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.customer})"
    
class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    spoonacular_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    ready_in_minutes = models.IntegerField(null=True, blank=True)
    servings = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class FetchHistory(models.Model):
    api_name = models.CharField(max_length=100, unique=True)
    last_fetch = models.DateTimeField()
    last_offset = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.api_name} last fetched at {self.last_fetch} with offset {self.last_offset}"














