from  django.db import  models
from django.contrib.postgres.fields import ArrayField
from users.models import Customer



class DietaryPreference(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    dietary_type = models.CharField(max_length=50)
    excluded_ingredients = ArrayField(
        models.TextField(),
        blank=True,
        default=list,
        null=True
    )
    favorite_cuisines = ArrayField(
        models.TextField(),
        blank=True,
        default=list,
        null=True
    )
    preferred_meal_types = ArrayField(
        models.TextField(),
        blank=True,
        default=list,
        null=True
    )
    nutritional_goal = models.CharField(max_length=50)
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














