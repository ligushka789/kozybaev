import streamlit as st
import pandas as pd

def app():
    st.title("🏠 Home Page")
    st.write("""
    This is our minimum viable product, a preview what's about to come in our final project. The sole purpose of this page is to check the feasibility of the idea and visually explore possible final look of our product:
    """)

    # Загружаем датасеты
    mealplan_df = pd.read_csv("datasets/mealplan_starter.csv")
    budget_df = pd.read_csv("datasets/budget_groceries_expanded.csv")

    # Создаем три колонки
    col1, col2, col3 = st.columns(3)

    # --- БЛОК 1 ---
    with col1:
        st.markdown("### 🥗 Block 1: Budget Options")
        st.write("Dataset с бюджетными продуктами и примером мил-плана студента.")

        st.markdown("**Meal Plan Starter:**")
        st.dataframe(mealplan_df, use_container_width=True, height=250)

        st.markdown("**Budget Groceries Expanded:**")
        st.dataframe(budget_df, use_container_width=True, height=300)
        st.markdown("---")

    # --- БЛОК 2 ---
    with col2:
        st.markdown("### 🔸 Block 2: Healthy Options")
        st.write("Это второй блок. Например, сюда можно вставить график, визуализацию или сравнение цен.")
        st.markdown("---")

    # --- БЛОК 3 ---
    with col3:
        st.markdown("### 🔹 Блок 3")
        st.write("Это третий блок. Здесь можно будет добавить аналитику или статистику.")
        st.markdown("---")

    # --- БЛОК 4 ---
    st.markdown("### 🏬 Block 4: Walmart Full Product Base")
    st.write("Этот блок предназначен для будущего расширения — здесь будет полная база продуктов Walmart для сортировки и рекомендаций.")
    st.info("На данном этапе этот блок — просто placeholder под будущие данные.")

    # --- CSS фикс скролла ---
    st.markdown("""
    <style>
/* Разрешаем вертикальный скролл на всей странице */
html, body, [class*="block-container"], .main {
    overflow-y: auto !important;
    height: auto !important;
}

/* Чиним, если nav-bar или Streamlit контейнеры скрывают скролл */
section.main, div.block-container {
    overflow-y: visible !important;
}

/* Убираем любое global overflow:hidden, если оно где-то применилось */
*[style*="overflow: hidden"] {
    overflow: visible !important;
}

/* Добавляем запас снизу, чтобы последний блок не упирался */
.block-container {
    padding-bottom: 6rem !important;
}
</style>
    """, unsafe_allow_html=True)
