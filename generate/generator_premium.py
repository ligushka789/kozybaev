
import pandas as pd
from pathlib import Path

DATASET_PATH = Path("datasets/walmart_scored.csv")

MIN_PREMIUM_PRICE = 6.0
MAX_PREMIUM_PRICE = 80

BLOCK_SIZES = {
    "protein": 4,
    "side": 4,
    "breakfast": 3,
    "snack": 3,
    "drink": 2
}

IGNORE_BLOCK = "ignore"
GREAT_VALUE = "great value"


# ======================
# PREMIUM MARKERS
# ======================
PREMIUM_BRANDS = [
    "haagen", "haagen-dazs", "ben & jerry", "magnum",
    "starbucks", "kirkland", "dunkin", "red bull",
    "monster", "kombucha", "angus", "ribeye", "prime",
    "organic valley", "tillamook", "talenti", "lindor",
    "peet", "la colombe"
]

ANTI_PREMIUM = [
    "mini","snack size","small pack","value pack","family pack","party pack","economy",
    "budget","cheap","tray","assortment","variety","box","ct","count","bag","pack","multipack",
    "kit","set","filler","pinata","piñata",
    "macaroni","mac and cheese","sandwich","pancake mix","waffle mix","tenders","nuggets",
    "meal","skillet","dinner","frozen meal",
    "vegan","plant-based","meatless",
    "supplement","nootropic","brain","focus","memory",
    "drink mix","powder","instant",
    "ground coffee","coffee beans","canister","jar",
    "amp energy","energy powder"
]

DAIRY = ["milk","cream","yogurt","chocolate milk"]
HOT_BREAKFAST = ["bacon","sausage","egg","sandwich","waffle","pancake","biscuit","muffin"]
SEAFOOD_STEAK = ["steak","ribeye","sirloin","shrimp","salmon","lobster","crab","snapper","tuna"]
DRINK_ALT = ["energy","kombucha","tea","juice","sparkling","soda","water"]


# ======================
# LOAD DATASET
# ======================
def load_dataset():
    df = pd.read_csv(DATASET_PATH)

    df = df[df["price"].notna()]
    df = df[df["product_name"].notna()]
    df = df[df["ml_block"] != IGNORE_BLOCK]
    df = df[(df["price"] >= MIN_PREMIUM_PRICE) & (df["price"] <= MAX_PREMIUM_PRICE)]
    df = df[~df["product_name"].str.lower().str.contains(GREAT_VALUE, na=False)]

    return df.reset_index(drop=True)


# ======================
# PREMIUM SCORE
# ======================
def compute_premium_score(row):
    name = row["product_name"].lower()
    price = row["price"]

    score = price * 2

    # бренд — это важно
    for b in PREMIUM_BRANDS:
        if b in name:
            score += 200

    # мясо и морепродукты должны доминировать
    if any(x in name for x in SEAFOOD_STEAK):
        score += 700

    # мусору — жёсткий минус
    for bad in ANTI_PREMIUM:
        if bad in name:
            score -= 300

    return score


# ======================
# VALIDATION BY BLOCK
# ======================
def validate_block(block, name):
    n = name.lower()

    # DRINK — только напитки
    if block == "drink":
        if any(x in n for x in [
            "pizza","burger","meat","bacon","sausage","chicken","egg","fish",
            "salmon","shrimp","lobster","crab","steak","tuna",
            "supplement","nootropic","capsule","pill","brain","focus",
            "powder","mix","shot",
            "machine","maker","brewer","grinder","system","cup","mug",
            "ground coffee","instant","jar","canister"
        ]):
            return False

    # PROTEIN — ТОЛЬКО чистое мясо и рыба
    if block == "protein":
        if not any(x in n for x in SEAFOOD_STEAK + ["beef","chicken","pork","lamb","duck"]):
            return False
        if any(x in n for x in [
            "cheese","sandwich","biscuit","breakfast","meal","skillet","dinner","microwave",
            "nugget","tender","strip","patty","ready",
            "fight","protein bar","snack",
            "vegan","plant-based","meatless"
        ]):
            return False

    # SIDE — ГАРНИР, НЕ ЕДА ИЗ КОНДИТЕРКИ
    if block == "side":
        if any(x in n for x in [
            "cake","cheesecake","cupcake","pie","dessert","ice cream",
            "beef","chicken","pork","sausage","bacon","steak","ribeye","sirloin",
            "salmon","shrimp","tuna","lobster","crab","fish",
            "burger","rib","wings","fillet","ham","salami",
            "meal","skillet","dinner"
        ]):
            return False

    # SNACK — никакой оптовки
    if block == "snack":
        if any(x in n for x in ["variety","assortment","pack","bundle","box","ct","count","bag"]):
            return False

    return True

