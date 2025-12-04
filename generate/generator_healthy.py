import pandas as pd
import joblib
import random
import re
from pathlib import Path

# ===========================
# PATHS
# ===========================
DATASET_PATH = Path("datasets/walmart_scored.csv")
MODEL_PATH   = Path("ml/model.pkl")

# ===========================
# LOAD MODEL
# ===========================
model = joblib.load(MODEL_PATH)

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

BANNED_KEYWORDS = [
    "soda", "candy", "syrup", "chips", "instant",
    "energy drink", "fruit snacks", "gummies", "chewy"
]

SNACK_BAN = [
    "candy","chocolate","cookie","brownie",
    "cake","chip","crisps","puff","fried","snack"
]

# ===========================
# NORMALIZE
# ===========================

def normalize(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# ===========================
# LOAD DATA
# ===========================

def load_dataset():
    df = pd.read_csv(DATASET_PATH)
    df = df[df["price"].notna()]
    df = df[df["product_name"].notna()]
    df = df[df["healthy_flag"].notna()]
    return df

# ===========================
# HEALTH SCORE
# ===========================

def compute_health_score(row):

    name = row["product_name"].lower()
    block = row["ml_block"]
    score = 0

    # unhealthy => DROP
    if row["healthy_flag"] == "unhealthy":
        return -999

    # healthy boost
    if row["healthy_flag"] == "healthy":
        score += 3

    # trusted bonus
    if row.get("trusted_brand", False):
        score += 2

    # allergen penalty
    if row.get("allergen_any", False):
        score -= 2

    # spam/musor filter
    for kw in BANNED_KEYWORDS:
        if kw in name:
            return -999

    # mistakes protections
    if block == "drink" and "tuna" in name:
        return -999

    return score

# ===========================
# SNACK FILTER
# ===========================

def snack_filter(df):

    def ok(name):
        n = name.lower()
        for bad in SNACK_BAN:
            if bad in n:
                return False
        return True

    return df[df["product_name"].apply(ok)]

# ===========================
# VALIDATE BLOCK
# ===========================

def validate_block(block, name):
    n = name.lower()

    # --- PROTEIN (ЖЁСТКО) ---
    if block == "protein":

        # ❌ Фрукты / овощи / бобы / зерно / сладкое — убрать из protein
        if any(x in n for x in [
            "strawberry","blueberry","apple","banana","fruit",
            "beans","bean","lentil","pea","vegetable","veggie",
            "corn","carrot","broccoli","rice","oat","grain",
            "bread","cereal","pasta","burrito","tortilla",
            "sugar","sweet","chocolate","cookie","bar"
        ]):
            return False

        # ✅ Protein ТОЛЬКО если есть явный признак:
        if not any(x in n for x in [
            "chicken","beef","pork","turkey","fish","salmon",
            "tuna","egg","eggs","yogurt","tofu","protein",
            "steak","meat","burger","jerky"
        ]):
            return False

    # --- DRINK ---
    if block == "drink":
        if any(f in n for f in ["burger","chicken","meat","tuna","egg","beans"]):
            return False

    return True

# ===========================
# SELECT BLOCK
# ===========================

def select_block(df, block, k):

    pool = df[df["ml_block"] == block]

    if block == "snack":
        pool = snack_filter(pool)

    # ✅ Block validation — ДО сортировки и window
    pool = pool[pool["product_name"].apply(
        lambda x: validate_block(block, x)
    )]

    # fallback если блок пустой
    if len(pool) == 0:
        print(f"⚠️ EMPTY BLOCK {block} → fallback to global healthy")
        pool = df.copy()

    pool = pool.sort_values("health_score", ascending=False)
    window = pool.head(75)

    return window.sample(min(k, len(window)), random_state=random.randint(0, 99999))

# ===========================
# GENERATOR
# ===========================

def generate_healthy_plan():

    df = load_dataset()

    # base filter
    df = df[df["ml_block"] != IGNORE_BLOCK]
    df = df[df["health_score"] > 0]

    print("✅ After filtering:", len(df))

    selected = []

    for block, k in BLOCK_SIZES.items():
        part = select_block(df, block, k)
        part["block"] = block
        selected.append(part)

    result = pd.concat(selected).drop_duplicates("product_name")

    # добиваем до 16 если не хватает
    while len(result) < 16:
        extra = df.sample(1)
        result = pd.concat([result, extra]).drop_duplicates("product_name")

    return result[[
        "block","category","subcategory",
        "product_name","price",
        "amt","unit",
        "healthy_flag","allergen_any","trusted_brand",
        "health_score","product_url"
    ]]

# ===========================
# CLI
# ===========================

if __name__ == "__main__":

    plan = generate_healthy_plan()

    print("\n=== ✅ HEALTHY MEAL PLAN ===\n")
    print(plan.to_string(index=False))
    print("\nTOTAL:", len(plan))
