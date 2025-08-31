import re

def preprocess_ingredients(ingredients):
    # Remove special characters and convert to lowercase
    ingredients = re.sub(r'[^\w\s]', '', ingredients.lower())
    # Tokenize by splitting by space or comma
    return ingredients.split()
