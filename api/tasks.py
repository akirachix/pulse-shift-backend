from .nutrition import fetch_and_save_monthly_new_recipes
import logging
logger = logging.getLogger('nutrition')
def fetch_monthly_recipes_task():
    count = fetch_and_save_monthly_new_recipes()
    logger.info(f"Total new recipes saved: {count}")
    print(f"Total new recipes saved: {count}")