# ======================
# BLOCK SELECTOR
# ======================
def select_premium_block(df, block, k):

    pool = df[df["ml_block"] == block]
    pool = pool[pool["product_name"].apply(lambda x: validate_block(block, x))]

    pool = pool.assign(
        is_brand = pool["product_name"].str.lower().apply(
            lambda x: any(b in x for b in PREMIUM_BRANDS)
        )
    ).sort_values(["is_brand","premium_score"], ascending=False)

    window = pool.head(80)

    from generate.generator_popular import get_protein_type, get_breakfast_type, get_snack_type

    selected = []


    # ===== PROTEIN =====
    if block == "protein":
        used = set()
        for _, row in window.iterrows():
            name = row["product_name"].lower()
            ptype = get_protein_type(name)

            if ptype in used:
                continue

            if not any(x in name for x in SEAFOOD_STEAK):
                continue

            selected.append(row)
            used.add(ptype)

            if len(selected) == k:
                break


    # ===== BREAKFAST =====
    elif block == "breakfast":
        used = set()
        dairy_count = 0
        has_hot = False

        for _, row in window.iterrows():
            name = row["product_name"].lower()
            btype = get_breakfast_type(name)

            is_dairy = any(d in name for d in DAIRY)
            is_hot = any(h in name for h in HOT_BREAKFAST)

            # пока нет горячего — не брать молочку
            if is_dairy and not has_hot:
                continue

            # максимум 1 молочка
            if is_dairy:
                if dairy_count >= 1:
                    continue
                dairy_count += 1

            if btype in used:
                continue

            if is_hot:
                has_hot = True

            selected.append(row)
            used.add(btype)

            if len(selected) == k:
                break

        # жёсткая гарантия горячего
        if not has_hot:
            hot = window[window["product_name"].str.lower().str.contains("|".join(HOT_BREAKFAST), na=False)]
            if len(hot):
                selected[0] = hot.iloc[0]


    # ===== SNACK =====
    elif block == "snack":
        used = set()
        brand_used = set()
        fallback = []

        for _, row in window.iterrows():
            name = row["product_name"].lower()
            stype = get_snack_type(name)
            brand = next((b for b in PREMIUM_BRANDS if b in name), None)

            if brand and brand in brand_used:
                continue
            if stype in used:
                continue

            if brand:
                selected.append(row)
                brand_used.add(brand)
                used.add(stype)
            else:
                fallback.append(row)

            if len(selected) == k:
                break

        for r in fallback:
            if len(selected) == k:
                break
            selected.append(r)

        # гарантия бренда
        if not any(any(b in str(x["product_name"]).lower() for b in PREMIUM_BRANDS)
                   for _, x in pd.DataFrame(selected).iterrows()):
            branded = window[window["product_name"].str.lower().str.contains("|".join(PREMIUM_BRANDS), na=False)]
            if len(branded):
                selected[-1] = branded.iloc[0]


    # ===== DRINK =====
    elif block == "drink":
        coffee_count = 0
        alt_used = False

        for _, row in window.iterrows():
            name = row["product_name"].lower()

            if any(x in name for x in ["instant","ground coffee","canister","jar","powder","shot"]):
                continue
            is_coffee = any(x in name for x in ["coffee","espresso","k-cup","pod","capsule"])
            is_alt = any(a in name for a in DRINK_ALT)

            if is_coffee:
                if coffee_count >= 1:
                    continue
                coffee_count += 1

            if is_alt:
                alt_used = True

            selected.append(row)

            if len(selected) == k:
                break

        # гарантия не-кофе
        if not alt_used:
            alt = window[window["product_name"].str.lower().str.contains("|".join(DRINK_ALT), na=False)]
            if len(alt):
                selected[-1] = alt.iloc[0]


    else:
        selected = window.head(k).to_dict("records")

    return pd.DataFrame(selected)


# ======================
# GENERATE PLAN
# ======================
def generate_premium_plan():

    df = load_dataset()
    df["premium_score"] = df.apply(compute_premium_score, axis=1)

    parts = []

    for block, k in BLOCK_SIZES.items():
        part = select_premium_block(df, block, k)

        if len(part) < k:
            need = k - len(part)
            extra = df[df["ml_block"] == block].sort_values("premium_score", ascending=False).head(need)
            part = pd.concat([part, extra])

        part["block"] = block
        parts.append(part)

    result = pd.concat(parts).drop_duplicates("product_name")

    # safety net (никогда не зависает)
    attempts = 0
    while len(result) < 16 and attempts < 200:
        extra = df.sample(1)
        extra["block"] = extra["ml_block"]
        result = pd.concat([result, extra]).drop_duplicates("product_name")
        attempts += 1

    return result[["block","category","subcategory","product_name","price","product_url"]]


# ======================
# CLI
# ======================
if __name__ == "__main__":
    plan = generate_premium_plan()
    print("\n=== 💎 PREMIUM MEAL PLAN / v6 FINAL ===\n")
    print(plan.to_string(index=False))
    print("\nTOTAL:", len(plan))


