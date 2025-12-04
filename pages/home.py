import streamlit as st
import pandas as pd
import random
from pages.header import render_header
from generate.generator import generate_meal_plan as ml_generate_meal_plan
from generate.generator_healthy import generate_healthy_plan as healthy_generate_meal_plan


def app():
    if "plan_type" not in st.session_state:
        st.session_state.plan_type = None
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

        # Save button with PDF download functionality
        if st.session_state.get('current_meal') and st.session_state.get('plan_type'):
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.units import inch
            from io import BytesIO
            import re
            
            meal = st.session_state.current_meal
            
            # Create PDF in memory
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#722F37'),
                spaceAfter=30,
                alignment=1  # Center
            )
            
            # Title
            plan_name = "Budget Meal Plan" if st.session_state.plan_type == "budget" else "Healthy Meal Plan"
            title = Paragraph(f"<b>{plan_name}</b>", title_style)
            elements.append(title)
            elements.append(Spacer(1, 0.2*inch))
            
            # Prepare table data
            all_items = meal['left_column'] + meal['right_column']
            table_data = [['Product', 'Price']]
            
            for item in all_items:
                # Remove HTML tags
                clean_item = re.sub('<.*?>', '', item)
                parts = clean_item.split(' — ')
                if len(parts) == 2:
                    product = parts[0].strip()
                    price = parts[1].strip()
                    table_data.append([product, price])
            
            # Add total row
            table_data.append(['TOTAL', f"${meal['total_price']}"])
            
            # Create table
            table = Table(table_data, colWidths=[4.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#722F37')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F4D03F')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.beige, colors.white])
            ]))
            
            elements.append(table)
            
            # Build PDF
            doc.build(elements)
            pdf_data = buffer.getvalue()
            buffer.close()
            
            # Determine filename
            if st.session_state.plan_type == "budget":
                filename = "budget_meal_plan.pdf"
            elif st.session_state.plan_type == "healthy":
                filename = "healthy_meal_plan.pdf"
            else:
                filename = "meal_plan.pdf"
            
            # Download button
            st.download_button(
                label="💾 Save",
                data=pdf_data,
                file_name=filename,
                mime="application/pdf",
                key="save_btn",
                use_container_width=True
            )
        else:
            # If no meal plan generated yet
            if st.button("💾 Save", key="save_btn", use_container_width=True):
                st.warning("⚠️ Please generate a meal plan first!")
        
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
        
        # Categories button
        if st.button("📂 Categories", key="categories_main_btn", use_container_width=True):
            if 'show_categories' not in st.session_state:
                st.session_state.show_categories = False
            st.session_state.show_categories = not st.session_state.show_categories
        
        # Show category buttons if dropdown is open
        if st.session_state.get('show_categories', False):
            st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
            
            if st.button("Budget", key="budget_btn", use_container_width=True):
                st.session_state.plan_type = "budget"
                st.session_state.regenerate = True
                st.session_state.show_categories = False
                st.rerun()
            
            if st.button("Healthy food", key="middle_btn", use_container_width=True):
                st.session_state.plan_type = "healthy"
                st.session_state.regenerate = True
                st.session_state.show_categories = False
                st.rerun()
            
            if st.button("Premium", key="premium_btn", use_container_width=True):
                st.success("✅ Premium кнопка работает!")
                st.session_state.show_categories = False
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Center column - meal plan card
    with center_col:
        # Generate meal plan
        if st.session_state.get("plan_type") and ('current_meal' not in st.session_state or st.session_state.get('regenerate', False)
             ):
            if st.session_state.plan_type == "budget":
                st.session_state.current_meal = generate_meal_plan()
            elif st.session_state.plan_type == "healthy":
                st.session_state.current_meal = generate_healthy_meal_plan_ui()
            else:
                st.session_state.current_meal = generate_meal_plan()
            st.session_state.regenerate = False

        if st.session_state.plan_type is None:
            st.markdown("""
            <div style="display:flex;justify-content:center;align-items:center;height:300px;">
                <iframe 
                    src="https://lottie.host/embed/fbf7fb23-9cc5-4e07-97b0-f97afa787dc4/OLKsHTvBR7.lottie"
                    style="width:300px;height:300px;border:none;">
                </iframe>
            </div>
            <h3 style="text-align:center;color:#F4D03F;">Choose a category 👈</h3>
            """, unsafe_allow_html=True)
            return
        else:
            meal = st.session_state.current_meal

        st.markdown(f"""
        <div class="meal-card">
            <h1 class="meal-title">Daily Meal Plan</h1>
            <div class="ingredients-grid">
                <div class="ingredient-column">
                    {"".join([f'<div class="ingredient-item">{item}</div>' for item in meal['left_column']])}
                </div>
                <div class="ingredient-column">
                    {"".join([f'<div class="ingredient-item">{item}</div>' for item in meal['right_column']])}
                </div>
            </div>
            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid rgba(255,255,255,0.3); text-align: center;">
                <span style="color: #F4D03F; font-size: 32px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                    Total: ${meal['total_price']}
                </span>
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
    """
    Generates meal plan using ML model (ml/model.pkl)
    and generator logic from generate/generator.py
    """

    df = ml_generate_meal_plan()

    # Split to 2 columns
    half = len(df) // 2
    left_df = df.iloc[:half]
    right_df = df.iloc[half:]

    def fmt(row):
        product = row['product_name']
        price = round(row['price'], 2)
        url = row.get('product_url', '')
        
        if url and url.strip():
            # Create hyperlink with price as clickable text
            return f"{product} — <a href='{url}' target='_blank' style='color: #F4D03F; text-decoration: underline;'>${price}</a>"
        else:
            # No URL available, just show price
            return f"{product} — ${price}"

    left_column = [fmt(r) for _, r in left_df.iterrows()]
    right_column = [fmt(r) for _, r in right_df.iterrows()]

    # Calculate total price
    total_price = df['price'].sum()

    return {
        "left_column": left_column,
        "right_column": right_column,
        "total_price": round(total_price, 2)
    }


def generate_healthy_meal_plan_ui():
    df = healthy_generate_meal_plan()

    half = len(df) // 2
    left_df = df.iloc[:half]
    right_df = df.iloc[half:]

    def fmt(row):
        product = row['product_name']
        price = round(row['price'], 2)
        url = row.get('product_url', '')

        if url and url.strip():
            return f"{product} — <a href='{url}' target='_blank' style='color: #7CFC00; text-decoration: underline;'>${price}</a>"
        else:
            return f"{product} — ${price}"

    # Calculate total price
    total_price = df['price'].sum()

    return {
        "left_column": [fmt(r) for _, r in left_df.iterrows()],
        "right_column": [fmt(r) for _, r in right_df.iterrows()],
        "total_price": round(total_price, 2)
    }