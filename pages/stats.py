import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.header import render_header


def app():
    # Render common header
    render_header(current_page="stats")

    # Apply Comic Sans and text outline
    st.markdown("""
    <style>
    * {
        font-family: "Comic Sans MS", "Comic Sans", cursive !important;
        text-shadow: 0px 0px 2px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Statistics and Analytics")
    st.markdown("---")

    # Load datasets with correct filenames
    try:
        budget_df = pd.read_csv("datasets/budget_groceries_expanded.csv")

        # Try to load middle income groceries with different encodings
        try:
            middle_df = pd.read_csv("datasets/middle_income_groceries.csv")
        except UnicodeDecodeError:
            middle_df = pd.read_csv("datasets/middle_income_groceries.csv", encoding='latin1')

        # Tabs for different statistics
        tab1, tab2, tab3, tab4 = st.tabs(
            ["📈 General Statistics", "💰 Price Comparison", "🥗 Calories & Nutrients", "📊 Product Categories"])

        # TAB 1: General statistics
        with tab1:
            st.subheader("Dataset Overview")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Budget Products",
                    len(budget_df),
                    delta="Records"
                )

            with col2:
                st.metric(
                    "Middle-income Products",
                    len(middle_df),
                    delta="Records"
                )

            with col3:
                avg_budget_Price_USD = budget_df['Price_USD'].mean() if 'Price_USD' in budget_df.columns else 0
                st.metric(
                    "Avg Price_USD (Budget)",
                    f"${avg_budget_Price_USD:.2f}",
                    delta="USD"
                )

            with col4:
                avg_middle_Price_USD = middle_df['Price_USD'].mean() if 'Price_USD' in middle_df.columns else 0
                st.metric(
                    "Avg Price_USD (Middle)",
                    f"${avg_middle_Price_USD:.2f}",
                    delta="USD"
                )

            st.markdown("---")

            # Price_USD distribution charts
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 Price_USD Distribution - Budget")
                if 'Price_USD' in budget_df.columns:
                    fig = px.histogram(
                        budget_df,
                        x='Price_USD',
                        nbins=30,
                        title="Price_USD Distribution in Budget Products",
                        color_discrete_sequence=['#8B4C4C']
                    )
                    fig.update_layout(
                        xaxis_title="Price_USD ($)",
                        yaxis_title="Product Count",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("'Price_USD' column not found in dataset")

            with col2:
                st.markdown("#### 📊 Price_USD Distribution - Middle Income")
                if 'Price_USD' in middle_df.columns:
                    fig = px.histogram(
                        middle_df,
                        x='Price_USD',
                        nbins=30,
                        title="Price_USD Distribution in Middle-income Products",
                        color_discrete_sequence=['#6B4423']
                    )
                    fig.update_layout(
                        xaxis_title="Price_USD ($)",
                        yaxis_title="Product Count",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("'Price_USD' column not found in dataset")

        # TAB 2: Price_USD comparison
        with tab2:
            st.subheader("💰 Price_USD Comparison by Category")

            if 'Category' in budget_df.columns and 'Price_USD' in budget_df.columns:
                # Aggregate data by categories
                budget_by_category = budget_df.groupby('Category')['Price_USD'].mean().reset_index()
                budget_by_category.columns = ['Category', 'Avg_Price_USD']
                budget_by_category['Type'] = 'Budget'

                if 'Category' in middle_df.columns and 'Price_USD' in middle_df.columns:
                    middle_by_category = middle_df.groupby('Category')['Price_USD'].mean().reset_index()
                    middle_by_category.columns = ['Category', 'Avg_Price_USD']
                    middle_by_category['Type'] = 'Middle Income'

                    # Combine
                    combined = pd.concat([budget_by_category, middle_by_category])

                    # Build grouped bar chart
                    fig = px.bar(
                        combined,
                        x='Category',
                        y='Avg_Price_USD',
                        color='Type',
                        barmode='group',
                        title="Average Price_USD by Category: Budget vs Middle Income",
                        color_discrete_map={
                            'Budget': '#8B4C4C',
                            'Middle Income': '#6B4423'
                        }
                    )
                    fig.update_layout(
                        xaxis_title="Category",
                        yaxis_title="Average Price_USD ($)",
                        legend_title="Budget Type"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Comparison table
                    st.markdown("#### 📋 Detailed Comparison")
                    pivot_table = combined.pivot(index='Category', columns='Type', values='Avg_Price_USD')
                    pivot_table['Difference (%)'] = (
                                (pivot_table['Middle Income'] - pivot_table['Budget']) / pivot_table[
                            'Budget'] * 100).round(2)
                    st.dataframe(pivot_table, use_container_width=True)
                else:
                    st.warning("Could not find Category and Price_USD columns in middle_df")
            else:
                st.warning("Could not find Category and Price_USD columns in budget_df")

        # TAB 3: Calories and nutrients
        with tab3:
            st.subheader("🥗 Calories and Nutrient Analysis")

            # Check for Calories column
            calorie_columns = ['Calories', 'calories', 'Калории', 'калории']
            calorie_col = None

            for col in calorie_columns:
                if col in budget_df.columns:
                    calorie_col = col
                    break

            if calorie_col:
                col1, col2 = st.columns(2)

                with col1:
                    # Top 10 highest Calories products
                    top_calories = budget_df.nlargest(10, calorie_col)[['Product', calorie_col]]

                    fig = px.bar(
                        top_calories,
                        x=calorie_col,
                        y='Product',
                        orientation='h',
                        title="Top 10 Highest Calories Products",
                        color=calorie_col,
                        color_continuous_scale='Reds'
                    )
                    fig.update_layout(
                        xaxis_title="Calories",
                        yaxis_title="Product",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Calories distribution by category
                    if 'Category' in budget_df.columns:
                        calories_by_cat = budget_df.groupby('Category')[calorie_col].mean().reset_index()

                        fig = px.pie(
                            calories_by_cat,
                            values=calorie_col,
                            names='Category',
                            title="Average Calories by Category",
                            color_discrete_sequence=px.colors.sequential.RdBu
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Category column not found")

                # Statistics
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Average Calories", f"{budget_df[calorie_col].mean():.0f}")
                with col2:
                    st.metric("Median Calories", f"{budget_df[calorie_col].median():.0f}")
                with col3:
                    st.metric("Maximum", f"{budget_df[calorie_col].max():.0f}")
                with col4:
                    st.metric("Minimum", f"{budget_df[calorie_col].min():.0f}")
            else:
                st.info("📊 Calories column not found in dataset. Possible names: Calories, calories")

        # TAB 4: Product categories
        with tab4:
            st.subheader("📊 Product Category Analysis")

            if 'Category' in budget_df.columns:
                col1, col2 = st.columns(2)

                with col1:
                    # Category distribution in Budget
                    category_counts = budget_df['Category'].value_counts().reset_index()
                    category_counts.columns = ['Category', 'Count']

                    fig = px.bar(
                        category_counts,
                        x='Category',
                        y='Count',
                        title="Product Count by Category (Budget)",
                        color='Count',
                        color_continuous_scale='Reds'
                    )
                    fig.update_layout(
                        xaxis_title="Category",
                        yaxis_title="Product Count",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Pie chart
                    fig = px.pie(
                        category_counts,
                        values='Count',
                        names='Category',
                        title="Category Share in Assortment",
                        color_discrete_sequence=px.colors.sequential.RdBu
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Detailed table
                st.markdown("---")
                st.markdown("#### 📋 Detailed Statistics by Category")

                if 'Price_USD' in budget_df.columns:
                    category_stats = budget_df.groupby('Category').agg({
                        'Product': 'count',
                        'Price_USD': ['mean', 'min', 'max']
                    }).round(2)
                    category_stats.columns = ['Product Count', 'Average Price_USD', 'Min Price_USD', 'Max Price_USD']
                    st.dataframe(category_stats, use_container_width=True)
                else:
                    st.dataframe(category_counts, use_container_width=True)
            else:
                st.warning("'Category' column not found in dataset")

    except FileNotFoundError as e:
        st.error(f"❌ Error loading datasets: {str(e)}")
        st.info("""
        Make sure the following CSV files are in the 'datasets/' folder:
        - budget_groceries_expanded.csv
        - middle_income_groceries.csv
        - mealplan_starter.csv
        - middle_income_mealplan.csv
        """)
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Check the format and structure of your datasets")