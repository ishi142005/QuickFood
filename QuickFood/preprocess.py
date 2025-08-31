import pandas as pd
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "recipes.csv")
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_recipe.csv")
MINI_CSV_PATH = os.path.join(BASE_DIR, "dataset", "mini_recipes.csv")
MINI_JSON_PATH = os.path.join(BASE_DIR, "dataset", "mini_recipes.json")

# Check dataset exists
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

# Load dataset
df = pd.read_csv(DATA_PATH)

# Fill missing values
df = df.fillna("")

# Convert string fields to JSON-friendly formats
def parse_ingredients(text):
    if not text:
        return []
    return [i.strip() for i in text.split(",")]

def parse_directions(text):
    if not text:
        return ["No steps provided."]
    return [step.strip() for step in text.split(".") if step.strip()]

def parse_nutrition(text):
    if not text:
        return {}
    try:
        items = [i.strip() for i in text.split(",")]
        return {kv.split(" ")[0]: " ".join(kv.split(" ")[1:]) for kv in items if " " in kv}
    except:
        return {}

# Apply transformations
df["ingredients"] = df["ingredients"].apply(parse_ingredients)
df["directions"] = df["directions"].apply(parse_directions)
df["nutrition"] = df["nutrition"].apply(parse_nutrition)

# Save full cleaned dataset
df.to_csv(CLEANED_DATA_PATH, index=False)

# Create smaller version (20 recipes)
mini_df = df.sample(n=20, random_state=42)
mini_df.to_csv(MINI_CSV_PATH, index=False)
mini_df.to_json(MINI_JSON_PATH, orient="records", indent=2)

print("✅ Full dataset saved as 'cleaned_recipe.csv'")
print("✅ Mini dataset (20 recipes) saved as 'mini_recipes.csv' and 'mini_recipes.json'")
import pandas as pd
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "recipes.csv")
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_recipe.csv")
MINI_CSV_PATH = os.path.join(BASE_DIR, "dataset", "mini_recipes.csv")
MINI_JSON_PATH = os.path.join(BASE_DIR, "dataset", "mini_recipes.json")

# Check dataset exists
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

# Load dataset
df = pd.read_csv(DATA_PATH)

# Fill missing values
df = df.fillna("")

# Convert string fields to JSON-friendly formats
def parse_ingredients(text):
    if not text:
        return []
    return [i.strip() for i in text.split(",")]

def parse_directions(text):
    if not text:
        return ["No steps provided."]
    return [step.strip() for step in text.split(".") if step.strip()]

def parse_nutrition(text):
    if not text:
        return {}
    try:
        items = [i.strip() for i in text.split(",")]
        return {kv.split(" ")[0]: " ".join(kv.split(" ")[1:]) for kv in items if " " in kv}
    except:
        return {}

# Apply transformations
df["ingredients"] = df["ingredients"].apply(parse_ingredients)
df["directions"] = df["directions"].apply(parse_directions)
df["nutrition"] = df["nutrition"].apply(parse_nutrition)

# Save full cleaned dataset
df.to_csv(CLEANED_DATA_PATH, index=False)

# Create smaller version (20 recipes)
mini_df = df.sample(n=20, random_state=42)
mini_df.to_csv(MINI_CSV_PATH, index=False)
mini_df.to_json(MINI_JSON_PATH, orient="records", indent=2)

print("✅ Full dataset saved as 'cleaned_recipe.csv'")
print("✅ Mini dataset (20 recipes) saved as 'mini_recipes.csv' and 'mini_recipes.json'")
