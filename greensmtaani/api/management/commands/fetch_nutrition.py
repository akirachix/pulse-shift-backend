from django.core.management.base import BaseCommand
from api.nutrition import fetch_and_save_new_recipes  

class Command(BaseCommand):
    help = 'Fetch and save new recipes from Spoonacular API'

    def handle(self, *args, **kwargs):
        count = fetch_and_save_new_recipes()
        self.stdout.write(self.style.SUCCESS(f'Successfully saved {count} new recipes.'))
