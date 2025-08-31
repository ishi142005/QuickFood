import pandas as pd
from collections import Counter
import re

# Load dataset
df = pd.read_csv("dataset/recipes.csv")

print("Columns in dataset:", df.columns.tolist())
print("First few rows of dataset:")
print(df.head())

# Check ingredients column
sample = df["ingredients"].head(3).to_list()
print("\nSample ingredients column values:")
for s in sample:
    print(s)

# Function to normalize ingredient text
def normalize(ing):
    ing = ing.lower().strip()
    ing = re.sub(r"[^a-zA-Z\s]", "", ing)  # remove numbers, fractions, punctuation
    return ing.strip()

all_ingredients = []

for row in df["ingredients"].dropna():
    # Split the long string into individual ingredients
    items = row.split(",")
    for item in items:
        norm = normalize(item)
        if norm:
            all_ingredients.append(norm)

# Count frequency
counter = Counter(all_ingredients)

print("\n🔹 Top 20 distinct normalized ingredients:")
for ing, count in counter.most_common(20):
    print(f"{ing}: {count}")
