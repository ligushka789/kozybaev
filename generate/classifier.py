import pandas as pd
import joblib
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

print(">>> classifier.py started")

# ===========================
# PATHS
# ===========================

BASE_DIR = Path("generate/ml_datasets")
ML_DIR = Path("ml")
ML_DIR.mkdir(exist_ok=True)

MODEL_PATH = ML_DIR / "model.pkl"

# ===========================
# NORMALIZATION
# ===========================

def normalize(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# ===========================
# LOAD DATASETS
# ===========================

def load_training_data():

    datasets = {
        "protein":   BASE_DIR / "protein.csv",
        "side":      BASE_DIR / "side.csv",
        "breakfast": BASE_DIR / "breakfast.csv",
        "snack":     BASE_DIR / "snack.csv",
        "drink":     BASE_DIR / "drink.csv",
        "ignore":    BASE_DIR / "ignore.csv",
    }

    frames = []

    for label, path in datasets.items():
        if not path.exists():
            raise FileNotFoundError(f"❌ Missing: {path}")

        df = pd.read_csv(path)

        if "product_name" not in df.columns:
            raise ValueError(f"❌ 'product_name' not found in {path.name}")

        df = df[["product_name"]].dropna()
        df["true_block"] = label
        frames.append(df)

    data = pd.concat(frames, ignore_index=True)
    data["text"] = data["product_name"].apply(normalize)

    return data[["text", "true_block"]]

# ===========================
# TRAIN
# ===========================

def train():

    print("➡️ Loading datasets...")
    data = load_training_data()

    X = data["text"]
    y = data["true_block"]

    print("➡️ Building pipeline...")

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1,2),
            min_df=5,
            max_df=0.9,
            stop_words="english",
            sublinear_tf=True
        )),
        ("clf", LogisticRegression(max_iter=3000, n_jobs=-1))
    ])

    print("➡️ Training model...")
    pipeline.fit(X, y)

    print("✅ Saving model...")
    joblib.dump(pipeline, MODEL_PATH)

    print("✅ TRAINING COMPLETE")
    print("Saved to:", MODEL_PATH)
    print("Classes:", pipeline.classes_)

if __name__ == "__main__":
    train()
