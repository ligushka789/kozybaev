import streamlit as st

# Настройки страницы — ТОЛЬКО здесь!
st.set_page_config(
    page_title="MPFU - Meal Plans Generator",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ПРИНУДИТЕЛЬНО СВЕТЛАЯ ТЕМА + СКРЫВАЕМ sidebar + УБИРАЕМ ВСТРОЕННЫЙ ХЕДЕР
st.markdown("""
<style>
    /* ПРИНУДИТЕЛЬНАЯ СВЕТЛАЯ ТЕМА */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #8B4C4C 0%, #F5E6D3 100%) !important;
    }
    
    /* Цвет текста по умолчанию */
    .stApp {
        color: #000000 !important;
    }
    
    /* УБИРАЕМ ВСТРОЕННЫЙ ХЕДЕР STREAMLIT */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* ПОЛНОСТЬЮ СКРЫВАЕМ SIDEBAR */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* ПОЛНАЯ БЛОКИРОВКА скролла на всех уровнях кроме контента */
    html {
        overflow: hidden !important;
        height: 100% !important;
        position: fixed !important;
        width: 100% !important;
    }
    
    body {
        overflow: hidden !important;
        height: 100% !important;
        position: fixed !important;
        width: 100% !important;
        overscroll-behavior-y: none !important;
    }
    
    #root, .stApp {
        overflow: hidden !important;
        height: 100vh !important;
        position: relative !important;
    }
    
    /* Основной контейнер - ТОЛЬКО здесь скролл */
    .main {
        overflow-y: scroll !important;
        overflow-x: hidden !important;
        height: 100vh !important;
        overscroll-behavior: contain !important;
        position: relative !important;
        margin-left: 0 !important;
    }
    
    /* Убираем верхний padding */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem;
        max-width: 100% !important;
    }
    
    /* Отключаем изменение размера таблиц */
    .stDataFrame [data-testid="stDataFrameResizeHandle"] {
        display: none !important;
    }
    
    .stDataFrame {
        pointer-events: none !important;
    }
    
    .stDataFrame > div {
        pointer-events: auto !important;
    }
    
    /* Градиентный фон для всего приложения */
    .stApp {
        background: linear-gradient(180deg, #8B4C4C 0%, #F5E6D3 100%) !important;
    }
    
    /* Контур для белого текста */
    h1, h2, h3, p, span, div {
        text-shadow: 0px 0px 3px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Получаем параметр страницы из URL
query_params = st.query_params
page = query_params.get("page", "test")  # Изменено с "home" на "test"

# Переход между страницами
if page == "test":
    import pages.test as test
    test.app()
elif page == "home":
    import pages.home as home
    home.app()
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
    # По умолчанию показываем тест
    import pages.test as test
    test.app()