import pandas as pd
import joblib
import re
import random
from pathlib import Path
import streamlit as st

# ===========================
# PATHS
# ===========================

DATASET_PATH = Path("datasets/walmart.csv")
MODEL_PATH = Path("ml/model.pkl")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# ===========================
# CONFIG
# ===========================

BLOCK_SIZES = {
    "protein": 4,
    "side": 4,
    "breakfast": 3,
    "snack": 3,
    "drink": 2
}

IGNORE_BLOCK = "ignore"

IGNORE_CATEGORIES = [
    "Herbs, spices & seasonings", "Condiments",
    "Fresh Dressings", "Oils & Shortening",
    "Cooking oils & vinegars", "Sugars & Sweeteners",
    "Yeast", "Baking Soda & Starch"
]

MAX_AMT = 5000
CANDIDATE_WINDOW = 50

SIDE_BANNED_KEYWORDS = [
    "sauce", "marinade", "gravy", "dressing",
    "alfredo", "pesto", "dip", "topping"
]

# ===========================
# NORMALIZE
# ===========================

def normalize(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def predict_block(name: str) -> str:
    return model.predict([normalize(name)])[0]

# ===========================
# LOAD DATA
# ===========================

@st.cache_data
def load_dataset():
    df = pd.read_csv("datasets/walmart.csv")

    df = df[df["price"] > 0]
    df = df[df["amt"].notna()]
    df = df[df["unit"].notna()]
    df = df[df["amt"] <= MAX_AMT]
    df = df[~df["category"].isin(IGNORE_CATEGORIES)]

    if "product_url" in df.columns:
        df = df.drop_duplicates("product_url")
    else:
        df = df.drop_duplicates("product_name")

    df["unit_price"] = df["price"] / df["amt"]

    print("Classifying with ML...")
    texts = df["product_name"].astype(str).apply(normalize).tolist()
    df["ml_block"] = model.predict(texts)

    df = df[df["ml_block"] != IGNORE_BLOCK]
    df = df.drop_duplicates(subset="product_name")

    return df

# ===========================
# SELECTORS
# ===========================

def rand_from_top(df, k):
    if len(df) <= k:
        return df
    window = df.head(CANDIDATE_WINDOW)
    return window.sample(min(k, len(window)))

def filter_sides(df):
    return df[~df["product_name"].str.lower().str.contains("|".join(SIDE_BANNED_KEYWORDS), na=False)]

def select_block(df, block, k):
    pool = df[df["ml_block"] == block].sort_values("unit_price")

    if block == "side":
        pool = filter_sides(pool)

    return rand_from_top(pool, k)

def fallback(df, k):
    return rand_from_top(df.sort_values("unit_price"), k)

# ===========================
# MAIN
# ===========================

def generate_meal_plan():

    df = load_dataset()
    selected = []

    for block, k in BLOCK_SIZES.items():

        part = select_block(df, block, k)

        if len(part) < k:
            need = k - len(part)
            extra = fallback(df, need)
            part = pd.concat([part, extra])

        part["block"] = block
        selected.append(part)

        result = pd.concat(selected, ignore_index=True)
        result = result.drop_duplicates("product_name")

        # добиваем недостающие уникальные
        while len(result) < 16:
            extra = df.sample(1)
            result = pd.concat([result, extra])
            result = result.drop_duplicates("product_name")


    return result[[
        "block","category","subcategory",
        "product_name","price",
        "amt","unit","unit_price",
        "product_url"
    ]]

# ===========================
# CLI
# ===========================

if __name__ == "__main__":
    plan = generate_meal_plan()
    print(plan)
    print("TOTAL:", len(plan))
