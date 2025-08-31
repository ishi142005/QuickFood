import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Path to the trained model
MODEL_PATH = r"C:\Users\Ishita\Projects\Recipe Recommendation\QuickFood\QuickFood\ml_models\ingredient_model.h5"
print(MODEL_PATH)
print(os.path.exists(MODEL_PATH))


# Load model once when this module is imported
model = None
class_labels = None

def load_ingredient_model():
    """Load the ingredient classification model and labels."""
    global model, class_labels
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model file not found at: {MODEL_PATH}. Image upload will use fallback.")
        return None
    try:
        model = load_model(MODEL_PATH)

        # Load class labels from training directory structure
        train_dir = os.path.join(os.path.dirname(__file__), "../dataset/train")
        if os.path.exists(train_dir):
            class_labels = sorted(os.listdir(train_dir))  # folder names = labels
        else:
            class_labels = ["unknown"]  # fallback label

        print("✅ Ingredient model loaded successfully!")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model = None
        class_labels = ["unknown"]
        return None

def predict_ingredients(img_path):
    """Take an image file path, return predicted ingredient(s)."""
    global model, class_labels

    if model is None:
        load_ingredient_model()

    if model is None or not os.path.exists(img_path):
        print(f"⚠️ Cannot predict. Model or image missing: {img_path}")
        return ["unknown"]

    try:
        # Preprocess image
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        preds = model.predict(img_array)
        pred_idx = np.argmax(preds[0])
        predicted_label = class_labels[pred_idx] if class_labels else "unknown"
        return [predicted_label]
    except Exception as e:
        print(f"⚠️ Prediction error: {e}")
        return ["unknown"]

# For testing this script directly
if __name__ == "__main__":
    load_ingredient_model()
    test_img = os.path.join(os.path.dirname(__file__), "../dataset/valid/butter/butter_17_jpg.rf.4166c6a4d2dfb83e26469f209c0b8a17.jpg")
    print(predict_ingredients(test_img))
