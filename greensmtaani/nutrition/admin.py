from django.contrib import admin

from .models import  DietaryPreference,MealPlan,Recipe,Ingredient,FetchHistory
admin.site.register(MealPlan)
admin.site.register(DietaryPreference)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(FetchHistory)


# Register your models here.
