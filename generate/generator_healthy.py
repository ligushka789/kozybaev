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

    # ❌ DROP UNHEALTHY
    if row["healthy_flag"] == "unhealthy":
        return -999

    # ✅ BASE HEALTH
    if row["healthy_flag"] == "healthy":
        score += 3

    # ✅ TRUSTED BRAND
    if row.get("trusted_brand", False):
        score += 2

    # ❌ ALLERGEN PENALTY
    if row.get("allergen_any", False):
        score -= 2

    # ❌ GREAT VALUE PENALTY (STRONG)
    if "great value" in name:
        score -= 8

    # ✅ PREMIUM / ORGANIC BOOST
    if any(x in name for x in [
        "organic", "wild caught", "grass fed",
        "free range", "no antibiotics",
        "nature valley", "quaker", "oikos", "perdue"
    ]):
        score += 3

    # ❌ SPAM
    for kw in BANNED_KEYWORDS:
        if kw in name:
            return -999

    # ❌ DRINK MISTAKE PROTECTION
    if block == "drink" and any(x in name for x in ["tuna","meat","burger","chicken","egg"]):
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

    # --- PROTEIN ---
    if block == "protein":

        # ❌ NO PLANTS / GRAINS / SUGAR
        if any(x in n for x in [
            "strawberry","blueberry","apple","banana","fruit",
            "beans","bean","lentil","pea",
            "corn","rice","oat","bread","cereal","pasta","tortilla",
            "sugar","cookie","bar","chocolate"
        ]):
            return False

        # ✅ MUST BE REAL PROTEIN
        if not any(x in n for x in [
            "chicken","beef","pork","turkey","salmon","fish","tuna",
            "egg","eggs","yogurt","tofu","steak","meat","jerky","burger"
        ]):
            return False

    # --- DRINK ---
    if block == "drink":
        if any(x in n for x in ["burger","chicken","meat","tuna","egg","beans"]):
            return False

    return True


# ===========================
# SELECT BLOCK
# ===========================

def select_block(df, block, k):

    pool = df[df["ml_block"] == block]

    if block == "snack":
        pool = snack_filter(pool)

    # ✅ BLOCK VALIDATION FIRST
    pool = pool[pool["product_name"].apply(lambda x: validate_block(block, x))]

    # fallback
    if len(pool) == 0:
        print(f"⚠️ EMPTY BLOCK {block} → fallback")
        pool = df.copy()

    # ✅ SORT BY SCORE
    pool = pool.sort_values("health_score", ascending=False)

    # ✅ TAKE BEST POOL
    window = pool.head(75)

    return window.sample(min(k, len(window)), random_state=random.randint(0, 99999))


# ===========================
# GENERATOR
# ===========================

def generate_healthy_plan():

    df = load_dataset()

    # ✅ COMPUTE HEALTH SCORE
    df["health_score"] = df.apply(compute_health_score, axis=1)

    # ✅ BASE FILTER
    df = df[df["ml_block"] != IGNORE_BLOCK]
    df = df[df["health_score"] > 0]

    print("✅ After filtering:", len(df))

    selected = []

    for block, k in BLOCK_SIZES.items():
        part = select_block(df, block, k)
        part["block"] = block
        selected.append(part)

    result = pd.concat(selected).drop_duplicates("product_name")

    # ✅ FILL IF LESS THAN 16
    while len(result) < 16:
        extra = df.sample(1)
        result = pd.concat([result, extra]).drop_duplicates("product_name")

    # ✅ LIMIT GREAT VALUE MAX 2
    gv = result[result["product_name"].str.lower().str.contains("great value")]
    if len(gv) > 2:
        drop = gv.sample(len(gv) - 2)
        result = result.drop(drop.index)
        refill = df[~df["product_name"].str.lower().str.contains("great value")].sample(len(drop))
        result = pd.concat([result, refill])

    # ✅ DEBUG
    print("\n🔥 GREAT VALUE:", len(result[result["product_name"].str.lower().str.contains("great value")]))

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
