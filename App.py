import streamlit as st

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="MPFU - Meal Plans Generator", 
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global CSS - applies to all pages
st.markdown("""
<style>
* { font-family: 'Comic Sans MS', 'Comic Sans', cursive !important; }

    /* Force light theme with gradient background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #8B4C4C 0%, #F5E6D3 100%) !important;
    }
    
    .stApp {
        color: #000000 !important;
    }
    
    /* Hide Streamlit's default header */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Prevent body scroll, only allow content scroll */
    html, body {
        overflow: hidden !important;
        height: 100% !important;
        position: fixed !important;
        width: 100% !important;
    }
    
    #root, .stApp {
        overflow: hidden !important;
        height: 100vh !important;
        position: relative !important;
    }
    
    /* Main container scrolls */
    .main {
        overflow-y: scroll !important;
        overflow-x: hidden !important;
        height: 100vh !important;
        overscroll-behavior: contain !important;
        position: relative !important;
        margin-left: 0 !important;
    }
    
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem;
        max-width: 100% !important;
    }
    
    /* Text shadow for better readability */
    h1, h2, h3, p, span, div {
        text-shadow: 0px 0px 3px rgba(0,0,0,0.3);
    }
    
    /* Hide resize handles on dataframes */
    .stDataFrame [data-testid="stDataFrameResizeHandle"] {
        display: none !important;
    }
    
    .stDataFrame {
        pointer-events: none !important;
    }
    
    .stDataFrame > div {
        pointer-events: auto !important;
    }
</style>
""", unsafe_allow_html=True)

# Get page from query params
query_params = st.query_params
page = query_params.get("page", "home")

# Route to appropriate page
if page == "home":
    import pages.home as home
    home.app()
elif page == "account":
    import pages.account as account
    account.app()
elif page == "stats":
    import pages.stats as stats
    stats.app()
elif page == "datasets":
    import pages.datasets as datasets
    datasets.app()
elif page == "faq":
    import pages.faq as faq
    faq.app()
elif page == "about":
    import pages.abtus as abtus
    abtus.app()
else:
    # Default to home page
    import pages.home as home
    home.app()