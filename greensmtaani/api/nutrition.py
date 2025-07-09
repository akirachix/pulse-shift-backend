import os
import requests
import time
import django
import sys
from dotenv import load_dotenv
from datetime import datetime,timedelta
from django.utils import timezone
from django.utils.html import strip_tags  # to fix HTML codes and retrieve empty if the recipe doesn't have summary in that api
from nutrition.models import Recipe, Ingredient,FetchHistory  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greensmtaani.settings') 
sys.path.append('/home/student/backend/project/pulse-shift-backend/greensmtaani') # adds our project root to python's module search path
django.setup() 
import logging
logger = logging.getLogger(__name__)
load_dotenv()




# Access our environment variables
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = 'https://api.spoonacular.com/recipes/complexSearch'


def get_last_month_date():   # Returns the datetime for the first day of the previous month .
    
    now=timezone.now()
    first_day_this_month=now.replace(day=1)
    last_month=first_day_this_month-timedelta(days=1)
    return last_month.replace(day=1)
def get_last_fetch_offset():

    try:
        history = FetchHistory.objects.get(api_name='spoonacular')
        return history.last_offset
    except FetchHistory.DoesNotExist:
        return 0


def update_fetch_progress(offset): #Update record with current datetime and offset.
   
    FetchHistory.objects.update_or_create(
        api_name='spoonacular',
        defaults={
            'last_fetch': timezone.now(),
            'last_offset': offset
        }
    )
def sanitize_text(text):
    if not text:
        return ''
    return strip_tags(text).strip()



def fetch_recipes_from_api(ingredients_list, number=100, offset=0, min_date=None):  #Fetch recipes from Spoonacular API that include any of the specified ingredients. Supports pagination via offset.
   
    if not SPOONACULAR_API_KEY:
        raise ValueError("Spoonacular API key not set in environment variables.")

    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'includeIngredients': ','.join(ingredients_list),
        'number': number,
        'offset': offset,
        'addRecipeInformation': True,
        'fillIngredients': True,
        'instructionsRequired': True,
        'sort': 'popularity',
    }
    if min_date:
        params['minDate'] = min_date.strftime('%y-%m-%d')

    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data.get('results', [])





def save_recipes(recipes_data, min_date=None):  # Save new recipes and their ingredients to the database. Avoid duplicates by checking spoonacular_id. Returns the count of new recipes saved.
  
    new_count = 0

    for data in recipes_data:
        if Recipe.objects.filter(spoonacular_id=data['id']).exists():
            continue

        ingredients_objs = []
        for ing in data.get('extendedIngredients', []):
            ingredient_name = ing['name'].strip().lower()  # Normalize ingredient name
            ingredient_obj, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            ingredients_objs.append(ingredient_obj)

        # Sanitize the summary and instructions for the recipes before saving
        summary = sanitize_text(data.get('summary'))
        instructions = sanitize_text(data.get('instructions'))

        recipe = Recipe.objects.create(
            spoonacular_id=data['id'],
            title=data['title'],
            image_url=data.get('image'),
            summary=summary,
            instructions=instructions,
            source_url=data.get('sourceUrl'),
        )
        recipe.ingredients.set(ingredients_objs)
        recipe.save()

        new_count += 1

    return new_count


def fetch_and_save_monthly_new_recipes(): # Fetches up to 15,000 new recipes in batches of 100, only for the current month.
   
    ingredients = ['vegetables', 'fruits']  # Customize our ingredient filter here
    batch_size = 100  # Max recipes per request allowed by Spoonacular
    max_batches=150   # allow 150 request per day
    total_to_fetch=batch_size * max_batches
    all_recipes = []
    offset = 0  # always start from 0 for monthly fetch
    min_date=get_last_month_date() # calculate the first day of the previous month

    logger.info(f"Starting paginated fetch from Spoonacular API from offset {offset}, since {min_date}...")
    for batch in range(max_batches):
        try:
            recipes = fetch_recipes_from_api(ingredients, number=batch_size, offset=offset, min_date=min_date)
        except requests.RequestException as e:
            logger.error(f"API request failed at offset {offset}: {e}")
            break

        if not recipes:
            logger.info("No more recipes returned by API.")
            break

        all_recipes.extend(recipes)
        offset += batch_size
        update_fetch_progress(offset)
        time.sleep(1)  # Avoid API rate limits

        logger.info(f"Fetched {len(recipes)} recipes, total fetched so far: {len(all_recipes)}")
        if len(all_recipes)>=total_to_fetch:
            break

    new_recipes_count = save_recipes(all_recipes, min_date=min_date)
    logger.info(f"Saved {new_recipes_count} new recipes to the database.")

    return new_recipes_count



if __name__ == "__main__":

    count = fetch_and_save_new_recipes()
    print(f"Total new recipes saved: {count}")
