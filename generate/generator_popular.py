import pandas as pd
import random
from pathlib import Path
import re

# ===========================
# PATH
# ===========================

DATASET_PATH = Path("datasets/walmart_scored.csv")

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

# ===========================
# GLOBAL WORLD BRANDS
# ===========================

WORLD_BRANDS = [
    "coca-cola","sprite","fanta","pepsi","dr pepper","mountain dew",
    "red bull","monster","gatorade","powerade",
    "snickers","twix","kitkat","mars","m&m","hershey","reese",
    "oreo","nutella",
    "pringles","lays","doritos","cheetos","takis","ruffles",
    "ritz","goldfish",
    "kraft","heinz","mccain","nestle","tyson","kellogg","pillsbury",
    "digiorno","totino","red baron",
    "ben & jerry","haagen-dazs","magnum"
]

# ===========================
# ANTI HEALTH WORDS
# ===========================

ANTI_HEALTH = [
    "organic","bio","vegan","plant based","keto","low fat",
    "whole grain","gluten free","sugar free","fitness","protein",
    "healthy","light","zero sugar","natural","diet"
]

GREAT_VALUE = "great value"

POPULAR_SIGNALS = [
    "classic","original","family","party","mega",
    "double","xl","king","cheesy","loaded","extra"
]

# ===========================
# PROTEIN TYPE CONTROL
# ===========================

PROTEIN_TYPES = {
    "pizza": ["pizza"],
    "meat_stick": ["stick", "jerky"],
    "nugget": ["nugget", "tender", "strip", "fries", "patty"],
    "pork": ["pork", "bacon"],
    "burger": ["burger", "sandwich"],
    "sausage": ["sausage", "hot dog", "brat"],
    "chicken": ["chicken"]
}

def get_protein_type(name):
    n = name.lower()
    for key, words in PROTEIN_TYPES.items():
        for w in words:
            if w in n:
                return key
    return "other"

def extract_brand(name):
    for b in WORLD_BRANDS:
        if b in name:
            return b
    return "other"

# ===========================
# BREAKFAST TYPE CONTROL
# ===========================

BREAKFAST_TYPES = {
    "cookie": ["cookie", "dough", "brownie", "frosting"],
    "cereal": ["cereal", "corn flakes", "cheerios"],
    "bread": ["toast", "bread", "bun", "bagel"],
    "waffle": ["waffle", "pancake"],
    "sandwich": ["sandwich", "croissant", "biscuit"],
    "sausage": ["sausage", "bacon"],
    "burger": ["burger"],
    "egg": ["egg"]
}

def get_breakfast_type(name):
    n = name.lower()
    for key, words in BREAKFAST_TYPES.items():
        for w in words:
            if w in n:
                return key
    return "other"

# ===========================
# SNACK TYPES
# ===========================

SNACK_TYPES = {
    "candy": ["snickers","mars","twix","kitkat","m&m","hershey","reese"],
    "chips": ["chips","doritos","lays","pringles","cheetos","takis","ruffles"],
    "cookies": ["cookie","oreo"],
    "crackers": ["ritz","goldfish"],
    "popcorn": ["popcorn"]
}

def get_snack_type(name):
    n = name.lower()
    for key, words in SNACK_TYPES.items():
        for w in words:
            if w in n:
                return key
    return "other"

# ===========================
# LOAD DATA
# ===========================

def load_dataset():
    df = pd.read_csv(DATASET_PATH)
    df = df[df["price"].notna()]
    df = df[df["product_name"].notna()]
    df = df[df["ml_block"] != IGNORE_BLOCK]
    return df

# ===========================
# POPULAR SCORE
# ===========================

def compute_popular_score(row):
    name = row["product_name"].lower()
    block = row["ml_block"]
    score = 0

    for b in WORLD_BRANDS:
        if b in name:
            score += 12

    for s in POPULAR_SIGNALS:
        if s in name:
            score += 2

    for h in ANTI_HEALTH:
        if h in name:
            score -= 6

    if GREAT_VALUE in name:
        score -= 20

    price = row.get("price", 0)
    if 1 <= price <= 15:
        score += 2
    elif price > 25:
        score -= 3

    if block == "protein":
        score += 2
    if block == "drink":
        score += 3
    if block == "snack":
        score += 1

    if any(x in name for x in ["burger","bacon","sausage","chicken","nugget","steak","beef","pork","bbq"]):
        score += 6

    if "pizza" in name:
        score -= 3

    return score

