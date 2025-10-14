import streamlit as st
from streamlit_navigation_bar import st_navbar

# Настройки страницы — ТОЛЬКО здесь!
st.set_page_config(page_title="Kazakhstanian Internalization yopta", layout="wide")

# Навигационное меню
page = st_navbar(
    ["home", "stats", "datasets", "abtus"],
    options={"show_menu": False}
)

# Переход между страницами
if page == "home":
    import pages.home as home
    home.app()
elif page == "stats":
    import pages.stats as stats
    stats.app()
elif page == "datasets":
    import pages.datasets as datasets
    datasets.app()
elif page == "abtus":
    import pages.abtus as abtus
    abtus.app()
