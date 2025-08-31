import os
import json
from django.core.management.base import BaseCommand
from QuickFood.models import Recipe

def parse_time(value):
    """
    Convert strings like '1 hr 30 mins' or '10 mins' into integer minutes.
    """
    if isinstance(value, int):
        return value
    if not value:
        return 0

    value = str(value).lower()
    minutes = 0

    # Handle hours
    if "hr" in value:
        hr_part = ''.join(filter(str.isdigit, value.split('hr')[0]))
        if hr_part.isdigit():
            minutes += int(hr_part) * 60
        value = value.split('hr')[1]  # remaining part after hours

    # Handle minutes
    if "min" in value:
        min_part = ''.join(filter(str.isdigit, value))
        if min_part.isdigit():
            minutes += int(min_part)

    return minutes

class Command(BaseCommand):
    help = 'Loads recipes from mini_recipes.json into the database'

    def handle(self, *args, **options):
        # Project root (Recipe Recommendation)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        JSON_PATH = os.path.join(BASE_DIR, "dataset", "mini_recipes.json")

        if not os.path.exists(JSON_PATH):
            self.stderr.write(self.style.ERROR(f"JSON file not found at {JSON_PATH}"))
            return

        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            recipes_data = json.load(f)

        self.stdout.write(self.style.SUCCESS(f"Loading {len(recipes_data)} recipes from {JSON_PATH}"))

        Recipe.objects.all().delete()  # Clear existing recipes

        for item in recipes_data:
            # Ingredients
            ingredients_list = item.get('ingredients', [])
            if isinstance(ingredients_list, str):
                ingredients_list = [i.strip() for i in ingredients_list.split(',') if i.strip()]

            # Directions
            directions_list = item.get('directions', ["No steps provided."])
            if isinstance(directions_list, str):
                directions_list = [d.strip() for d in directions_list.split('.') if d.strip()]

            Recipe.objects.create(
                recipe_name=item.get('recipe_name', 'Unknown Recipe'),
                prep_time=parse_time(item.get('prep_time', 0)),
                cook_time=parse_time(item.get('cook_time', 0)),
                total_time=parse_time(item.get('total_time', 0)),
                servings=item.get('servings', 1),
                ingredients=ingredients_list,
                directions=". ".join(directions_list),
                image=item.get('image', ''),
                rating=item.get('rating', 0.0),
                url=item.get('url', ''),
                cuisine_path=item.get('cuisine_path', ''),
                nutrition=item.get('nutrition', {}),
                timing=item.get('timing', {})
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded recipes!'))