# ===========================
# VALIDATION
# ===========================

def validate_block(block, name):
    n = name.lower()

    if block == "drink" and any(x in n for x in ["pizza","burger","bacon","sausage"]):
        return False

    if block == "protein" and any(x in n for x in ["soda","drink","cookie","candy","chocolate"]):
        return False

    return True

# ===========================
# SELECT BLOCK
# ===========================

def select_block(df, block, k):

    pool = df[df["ml_block"] == block]
    pool = pool[pool["product_name"].apply(lambda x: validate_block(block, x))]
    pool = pool.sort_values("popular_score", ascending=False)
    window = pool.head(120)

    # ==== PROTEIN ====
    if block == "protein":
        selected = []
        used_types = set()
        brand_count = {}

        for _, row in window.iterrows():
            name = row["product_name"].lower()
            ptype = get_protein_type(name)
            brand = extract_brand(name)

            if ptype == "pizza" and "pizza" in used_types:
                continue

            if brand_count.get(brand,0) >= 2:
                continue

            if ptype in used_types:
                continue

            selected.append(row)
            used_types.add(ptype)
            brand_count[brand] = brand_count.get(brand,0)+1

            if len(selected) == k:
                break

        return pd.DataFrame(selected)

    # ==== BREAKFAST ====
    if block == "breakfast":

        selected=[]
        used_types=set()
        cookie_used=False

        PRIORITY = ["cereal","sandwich","waffle","sausage","burger","egg"]
        fallback = []

        for _, row in window.iterrows():
            btype = get_breakfast_type(row["product_name"])

            if btype=="cookie":
                if cookie_used:
                    continue
            else:
                if btype in used_types:
                    continue

            # ✅ СНАЧАЛА ПЫТАЕМСЯ СОБРАТЬ НОРМ ЕДУ
            if btype in PRIORITY:
                selected.append(row)
                used_types.add(btype)
                cookie_used |= (btype=="cookie")
            else:
                fallback.append(row)

            if len(selected)==k:
                return pd.DataFrame(selected)

        # ✅ ЕСЛИ НЕ ХВАТИЛО — ДОБИВАЕМ FALLBACK
        for row in fallback:
            selected.append(row)
            if len(selected)==k:
                break

        return pd.DataFrame(selected)

        # ==== SNACK ====
    if block == "snack":
        selected=[]
        used_types=set()
        candy_count=0

        PRIORITY = ["chips","crackers","popcorn","cookies"]
        fallback = []

        for _, row in window.iterrows():
            stype = get_snack_type(row["product_name"])

            # ❌ максимум 2 candy
            if stype=="candy":
                if candy_count>=2:
                    continue
            else:
                if stype in used_types:
                    continue

            # ✅ сначала норм снеки
            if stype in PRIORITY:
                selected.append(row)
                used_types.add(stype)
            else:
                fallback.append(row)

            if stype=="candy":
                candy_count+=1

            if len(selected)==k:
                return pd.DataFrame(selected)

        # ✅ если не хватило — добиваем чем есть
        for row in fallback:
            selected.append(row)
            if len(selected)==k:
                break

        return pd.DataFrame(selected)
    return window.sample(min(k,len(window)),random_state=random.randint(0,9999))

# ===========================
# GENERATOR
# ===========================

def generate_popular_plan():
    df = load_dataset()
    df["popular_score"] = df.apply(compute_popular_score,axis=1)
    df = df[df["popular_score"]>0]

    selected=[]

    for block, k in BLOCK_SIZES.items():
        part = select_block(df,block,k)
        part["block"]=block
        selected.append(part)

    result=pd.concat(selected).drop_duplicates("product_name")

    while len(result)<16:
        result=pd.concat([result,df.sample(1)]).drop_duplicates("product_name")

    return result[["block","category","subcategory","product_name","price","healthy_flag","popular_score","product_url"]]

# ===========================
# CLI
# ===========================

if __name__=="__main__":
    plan = generate_popular_plan()
    print("\n=== 🍔 TYPICAL AMERICAN MEAL PLAN ===\n")
    print(plan.to_string(index=False))
    print("\nTOTAL:",len(plan))