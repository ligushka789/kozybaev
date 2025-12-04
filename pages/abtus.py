import streamlit as st
from pages.header import render_header

def app():
    # Render common header
    render_header(current_page="about")
    
    # Apply Comic Sans and text outline
    st.markdown("""
    <style>
    * {
        font-family: "Comic Sans MS", "Comic Sans", cursive !important;
        text-shadow: 0px 0px 2px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("ℹ️ About Us")
    st.write("Meet the Meal Plan Generator development team!")
    
    st.markdown("---")
    
    # Create three columns for team cards
    col1, col2, col3 = st.columns(3)
    
    # ============================================
    # CARD 1: Roman Gribanov (Project Leader)
    # ============================================
    with col1:
        st.markdown("### 👨‍💼 Roman Gribanov")
        st.markdown("**Project Leader**")
        
        st.image("https://sun9-39.userapi.com/s/v1/ig2/cR0VpV6bVY29ytnH2Ma-K4u4wGv1mlvaNQNdPsjTMTHJtUmKSjLecakoSBGyIRQogpWl2XbFoMmBPKrSGKJNtVbT.jpg?quality=95&as=32x26,48x39,72x58,108x87,160x130,240x194,360x292,480x389,540x437,640x519,720x583,1080x875&from=bu&cs=1080x0", use_container_width=True)
        
        st.markdown("""
        **Role in project:**
        - Team leadership
        - Work coordination
        - Project architecture
        - Backend development
        - ML models
        
        **Contacts:**
        - 📧 Email: roman@example.com
        - 💼 LinkedIn: https://www.linkedin.com/in/roman-gribanov-data/
        - 🐙 GitHub: https://github.com/ligushka789
        """)
    
    # ============================================
    # CARD 2: John Raymond
    # ============================================
    with col2:
        st.markdown("### 👨‍💻 John Raymond")
        st.markdown("**Team Member**")
        
        st.image("https://sun9-84.userapi.com/s/v1/ig2/zAIygyLw5sHJHHDF9ceO_hqwsfbiU7YPfFd8KB6IyVCfXjzgdMHSjIPSuigb1MgqvH7gR2L61atxOum5HImpvIov.jpg?quality=95&as=32x47,48x71,72x106,108x159,160x236,240x354,360x532,480x709,540x797,600x886&from=bu&cs=600x0", use_container_width=True)
        
        st.markdown("""
        **Role in project:**
        - Frontend development
        - UI/UX design
        - Testing
        - Poster creator
        
        **Contacts:**
        - 📧 Email: john@example.com
        - 💼 LinkedIn: https://www.linkedin.com/in/pavelyeremenko/
        - 🐙 GitHub: https://github.com/JohnRaymondTwin
        """)
    
    # ============================================
    # CARD 3: Ruslan Babayev
    # ============================================
    with col3:
        st.markdown("### 👨‍🔬 Ruslan Babayev")
        st.markdown("**Team Member**")
        
        st.image("https://sun9-84.userapi.com/s/v1/ig2/TI0a4eFkbeCgyzPTitW7Uhvo-jo7N5CBc7rp_SlR2Twrl3WGqGDBYMusOTe2wkIgKXGG5VpGLH6uMpZx_zvncIj4.jpg?quality=95&as=32x30,48x45,72x67,108x101,160x149,240x224,360x335,480x447,540x503,640x596,720x671,1080x1006,1200x1118&from=bu&cs=1200x0", use_container_width=True)
        
        st.markdown("""
        **Role in project:**
        - Data Science
        - Visualizations
        - Data analysis
        - Frontend development
        
        **Contacts:**
        - 📧 Email: babayev21@arizona.edu
        - 💼 LinkedIn: https://www.linkedin.com/in/ruslanbabayevkz/
        - 🐙 GitHub: https://github.com/immortalburning
        """)
    
    st.markdown("---")
    
    # Project information
    st.markdown("## 📋 About the Project")
    st.write("""
    **Meal Plans For You** is an MVP project developed as part of a capstone project.
    
    The project's goal is to help people plan their meals according to their budget and preferences.
    
    ### Key Features:
    - 🥗 Ready-made meal plans for different budgets
    - 📊 Product analysis and statistics
    - 📁 Work with product and recipe datasets
    - 🎯 Personalization for different lifestyles
    - 🤖 Machine Learning for plan optimization
    
    ### Technologies:
    - Python
    - Streamlit
    - Pandas
    - Plotly
    - Joblib
    - Data Analysis & ML
    """)
    
    st.markdown("---")
    st.markdown("*© Meal Plans For You Team. All rights reserved.*")
