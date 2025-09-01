from django.shortcuts import render, redirect
from django import forms
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import Recipe
from django.conf import settings
from rapidfuzz import fuzz, process
import json
import ast
import re
import os

from .ml_model import predict_ingredients

def clear_pantry(request):
    request.session.pop('pantry', None)
    return redirect('home')

def normalize(text):
    """Lowercase, remove numbers, units, and punctuation"""
    text = text.lower()
    text = re.sub(r'\b(cup|cups|teaspoon|teaspoons|tablespoon|tablespoons|ounce|ounces|lb|lbs|gram|g|kg)\b', '', text)
    text = re.sub(r'\d+(/\d+)?', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def is_match(pantry, ingredient, threshold=80):
    ingredient_norm = normalize(ingredient)
    pantry_norm = [normalize(p) for p in pantry]
    best_match, score, _ = process.extractOne(ingredient_norm, pantry_norm, scorer=fuzz.token_sort_ratio)
    return score >= threshold

def categorize_pantry(pantry_items):
    categories = {
        'baking essentials': ['sugar','butter','flour','eggs','milk','vanilla','baking powder','baking soda'],
        'spices & flavoring': ['cinnamon','nutmeg','salt','cloves'],
        'fruits & nuts': ['apple','banana','walnuts','raisins','orange'],
        'dairy': ['cream','yogurt','cheese'],
        'others': []
    }
    categorized_items = {key: [] for key in categories}
    for item in pantry_items:
        added = False
        item_lower = item.lower()
        for category, items in categories.items():
            if any(ingredient in item_lower for ingredient in items):
                categorized_items[category].append(item)
                added = True
                break
        if not added:
            categorized_items['others'].append(item)
    return categorized_items

class IngredientImageForm(forms.Form):
    image = forms.ImageField()

def home(request):
    pantry_items = request.session.get('pantry', [])
    pantry_categories = categorize_pantry(pantry_items)
    return render(request, 'quickfood/home.html', {'pantry': pantry_categories})

def add_to_pantry(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pantry = request.session.get('pantry', [])
        for ing in data.get('ingredient', []):
            ing = ing.strip()
            if ing and ing.lower() not in [x.lower() for x in pantry]:
                pantry.append(ing)
        request.session['pantry'] = pantry
        return JsonResponse({'success': True})

def remove_from_pantry(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pantry = request.session.get('pantry', [])
        pantry_lower = [x.lower() for x in pantry]
        if data['ingredient'].lower() in pantry_lower:
            pantry.pop(pantry_lower.index(data['ingredient'].lower()))
        request.session['pantry'] = pantry
        return JsonResponse({'success': True})

def get_recipes(request):
    pantry_items = request.session.get('pantry', [])
    if not pantry_items:
        return render(request, 'quickfood/results.html', {
            'recipes': [],
            'message': "Your pantry is empty. Please add ingredients.",
            'pantry': categorize_pantry(pantry_items)
        })

    recipes = Recipe.objects.all()
    matched_recipes = []

    pantry_norm = [normalize(p) for p in pantry_items]

    for recipe in recipes:
        # Parse ingredients
        if isinstance(recipe.ingredients, list):
            recipe_ings = recipe.ingredients
        else:
            try:
                recipe_ings = ast.literal_eval(recipe.ingredients)
                if not isinstance(recipe_ings, list):
                    recipe_ings = []
            except:
                recipe_ings = []

        recipe_ings = [normalize(i) for i in recipe_ings if isinstance(i, str) and i.strip()]

        if not recipe_ings:
            continue

        # Check if any ingredient matches pantry
        recipe_matches = any(
            normalize(p) in normalize(r_ing) or normalize(r_ing) in normalize(p)
            for r_ing in recipe_ings
            for p in pantry_items
        )
        if recipe_matches:
            recipe.ingredient_list = [i.strip() for i in recipe_ings]
            recipe.direction_list = [d.strip() for d in str(recipe.directions).split(".") if d.strip()]
            matched_recipes.append(recipe)

    message = "No recipes match your pantry items." if not matched_recipes else ""
    return render(request, 'quickfood/results.html', {
        'recipes': matched_recipes,
        'pantry': categorize_pantry(pantry_items),
        'message': message
    })


def upload_ingredient(request):
    from .ml_model import predict_ingredients
    if request.method == "POST":
        form = IngredientImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # save in media/
            filename = fs.save(img.name, img)
            file_path = fs.path(filename)

            # Predict ingredient
            detected_ingredients = predict_ingredients(file_path)

            # Add detected ingredient to pantry
            pantry = request.session.get('pantry', [])
            for item in detected_ingredients:
                if item.lower() not in [x.lower() for x in pantry]:
                    pantry.append(item)
            request.session['pantry'] = pantry

            # Delete the uploaded image immediately
            os.remove(file_path)

            return redirect('home')
    else:
        form = IngredientImageForm()
    return render(request, 'quickfood/upload.html', {'form': form})
