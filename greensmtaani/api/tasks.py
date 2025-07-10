from .nutrition import fetch_and_save_monthly_new_recipes

def fetch_monthly_recipes_task():
    count = fetch_and_save_monthly_new_recipes()
    print(f"Total new recipes saved: {count}")