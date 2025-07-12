
import os
import requests
import time
import django
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.html import strip_tags  
from nutrition.models import Recipe, Ingredient, FetchHistory  
import logging

BASE_DIR = Path(__file__).resolve().parent.parent.parent
logger = logging.getLogger('nutrition')
load_dotenv(dotenv_path=BASE_DIR / '.env')

SPOONACULAR_API_KEY =os.getenv('SPOONACULAR_API_KEY')
logger.info(f"Spoonacular API Key loaded: {'Yes' if SPOONACULAR_API_KEY else 'No'}")
BASE_URL = os.getenv('SPOONACULAR_BASE_URL')


def get_last_fetch_offset():
    try:
        history = FetchHistory.objects.get(api_name='spoonacular')
        return history.last_offset
    except FetchHistory.DoesNotExist:
        return 0


def update_fetch_progress(offset): 
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


def fetch_recipes_from_api(ingredients_list, number=100, offset=0):  
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

    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data.get('results', [])




def get_instructions(data):
    instructions = data.get('instructions')
    if instructions:
        return instructions

    analyzed = data.get('analyzedInstructions', [])
    if analyzed:
        steps = []
        for instruction_set in analyzed:
            for step in instruction_set.get('steps', []):
                step_text = step.get('step', '').strip()
                if step_text:
                    steps.append(step_text)
        return ' '.join(steps)

    return ''  


def save_recipes(recipes_data): 
    new_count = 0

    for data in recipes_data:
        if Recipe.objects.filter(spoonacular_id=data['id']).exists():
            continue

        ingredients_objs = []
        for ing in data.get('extendedIngredients', []):
            ingredient_name = ing['name'].strip().lower() 
            ingredient_obj, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            ingredients_objs.append(ingredient_obj)

        summary = sanitize_text(data.get('summary'))
        instructions = sanitize_text(get_instructions(data))

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

def fetch_and_save_monthly_new_recipes(): 
    ingredients = [] 
    batch_size = 100 
    max_batches = 150  
    total_to_fetch = batch_size * max_batches
    all_recipes = []
    offset = 0 

    logger.info(f"Starting paginated fetch from Spoonacular API from offset {offset}...")
    for batch in range(max_batches):
        try:
            recipes = fetch_recipes_from_api(ingredients, number=batch_size, offset=offset)
        except requests.RequestException as e:
            logger.error(f"API request failed at offset {offset}: {e}")
            break

        if not recipes:
            logger.info("No more recipes returned by API.")
            break

        all_recipes.extend(recipes)
        offset += batch_size
        update_fetch_progress(offset)
        time.sleep(1)  
        logger.info(f"Fetched {len(recipes)} recipes, total fetched so far: {len(all_recipes)}")
        if len(all_recipes) >= total_to_fetch:
            break

    new_recipes_count = save_recipes(all_recipes)
    logger.info(f"Saved {new_recipes_count} new recipes to the database.")

    return new_recipes_count


if __name__ == "__main__":
    count = fetch_and_save_monthly_new_recipes()
    print(f"Total new recipes saved: {count}")
