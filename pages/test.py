import streamlit as st
from PIL import Image
import os
import json
from datetime import datetime


def app():
    # ==== LOAD LOGO ====
    logo_path = os.path.join("src", "logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
    
    # Custom CSS
    st.markdown("""
    <style>
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
        padding-top: 2rem !important;
        padding-bottom: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Text outline */
    * {
        text-shadow: 0px 0px 2px rgba(0,0,0,0.3);
    }

    /* Logo container */
    .logo-container {
        text-align: center;
        margin-bottom: 40px;
    }

    /* Test card */
    .test-card {
        background: linear-gradient(135deg, #722F37 0%, #5A1E28 100%);
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }

    .test-title {
        color: #F4D03F;
        font-size: 42px;
        text-align: center;
        margin-bottom: 30px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .question-block {
        padding: 20px 0;
        margin-bottom: 15px;
    }

    .question-text {
        color: white;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }

    /* Radio buttons styling */
    .stRadio > div {
        gap: 10px;
    }

    .stRadio > div > label {
        background: rgba(255,255,255,0.15);
        padding: 12px 20px;
        border-radius: 10px;
        border: 2px solid rgba(255,255,255,0.3);
        color: white !important;
        font-size: 18px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .stRadio > div > label:hover {
        background: rgba(255,255,255,0.25);
        border-color: rgba(255,255,255,0.5);
    }

    /* Submit button */
    .stButton > button {
        width: 100%;
        height: 60px;
        border-radius: 12px;
        border: 3px solid #111 !important;
        background: #fee6e3 !important;
        font-family: "Comic Sans MS", cursive !important;
        font-size: 22px !important;
        font-weight: bold;
        color: #111 !important;
        box-shadow: 4px 4px 0px #111;
        transition: all 0.2s ease-in-out;
        margin-top: 30px;
    }
    
    .stButton > button:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #111;
        background-color: #ffd1cb !important;
    }
    
    .stButton > button:active {
        transform: translate(4px, 4px);
        box-shadow: 0px 0px 0px #111;
        background-color: #ffb6ad !important;
    }

    /* Warning message */
    .stAlert {
        border-radius: 15px;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Home button
    home_col = st.columns([1, 1, 1])
    with home_col[1]:
        if st.button("🏠 Home"):
            st.query_params["page"] = "home"
            st.rerun()


    # Display logo (2x bigger, perfectly centered)
    if os.path.exists(logo_path):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
            st.image(logo, width=210)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Initialize session state for answers
    if 'test_answers' not in st.session_state:
        st.session_state.test_answers = {}

    # Test content
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="test-title">Testing</h1>', unsafe_allow_html=True)

    # Questions
    questions = [
        {"id": 1, "text": "Question 1", "options": ["Option A", "Option B", "Option C"]},
        {"id": 2, "text": "Question 2", "options": ["Option A", "Option B", "Option C"]},
        {"id": 3, "text": "Question 3", "options": ["Option A", "Option B", "Option C"]},
        {"id": 4, "text": "Question 4", "options": ["Option A", "Option B", "Option C"]},
        {"id": 5, "text": "Question 5", "options": ["Option A", "Option B", "Option C"]},
        {"id": 6, "text": "Question 6", "options": ["Option A", "Option B", "Option C"]},
        {"id": 7, "text": "Question 7", "options": ["Option A", "Option B", "Option C"]},
        {"id": 8, "text": "Question 8", "options": ["Option A", "Option B", "Option C"]},
        {"id": 9, "text": "Question 9", "options": ["Option A", "Option B", "Option C"]},
        {"id": 10, "text": "Question 10", "options": ["Option A", "Option B", "Option C"]},
    ]

    # Display questions
    for q in questions:
        st.markdown(f'<div class="question-block">', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">{q["text"]}</div>', unsafe_allow_html=True)
        
        answer = st.radio(
            f"Select answer for question {q['id']}:",
            q["options"],
            key=f"q_{q['id']}",
            label_visibility="collapsed",
            index=None  # Добавлено: нет выбранного варианта по умолчанию
        )
        
        # Save answer to session state
        if answer:
            st.session_state.test_answers[q['id']] = answer
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Submit button
    if st.button("🎯 Complete Test", key="submit_test"):
        # Check if all questions are answered
        if len(st.session_state.test_answers) < len(questions):
            st.error("⚠️ You have unanswered questions! Please answer all questions before completing the test.")
        else:
            # Save answers to JSON file
            result = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "answers": st.session_state.test_answers
            }
            
            # Save to root directory with fixed filename
            filename = "test_results.json"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                
                st.success(f"✅ Test completed successfully! Results saved to file: {filename}")
                st.balloons()
                
                # Clear answers after successful submission
                st.session_state.test_answers = {}
                
                # Redirect to home page after 2 seconds
                st.query_params["page"] = "home"
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error saving results: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)