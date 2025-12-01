import streamlit as st
from pages.header import render_header

def app():
    # Render common header
    render_header(current_page="account")
    
    # Apply Comic Sans and text outline
    st.markdown("""
    <style>
    * {
        font-family: "Comic Sans MS", "Comic Sans", cursive !important;
        text-shadow: 0px 0px 2px rgba(0,0,0,0.5);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .feature-title {
        font-size: 24px;
        font-weight: bold;
        color: #F4D03F;
        margin-bottom: 15px;
    }
    
    .feature-description {
        font-size: 18px;
        color: white;
        line-height: 1.6;
    }
    
    .coming-soon-badge {
        display: inline-block;
        background: #FF6B6B;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("👤 My Account")
    st.write("Manage your profile, saved meal plans, and preferences")
    
    st.markdown("---")
    
    # Info message
    st.info("🚧 **Account features are currently under development.** Check back soon for exciting new capabilities!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upcoming Features Section
    st.markdown("## 🎯 Planned Account Features")
    
    # Feature 1: Profile Management
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 👤")
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Profile Management <span class="coming-soon-badge">Coming Soon</span></div>
            <div class="feature-description">
                Create and customize your profile with dietary preferences, allergies, 
                and favorite ingredients. Set your budget range and meal planning goals.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 2: Saved Meal Plans
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 💾")
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Saved Meal Plans <span class="coming-soon-badge">Coming Soon</span></div>
            <div class="feature-description">
                Save your favorite meal plans and access them anytime. Create collections, 
                add notes, and rate your saved plans for easy reference.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 3: Shopping History
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 🛒")
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Shopping History <span class="coming-soon-badge">Coming Soon</span></div>
            <div class="feature-description">
                Track your grocery shopping history, spending patterns, and frequently 
                purchased items. Get insights on your food budget over time.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 4: Meal Calendar
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 📅")
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Weekly Calendar <span class="coming-soon-badge">Coming Soon</span></div>
            <div class="feature-description">
                Plan your meals for the entire week with our interactive calendar. 
                Drag and drop meal plans, set reminders, and sync with your devices.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 5: Nutrition Tracking
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 📊")
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Nutrition Tracking <span class="coming-soon-badge">Coming Soon</span></div>
            <div class="feature-description">
                Monitor your daily calorie intake, macronutrients, and nutritional goals. 
                View detailed reports and progress charts.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 6: Social Sharing
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 🤝")
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Share & Collaborate <span class="coming-soon-badge">Coming Soon</span></div>
            <div class="feature-description">
                Share your meal plans with family and friends. Collaborate on grocery 
                lists and discover popular meal plans from the community.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Placeholder account preview
    st.markdown("## 🎨 Account Preview")
    
    col1, col2, col3 = st.columns(3)
    