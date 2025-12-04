import streamlit as st
from PIL import Image
import os


def render_header(current_page="home"):

    # ==== LOAD LOGO ====
    logo_path = os.path.join("src", "logo.png")
    if not os.path.exists(logo_path):
        st.error("❌ Logo not found at src/logo.png")
        return

    logo = Image.open(logo_path)

    # ==== CSS ====
    st.markdown("""
    <style>
    * { font-family: "Comic Sans MS", "Comic Sans", cursive !important; }

    header[data-testid="stHeader"] { display: none !important; }

    .main-header {
        height: 130px;
        background: linear-gradient(180deg, #8B4C4C, #5A1E28);
        padding: 0 40px;
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        max-width: 10000px;  /* Или любое другое значение */
        margin: 0 auto;     /* Центрируем */
    }

    .nav-left,
    .nav-right {
        display: flex;
        align-items: center;
        gap: 30px;
    }

    .nav-left {
        justify-content: flex-start;
    }

    .nav-right {
        justify-content: flex-end;
    }

    .logo-center {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }

    .logo-center img {
        height: 105px;
        cursor: pointer;
        transition: transform 0.6s ease;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,.3));
    }

    .logo-center img:hover {
        transform: rotate(360deg) scale(1.05);
    }

    .tagline {
        color: white;
        font-size: 22px;
        font-style: italic;
        text-shadow: 1px 1px 3px rgba(0,0,0,.4);
        white-space: nowrap;
    }

    .stButton > button {
        background: transparent !important;
        border: none !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        padding: 8px 12px !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,.4) !important;
    }

    .stButton > button:hover {
        text-decoration: underline !important;
    }

    /* DROPDOWN MENU - УЛУЧШЕННАЯ ВЕРСИЯ */
    .dropdown {
        position: relative;
        display: inline-block;
    }

    .dropbtn {
        background: none;
        border: none;
        color: white;
        font-size: 22px;
        cursor: pointer;
        font-weight: 600;
        text-shadow: 1px 1px 3px rgba(0,0,0,.4);
        padding: 8px 12px;
    }

    .dropbtn:hover {
        text-decoration: underline;
    }

    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #5A1E28;
        min-width: 190px;
        border-radius: 10px;
        padding: 10px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,.3);
        top: 100%;
        right: 0;
        margin-top: 2px;
        z-index: 10;
    }

    .dropdown-content a {
        display: block;
        padding: 12px 20px;
        color: white;
        cursor: pointer;
        font-size: 18px;
        text-decoration: none;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
        transition: background-color 0.2s ease;
    }

    .dropdown-content a:hover {
        background-color: #8B4C4C;
    }

    /* Показываем меню при наведении на dropdown контейнер */
    .dropdown:hover .dropdown-content {
        display: block;
        animation: fadeIn 0.6s ease-in;
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

    hr {
        border: none;
        height: 1px;
        background: rgba(255,255,255,.2);
        margin: 0;
    }

    </style>
    """, unsafe_allow_html=True)

    # ==== LAYOUT ====
    col_left, col_center, col_right = st.columns([2, 2, 2])

    # LEFT - HOME
    with col_left:
        if st.button("Home"):
            st.query_params["page"] = "home"
            st.rerun()

    # CENTER - LOGO (properly centered with container)
    with col_center:
        # Create a centered container
        st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%;">', unsafe_allow_html=True)
        # Use columns to center the image
        _, logo_col, _ = st.columns([1, 2, 1])
        with logo_col:
            st.image(logo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT - DROPDOWN with working hover
    with col_right:
        st.markdown("""
        <div style="display: flex; justify-content: flex-end;">
            <div class="dropdown">
                <button class="dropbtn">More ▾</button>
                <div class="dropdown-content">
                    <a href="?page=datasets">Datasets</a>
                    <a href="?page=faq">FAQ</a>
                    <a href="?page=about">About</a>
                    <a href="?page=account">My Account</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)