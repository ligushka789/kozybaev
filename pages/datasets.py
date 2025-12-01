import streamlit as st
import pandas as pd
import os
from pages.header import render_header


def app():
    # Render common header
    render_header(current_page="datasets")

    # Apply Comic Sans and text outline
    st.markdown("""
    <style>
    
    * {
        font-family: 'Comic Neue', cursive;
        text-shadow: 0px 0px 2px rgba(0,0,0,0.5);
    }

    /* Hide navigation arrows in dataframe */
    button[data-testid="StyledFullScreenButton"],
    button[kind="icon"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📂 Datasets Explorer")
    st.write("Select a dataset to view and analyze")

    # Get list of all CSV files from datasets folder
    datasets_folder = "datasets"

    # Specific datasets to look for
    available_datasets = {
        "Budget Groceries (Expanded)": "budget_groceries_expanded.csv",
        "Meal Plan Starter": "mealplan_starter.csv",
        "Middle Income Groceries": "middle_income_groceries.csv",
        "Middle Income Meal Plan": "middle_income_mealplan.csv"
    }

    try:
        # Check which datasets exist
        existing_datasets = {}
        for name, filename in available_datasets.items():
            file_path = os.path.join(datasets_folder, filename)
            if os.path.exists(file_path):
                existing_datasets[name] = filename

        if not existing_datasets:
            st.warning("⚠️ No datasets found in datasets folder. Please add the following files:")
            for name, filename in available_datasets.items():
                st.write(f"• {filename}")
            return

        # Context menu for dataset selection
        selected_name = st.selectbox(
            "🔍 Select dataset:",
            list(existing_datasets.keys()),
            index=0
        )

        selected_file = existing_datasets[selected_name]

        # Load selected dataset
        file_path = os.path.join(datasets_folder, selected_file)

        try:
            # Try loading with different encodings
            try:
                df = pd.read_csv(file_path)
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='latin1')

            st.success(f"✅ Loaded dataset: **{selected_name}** ({selected_file})")

            # Dataset information
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Rows", df.shape[0])
            with col2:
                st.metric("Columns", df.shape[1])
            with col3:
                st.metric("Memory Size", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            with col4:
                st.metric("Missing Values", df.isnull().sum().sum())

            st.markdown("---")

            # Filter panel
            with st.expander("🔧 Filters and Settings", expanded=True):
                filter_col1, filter_col2 = st.columns(2)

                with filter_col1:
                    # Select columns to display
                    all_columns = df.columns.tolist()
                    selected_columns = st.multiselect(
                        "Select columns to display:",
                        all_columns,
                        default=all_columns
                    )

                with filter_col2:
                    # Number of rows to display
                    num_rows = st.slider(
                        "Number of rows:",
                        min_value=5,
                        max_value=max(len(df), 10),
                        value=min(50, len(df)),
                        step=5
                    )

                # Filter by column values
                st.markdown("**Filters by values:**")
                filter_col3, filter_col4 = st.columns(2)

                with filter_col3:
                    # Select column for filtering
                    filter_column = st.selectbox(
                        "Column for filtering:",
                        ["None"] + all_columns
                    )

                filtered_df = df.copy()

                if filter_column != "None":
                    with filter_col4:
                        # Determine column data type
                        if pd.api.types.is_numeric_dtype(df[filter_column]):
                            # For numeric data - range
                            try:
                                min_val = float(df[filter_column].min())
                                max_val = float(df[filter_column].max())

                                if min_val < max_val:
                                    value_range = st.slider(
                                        f"{filter_column} range:",
                                        min_value=min_val,
                                        max_value=max_val,
                                        value=(min_val, max_val)
                                    )
                                    filtered_df = filtered_df[
                                        (filtered_df[filter_column] >= value_range[0]) &
                                        (filtered_df[filter_column] <= value_range[1])
                                        ]
                                else:
                                    st.info(f"Column '{filter_column}' has only one value: {min_val}")
                            except Exception as e:
                                st.warning(f"Cannot create filter for column '{filter_column}'")
                        else:
                            # For text data - multiselect
                            unique_values = df[filter_column].unique().tolist()
                            selected_values = st.multiselect(
                                f"{filter_column} values:",
                                unique_values,
                                default=unique_values
                            )
                            filtered_df = filtered_df[filtered_df[filter_column].isin(selected_values)]

                # Text search
                search_query = st.text_input("🔎 Search across all columns:")
                if search_query:
                    mask = filtered_df.astype(str).apply(
                        lambda x: x.str.contains(search_query, case=False, na=False)
                    ).any(axis=1)
                    filtered_df = filtered_df[mask]

                # Sorting
                sort_col1, sort_col2 = st.columns(2)
                with sort_col1:
                    sort_column = st.selectbox(
                        "Sort by:",
                        ["None"] + all_columns
                    )
                with sort_col2:
                    if sort_column != "None":
                        sort_order = st.radio(
                            "Order:",
                            ["Ascending", "Descending"],
                            horizontal=True
                        )
                        filtered_df = filtered_df.sort_values(
                            by=sort_column,
                            ascending=(sort_order == "Ascending")
                        )

            st.markdown("---")

            # Display filtered data
            if selected_columns:
                display_df = filtered_df[selected_columns].head(num_rows)
                st.dataframe(display_df, use_container_width=True, height=400)

                st.info(f"📊 Rows displayed: {len(display_df)} of {len(filtered_df)} (total in dataset: {len(df)})")
            else:
                st.warning("Select at least one column to display")

            # Additional statistics
            with st.expander("📈 Dataset Statistics"):
                stat_col1, stat_col2 = st.columns(2)

                with stat_col1:
                    st.markdown("**Numeric columns:**")
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if numeric_cols:
                        st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                    else:
                        st.write("No numeric columns")

                with stat_col2:
                    st.markdown("**Data types:**")
                    dtype_df = pd.DataFrame({
                        'Column': df.dtypes.index,
                        'Type': df.dtypes.values.astype(str)
                    })
                    st.dataframe(dtype_df, use_container_width=True, height=300)

            # Download filtered data
            st.markdown("---")
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download filtered data (CSV)",
                data=csv,
                file_name=f"filtered_{selected_file}",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Error loading dataset: {str(e)}")
            st.info("Please check the file format and encoding.")

    except Exception as e:
        st.error(f"❌ Error reading datasets folder: {str(e)}")