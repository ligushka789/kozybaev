import joblib
import re
from pathlib import Path

# ===========================
# PATH
# ===========================

MODEL_PATH = Path("ml") / "model.pkl"

# Загружаем pipeline
model = joblib.load(MODEL_PATH)

# ===========================
# TEXT NORMALIZATION (одинаковая как в classifier.py)
# ===========================

def normalize(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# ===========================
# PREDICT
# ===========================

def predict_block(name: str) -> str:
    return model.predict([normalize(name)])[0]

# ===========================
# CLI
# ===========================

if __name__ == "__main__":
    
    print("Type product names, CTRL+C to exit.\n")

    # авто-тест
    tests = [
        "chicken breast",
        "ground beef",
        "milk",
        "yogurt",
        "orange juice",
        "coffee",
        "potato chips",
        "oatmeal",
        "rice",
        "protein bar",
        "soda",
    ]

    for t in tests:
        print(t, "→", predict_block(t))

    print("\nInteractive mode:")

    while True:
        x = input("Product name: ")
        print("→", predict_block(x))
