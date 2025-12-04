import streamlit as st
import pandas as pd
import random
from pages.header import render_header


def app():
    # Render common header
    render_header(current_page="home")

    # ============================================
    # 🎨 FOOD IMAGE CIRCLES SETTINGS (3 pieces)
    # ============================================
    # Replace URLs with your images or leave empty for emojis
    FOOD_IMAGES = [
        {
            'emoji': '🍗 ',
            'url': '',
            'gradient': 'linear-gradient(135deg, #FFC0CB 0%, #FFB6C1 100%)'
        },
        {
            'emoji': '🍅',
            'url': '',
            'gradient': 'linear-gradient(135deg, #FF6B6B 0%, #FF4757 100%)'
        },
        {
            'emoji': '🥒',
            'url': '',
            'gradient': 'linear-gradient(135deg, #90EE90 0%, #7FBF7F 100%)'
        }
    ]
    # ============================================

    # Custom CSS
    st.markdown("""
    <style>
    /* ==== CUSTOM BUTTON STYLE ==== */
    .stButton > button,
    .custom-categories-btn {
        width: 100%;
        height: 56px;
        border-radius: 12px;
        border: 3px solid #111 !important;
        background: #fee6e3 !important;
        font-family: "Comic Sans MS", cursive !important;
        font-size: 18px !important;
        font-weight: bold;
        color: #111 !important;
        box-shadow: 4px 4px 0px #111;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
    }
    
    /* Hover */
    .stButton > button:hover,
    .custom-categories-btn:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #111;
        background-color: #ffd1cb !important;
    }
    
    /* Click */
    .stButton > button:active,
    .custom-categories-btn:active {
        transform: translate(4px, 4px);
        box-shadow: 0px 0px 0px #111;
        background-color: #ffb6ad !important;
    }

    /* Apply Comic Sans to everything */
    * {
        font-family: "Comic Sans MS", "Comic Sans", cursive !important;
    }

    /* Gradient background */
    .stApp {
        background: linear-gradient(180deg, #8B4C4C 0%, #F5E6D3 100%);
    }

    /* Remove padding */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem;
    }

    /* Text outline for all white text */
    * {
        text-shadow: 0px 0px 2px rgba(0,0,0,0.5);
    }

    /* Meal plan card */
    .meal-card {
        background: linear-gradient(135deg, #722F37 0%, #5A1E28 100%);
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        max-width: 1000px;
    }

    .meal-title {
        color: #F4D03F;
        font-size: 42px;
        text-align: center;
        margin-bottom: 30px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        transition: transform 0.3s ease, color 0.3s ease;
        cursor: pointer;
    }

    .meal-title:hover {
        transform: rotate(-3deg) scale(1.05);
        color: #FFE44D;
    }

    .ingredients-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 20px;
    }

    .ingredient-column {
        color: white;
        font-size: 19px;
        line-height: 2.2;
    }

    .ingredient-item {
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* Categories dropdown - HOVER VERSION */
    .categories-dropdown-wrapper {
        position: relative;
        width: 100%;
    }

    .categories-dropdown {
        display: none;
        position: absolute;
        left: 0;
        top: 100%;
        background: #5A1E28;
        width: 100%;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        border-radius: 0 0 12px 12px;
        z-index: 1000;
        padding: 0;
        margin-top: -3px;
        border: 3px solid #111;
        border-top: none;
        animation: fadeIn 0.2s ease-in;
    }

    .categories-dropdown-wrapper:hover .categories-dropdown {
        display: block;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-5px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .category-option {
        color: white;
        padding: 12px 20px;
        cursor: pointer;
        font-size: 18px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
        transition: background-color 0.2s ease;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .category-option:last-child {
        border-bottom: none;
        border-radius: 0 0 9px 9px;
    }

    .category-option:hover {
        background: #8B4C4C;
    }

    /* Round images on right - AT TOP WITH ROTATION */
    .food-images-container {
        display: flex;
        flex-direction: column;
        gap: 30px;
        align-items: center;
        padding: 0;
        margin-top: 0;
    }

    .food-circle {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        overflow: hidden;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        border: 4px solid white;
        display: flex;
        align-items: center;
        justify-content: center;
        background-size: cover;
        background-position: center;
        transition: transform 0.6s ease;
    }

    .food-circle:hover {
        transform: rotate(360deg);
    }

    .food-circle-emoji {
        font-size: 70px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    # Create three columns - as in screenshot
    left_col, center_col, right_col = st.columns([1, 3, 1])

    # Left column - buttons
    with left_col:
        st.markdown("<div style='margin-top: 80px; position: relative;'>", unsafe_allow_html=True)

        if st.button("💾 Save", key="save_btn", use_container_width=True):
            st.success("✅ Meal plan saved!")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        if st.button("✨ Generate", key="create_btn", use_container_width=True):
            st.session_state.regenerate = True
            st.rerun()
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        
        # Categories button with actual Streamlit buttons
        if st.button("📂 Categories", key="categories_main_btn", use_container_width=True):
            # Toggle dropdown visibility
            if 'show_categories' not in st.session_state:
                st.session_state.show_categories = False
            st.session_state.show_categories = not st.session_state.show_categories
        
        # Show category buttons if dropdown is open
        if st.session_state.get('show_categories', False):
            st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
            
            if st.button("Budget", key="budget_btn", use_container_width=True):
                st.success("✅ Budget кнопка работает!")
                st.session_state.show_categories = False
            
            if st.button("Middle Income", key="middle_btn", use_container_width=True):
                st.success("✅ Middle Income кнопка работает!")
                st.session_state.show_categories = False
            
            if st.button("Premium", key="premium_btn", use_container_width=True):
                st.success("✅ Premium кнопка работает!")
                st.session_state.show_categories = False
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Center column - meal plan card
    with center_col:
        # Generate meal plan
        if 'current_meal' not in st.session_state or st.session_state.get('regenerate', False):
            st.session_state.current_meal = generate_meal_plan()
            st.session_state.regenerate = False

        meal = st.session_state.current_meal

        st.markdown(f"""
        <div class="meal-card">
            <h1 class="meal-title">Daily Meal Plan</h1>
            <div class="ingredients-grid">
                <div class="ingredient-column">
                    {"".join([f'<div class="ingredient-item">• {item}</div>' for item in meal['left_column']])}
                </div>
                <div class="ingredient-column">
                    {"".join([f'<div class="ingredient-item">• {item}</div>' for item in meal['right_column']])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Right column - 3 round images AT TOP WITH ROTATION
    with right_col:
        st.markdown('<div class="food-images-container">', unsafe_allow_html=True)

        for img in FOOD_IMAGES:
            if img['url']:
                # If URL exists, show image
                st.markdown(f"""
                <div class="food-circle" style="background-image: url('{img['url']}');">
                </div>
                """, unsafe_allow_html=True)
            else:
                # If no URL, show emoji with gradient
                st.markdown(f"""
                <div class="food-circle" style="background: {img['gradient']};">
                    <span class="food-circle-emoji">{img['emoji']}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def generate_meal_plan():
    """Generates random daily meal plan"""

    proteins = [
        "1 chicken breast",
        "1 salmon fillet",
        "200g beef",
        "2 eggs",
        "150g tofu",
        "1 turkey fillet"
    ]

    vegetables = [
        "2 cups greens",
        "1 cup broccoli florets",
        "1 zucchini",
        "1 bell pepper",
        "150g spinach"
    ]

    small_veggies = [
        "½ cup cherry tomatoes",
        "¼ cup radish",
        "½ cucumber",
        "1 carrot"
    ]

    carbs = [
        "½ cup rice",
        "100g buckwheat",
        "2 bread slices",
        "150g pasta",
        "1 sweet potato"
    ]

    fats = [
        "⅓ cup sliced cucumber",
        "⅓ sliced avocado",
        "30g nuts",
        "2 tbsp hummus"
    ]

    oils = [
        "1 tbsp olive oil",
        "1 tsp coconut oil",
        "1 tbsp sesame oil"
    ]

    extras = [
        "1 tbsp balsamic vinegar",
        "1 garlic clove",
        "Quarter lemon",
        "2 tbsp soy sauce",
        "1 tsp honey"
    ]

    # Generate left column
    left_column = [
        random.choice(proteins),
        random.choice(vegetables),
        random.choice(small_veggies),
        random.choice(fats),
        random.choice(fats),
        random.choice(oils),
        random.choice(extras),
        "<i>Salt and pepper to taste</i>"
    ]

    # Generate right column
    right_column = [
        random.choice(proteins),
        random.choice(carbs),
        random.choice(vegetables),
        random.choice(oils),
        random.choice(extras),
        random.choice(extras),
        "",
        "<i>Salt and pepper to taste</i>"
    ]

    return {
        'left_column': left_column,
        'right_column': right_column
    }