import streamlit as st
from pages.header import render_header

def app():
    # Render common header
    render_header(current_page="faq")
    
    # Apply Comic Sans and text outline
    st.markdown("""
    <style>

    /* ================================
       GLOBAL FONT (SAFE)
    ================================ */
    * {
        font-family: "Comic Sans MS", "Comic Sans", cursive !important;
    }

    /* ================================
       PAGE BACKGROUND FIX (OPTIONAL)
    ================================ */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #8B4C4C 0%, #F5E6D3 100%);
    }

    /* ================================
       FAQ CONTAINER STYLE
    ================================ */
    .faq-section {
        background: rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 22px;
        margin: 18px 0;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.12);
    }

    /* ================================
       FAQ TEXT STYLE
    ================================ */
    .faq-question {
        font-size: 22px;
        font-weight: bold;
        color: #F4D03F;
    }

    .faq-answer {
        font-size: 18px;
        color: #FFF;
        line-height: 1.7;
        text-shadow: 0 0 2px rgba(0,0,0,0.4);
    }

    /* ================================
       FIX FOR EXPANDER BUG (IMPORTANT)
    ================================ */
    details summary,
    details summary * {
        text-shadow: none !important;
        filter: none !important;
        text-rendering: auto !important;
    }

    /* Remove underline glitch */
    details summary {
        text-decoration: none !important;
    }

    /* Hide keyboard_arrow_right icon */
    [data-testid="stIconMaterial"] {
        display: none !important;
    }
    
    /* Alternative: hide the icon span */
    details summary span[data-testid="stIconMaterial"] {
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* ================================
       EXPANDER LOOK
    ================================ */
    details {
        border-radius: 14px;
        background: rgba(255,255,255,0.10);
        padding: 10px;
        margin-bottom: 12px;
    }

    /* Hover effect */
    details:hover {
        background: rgba(255,255,255,0.14);
    }

    /* ================================
       KEEP BUTTONS SAFE
    ================================ */
    button, a {
        text-shadow: none !important;
    }

    button::before,
    button::after {
        filter: none !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("❓ Frequently Asked Questions")
    st.write("Find answers to common questions about Meal Plan Generator")
    
    st.markdown("---")
    
    # FAQ 1
    with st.expander("🍽️ What is Meal Plan Generator?", expanded=True):
        st.markdown("""
        **Meal Plan Generator** is a web application designed to help you plan your daily meals 
        according to your budget and dietary preferences. Our tool uses datasets of grocery items 
        with different price ranges to create balanced and affordable meal plans.
        """)
    
    # FAQ 2
    with st.expander("💰 What budget categories are available?"):
        st.markdown("""
        We currently offer three budget categories:
        - **Budget**: Affordable options for cost-conscious shoppers
        - **Middle Income**: Balanced quality and price options
        - **Premium**: High-quality ingredients for those who prefer premium products
        
        Each category has its own dataset with appropriate products and pricing.
        """)
    
    # FAQ 3
    with st.expander("📊 How accurate are the nutritional values?"):
        st.markdown("""
        Our nutritional data comes from verified datasets and is regularly updated. 
        We include information about:
        - Calories
        - Proteins, Fats, and Carbohydrates
        - Price per unit
        - Product categories
        
        However, always verify specific dietary requirements with a healthcare professional.
        """)
    
    # FAQ 4
    with st.expander("🔄 How often can I generate new meal plans?"):
        st.markdown("""
        You can generate new meal plans as many times as you want! Simply click the 
        **"Generate"** button to get a fresh, randomized meal plan. Each plan is designed 
        to be balanced and include a variety of proteins, vegetables, carbohydrates, and healthy fats.
        """)
    
    # FAQ 5
    with st.expander("💾 Can I save my meal plans?"):
        st.markdown("""
        Yes! Use the **"Save"** button to store your favorite meal plans. 
        *(Note: This feature is currently in development and will be fully functional in the next update)*
        """)
    
    # FAQ 6
    with st.expander("📱 Is the app mobile-friendly?"):
        st.markdown("""
        Yes! Meal Plan Generator is built with Streamlit and is fully responsive. 
        You can access it from your smartphone, tablet, or desktop computer. 
        The interface adapts to your screen size for the best experience.
        """)
    
    # FAQ 7
    with st.expander("📈 What information is available in Statistics?"):
        st.markdown("""
        The Statistics page provides comprehensive analysis including:
        - Price distribution across different budget categories
        - Product count by category
        - Calorie analysis and top calorie products
        - Comparative charts between budget types
        - Detailed nutritional breakdowns
        """)
    
    # FAQ 8
    with st.expander("📁 Can I upload my own datasets?"):
        st.markdown("""
        Currently, the app works with pre-loaded datasets. However, you can explore 
        existing datasets through the **Datasets** page, where you can:
        - View all available products
        - Filter and search data
        - Download filtered datasets
        - See detailed statistics
        
        Custom dataset upload is planned for a future release.
        """)
    
    # FAQ 9
    with st.expander("🤖 Does the app use AI/Machine Learning?"):
        st.markdown("""
        Yes! Our team has implemented machine learning algorithms to:
        - Optimize meal plan combinations
        - Balance nutritional values
        - Suggest complementary ingredients
        - Analyze pricing trends
        
        The ML models are continuously being improved to provide better recommendations.
        """)
    
    # FAQ 10
    with st.expander("👥 Who developed this app?"):
        st.markdown("""
        Meal Plan Generator was developed by a dedicated team of three professionals:
        - **Roman Gribanov** - Project Leader
        - **John Raymond** - Frontend Developer & UI/UX Designer
        - **Ruslan Babayev** - Data Scientist & ML Engineer
        
        Visit the **About** page to learn more about the team!
        """)
    
    # FAQ 11
    with st.expander("🐛 I found a bug. How do I report it?"):
        st.markdown("""
        We appreciate your feedback! If you encounter any issues:
        1. Note the page where the issue occurred
        2. Take a screenshot if possible
        3. Contact us through the email addresses on the **About** page
        4. Use the thumbs down button on problematic features
        
        Your feedback helps us improve the app for everyone!
        """)
    
    # FAQ 12
    with st.expander("🔮 What features are coming next?"):
        st.markdown("""
        We're constantly working on improvements! Upcoming features include:
        - ✨ User account system with saved preferences
        - 🍽️ Recipe suggestions with step-by-step instructions
        - 📅 Weekly meal planning calendar
        - 🛒 Shopping list generator
        - 🥗 Dietary restriction filters (vegan, gluten-free, etc.)
        - 📊 Personal nutrition tracking
        - 🤝 Meal plan sharing with friends
        
        Stay tuned for updates!
        """)
    
    st.markdown("---")
    
    # Contact section
    st.markdown("## 📧 Still Have Questions?")
    st.write("""
    If you couldn't find the answer you were looking for, feel free to reach out to our team 
    through the contact information on the **About** page. We're here to help!
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📧 Email Support")
    with col2:
        st.info("💬 Community Forum")
    with col3:
        st.info("📖 Documentation")