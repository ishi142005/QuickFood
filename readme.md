# 🍽️ Smart Recipe Generator

Smart Recipe Generator is a web-based application that suggests recipes based on ingredients provided by the user. It supports dietary filters, ingredient substitution suggestions, and a mobile-responsive interface — helping users create meals with what they already have.

---

## 🔗 Live Demo

👉 [Click here to view the live site](https://your-app-url.onrender.com)

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default)
- **Hosting**: Render (Free Tier)
- **Image Recognition (optional)**: Teachable Machine / Clarifai / dummy image mapping
- **Static Files**: WhiteNoise for production

---

## ✨ Features

- ✅ Text-based ingredient input
- ✅ Optionally recognize ingredients from uploaded images
- ✅ Dietary filters: vegetarian, gluten-free, etc.
- ✅ Recipe suggestions with:
  - Steps
  - Serving sizes
  - Nutritional info (e.g., calories, protein)
- ✅ Filter by difficulty, time, and servings
- ✅ Substitution suggestions for missing ingredients
- ✅ User ratings and ability to save favorites
- ✅ Fully mobile-responsive UI
- ✅ Deployed on a live server

---

## ⚙️ How It Works

1. Users enter ingredients (text or image).
2. A matching algorithm compares input to recipes in the database using text similarity.
3. Filters narrow down results based on dietary preferences and difficulty.
4. Substitution logic offers alternatives if ingredients are missing.
5. Recipes are displayed with steps, nutrition, and an option to save/rate.

---

## 📂 Installation (Local Development)

```bash
git clone https://github.com/yourusername/smart-recipe-generator.git
cd smart-recipe-generator
python -m venv new_env
source new_env/Scripts/activate  # On Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
