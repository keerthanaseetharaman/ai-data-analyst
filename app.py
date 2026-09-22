import streamlit as st
import pandas as pd
import sqlite3
import io

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("🤖 AI Data Analyst")
st.write(
    "Upload your CSV or Excel file and analyze your data "
    "using Python, Pandas, SQL and AI-powered insights."
)

# ============================================================
# FILE UPLOAD
# ============================================================

st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx"]
)

# ============================================================
# MAIN APPLICATION
# ============================================================

if uploaded_file is not None:

    # --------------------------------------------------------
    # READ FILE
    # --------------------------------------------------------

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        # Remove completely empty rows
        df = df.dropna(how="all")

        st.success("✅ File uploaded successfully!")

        # ====================================================
        # DATASET OVERVIEW
        # ====================================================

        st.header("📋 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Rows",
                df.shape[0]
            )

        with col2:
            st.metric(
                "Columns",
                df.shape[1]
            )

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        with col4:
            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum())
            )

        # ====================================================
        # DATASET PREVIEW
        # ====================================================

        st.header("📊 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ====================================================
        # DATA QUALITY CHECK
        # ====================================================

        st.header("🧹 Data Quality Check")

        missing_values = int(df.isnull().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        if missing_values == 0:
            st.success("✅ No missing values found!")

        else:
            st.warning(
                f"⚠️ {missing_values} missing values found."
            )

            st.dataframe(
                df.isnull().sum()
            )

        if duplicate_rows == 0:
            st.success("✅ No duplicate rows found!")

        else:
            st.warning(
                f"⚠️ {duplicate_rows} duplicate rows found."
            )

        # ====================================================
        # NUMERIC DATA SUMMARY
        # ====================================================

        st.header("💰 Numeric Data Summary")

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if len(numeric_columns) > 0:

            summary = df[numeric_columns].describe().T

            st.dataframe(
                summary,
                use_container_width=True
            )

        else:

            st.info(
                "No numeric columns available in this dataset."
            )

        # ====================================================
        # SALES / PROFIT SUMMARY
        # ====================================================

        if "Sales" in df.columns and "Profit" in df.columns:

            st.header("💵 Sales & Profit Summary")

            total_sales = df["Sales"].sum()
            average_sales = df["Sales"].mean()
            maximum_sales = df["Sales"].max()
            minimum_sales = df["Sales"].min()

            total_profit = df["Profit"].sum()
            average_profit = df["Profit"].mean()
            maximum_profit = df["Profit"].max()
            minimum_profit = df["Profit"].min()

            # Sales row

            st.subheader("📈 Sales")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Sales Total",
                    f"₹{total_sales:,.0f}"
                )

            with col2:
                st.metric(
                    "Sales Average",
                    f"₹{average_sales:,.2f}"
                )

            with col3:
                st.metric(
                    "Sales Maximum",
                    f"₹{maximum_sales:,.0f}"
                )

            with col4:
                st.metric(
                    "Sales Minimum",
                    f"₹{minimum_sales:,.0f}"
                )

            # Profit row

            st.subheader("💰 Profit")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Profit Total",
                    f"₹{total_profit:,.0f}"
                )

            with col2:
                st.metric(
                    "Profit Average",
                    f"₹{average_profit:,.2f}"
                )

            with col3:
                st.metric(
                    "Profit Maximum",
                    f"₹{maximum_profit:,.0f}"
                )

            with col4:
                st.metric(
                    "Profit Minimum",
                    f"₹{minimum_profit:,.0f}"
                )

        # ====================================================
        # TOP CATEGORIES
        # ====================================================

        if "Product" in df.columns and "Sales" in df.columns:

            st.header("🏆 Top Categories")

            product_sales = (
                df.groupby("Product")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.dataframe(
                product_sales.reset_index(
                    name="Total Sales"
                ),
                use_container_width=True
            )

        # ====================================================
        # INTERACTIVE DATA VISUALIZATION
        # ====================================================

        st.header("📊 Interactive Data Visualization")

        if "Product" in df.columns and "Sales" in df.columns:

            st.subheader("Sales by Product")

            product_sales = (
                df.groupby("Product")["Sales"]
                .sum()
            )

            st.bar_chart(product_sales)

        if "City" in df.columns and "Sales" in df.columns:

            st.subheader("Sales by City")

            city_sales = (
                df.groupby("City")["Sales"]
                .sum()
            )

            st.bar_chart(city_sales)

        if "Product" in df.columns and "Profit" in df.columns:

            st.subheader("Profit by Product")

            product_profit = (
                df.groupby("Product")["Profit"]
                .sum()
            )

            st.bar_chart(product_profit)

        # ====================================================
        # SQL ANALYSIS
        # ====================================================

        st.header("🗄️ SQL Data Analysis")

        st.write(
            "Use SQL queries to analyze the uploaded dataset."
        )

        if len(df) > 0:

            connection = sqlite3.connect(":memory:")

            df.to_sql(
                "sales",
                connection,
                index=False,
                if_exists="replace"
            )

            default_query = ""

            if "Product" in df.columns and "Sales" in df.columns:

                default_query = """
SELECT Product, SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Product
ORDER BY Total_Sales DESC;
"""

            else:

                default_query = "SELECT * FROM sales LIMIT 10;"

            st.code(
                default_query,
                language="sql"
            )

            sql_query = st.text_area(
                "Enter your SQL query:",
                value=default_query,
                height=150
            )

            if st.button(
                "▶️ Run SQL Query"
            ):

                try:

                    result = pd.read_sql_query(
                        sql_query,
                        connection
                    )

                    st.success(
                        "✅ Query executed successfully!"
                    )

                    st.dataframe(
                        result,
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"❌ SQL Error: {e}"
                    )

        # ====================================================
        # ASK AI DATA ANALYST
        # ====================================================

        st.header("🤖 Ask AI Data Analyst")

        st.write(
            "Ask questions about your uploaded dataset "
            "using normal English."
        )

        question = st.text_input(
            "💬 Ask your question:",
            placeholder="Example: Which product has the highest sales?"
        )

        if st.button(
            "🤖 Analyze Question"
        ):

            if question.strip() == "":
                st.warning(
                    "Please enter a question."
                )

            else:

                question_lower = question.lower()

                # --------------------------------------------
                # HIGHEST SALES
                # --------------------------------------------

                if (
                    "highest sales" in question_lower
                    or "maximum sales" in question_lower
                    or "top product" in question_lower
                ):

                    if (
                        "Product" in df.columns
                        and "Sales" in df.columns
                    ):

                        product_sales = (
                            df.groupby("Product")["Sales"]
                            .sum()
                        )

                        top_product = product_sales.idxmax()
                        top_value = product_sales.max()

                        st.success(
                            f"🏆 {top_product} has the highest "
                            f"sales with ₹{top_value:,.0f}."
                        )

                        result = product_sales.reset_index(
                            name="Total Sales"
                        )

                        st.dataframe(
                            result,
                            use_container_width=True
                        )

                # --------------------------------------------
                # LOWEST SALES
                # --------------------------------------------

                elif (
                    "lowest sales" in question_lower
                    or "minimum sales" in question_lower
                    or "least sales" in question_lower
                ):

                    if (
                        "Product" in df.columns
                        and "Sales" in df.columns
                    ):

                        product_sales = (
                            df.groupby("Product")["Sales"]
                            .sum()
                        )

                        lowest_product = product_sales.idxmin()
                        lowest_value = product_sales.min()

                        st.info(
                            f"📉 {lowest_product} has the lowest "
                            f"sales with ₹{lowest_value:,.0f}."
                        )

                # --------------------------------------------
                # HIGHEST PROFIT
                # --------------------------------------------

                elif (
                    "highest profit" in question_lower
                    or "maximum profit" in question_lower
                ):

                    if (
                        "Product" in df.columns
                        and "Profit" in df.columns
                    ):

                        product_profit = (
                            df.groupby("Product")["Profit"]
                            .sum()
                        )

                        top_product = product_profit.idxmax()
                        top_value = product_profit.max()

                        st.success(
                            f"💰 {top_product} has the highest "
                            f"profit with ₹{top_value:,.0f}."
                        )

                # --------------------------------------------
                # TOTAL SALES
                # --------------------------------------------

                elif (
                    "total sales" in question_lower
                    or "sales total" in question_lower
                ):

                    if "Sales" in df.columns:

                        total = df["Sales"].sum()

                        st.info(
                            f"💵 Total sales are "
                            f"₹{total:,.0f}."
                        )

                # --------------------------------------------
                # TOTAL PROFIT
                # --------------------------------------------

                elif (
                    "total profit" in question_lower
                    or "profit total" in question_lower
                ):

                    if "Profit" in df.columns:

                        total = df["Profit"].sum()

                        st.info(
                            f"💰 Total profit is "
                            f"₹{total:,.0f}."
                        )

                # --------------------------------------------
                # BEST CITY
                # --------------------------------------------

                elif (
                    "best city" in question_lower
                    or "highest city sales" in question_lower
                ):

                    if (
                        "City" in df.columns
                        and "Sales" in df.columns
                    ):

                        city_sales = (
                            df.groupby("City")["Sales"]
                            .sum()
                        )

                        best_city = city_sales.idxmax()
                        best_value = city_sales.max()

                        st.success(
                            f"🏙️ {best_city} generated the "
                            f"highest sales with ₹{best_value:,.0f}."
                        )

                else:

                    st.info(
                        "🤖 Try questions like:\n\n"
                        "- Which product has the highest sales?\n"
                        "- Which product has the lowest sales?\n"
                        "- Which product has the highest profit?\n"
                        "- What is the total sales?\n"
                        "- What is the total profit?\n"
                        "- Which city has the highest sales?"
                    )

        # ====================================================
        # STAGE 6 - AI BUSINESS INSIGHTS
        # ====================================================

        st.markdown("---")

        st.header("💡 AI Business Insights")

        if (
            "Product" in df.columns
            and "Sales" in df.columns
            and "Profit" in df.columns
        ):

            total_sales = df["Sales"].sum()
            total_profit = df["Profit"].sum()

            product_sales = (
                df.groupby("Product")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            product_profit = (
                df.groupby("Product")["Profit"]
                .sum()
                .sort_values(ascending=False)
            )

            highest_sales_product = (
                product_sales.index[0]
            )

            highest_sales_value = (
                product_sales.iloc[0]
            )

            highest_profit_product = (
                product_profit.index[0]
            )

            highest_profit_value = (
                product_profit.iloc[0]
            )

            lowest_sales_product = (
                product_sales.index[-1]
            )

            # --------------------------------------------
            # CITY ANALYSIS
            # --------------------------------------------

            if "City" in df.columns:

                city_sales = (
                    df.groupby("City")["Sales"]
                    .sum()
                    .sort_values(ascending=False)
                )

                best_city = city_sales.index[0]
                best_city_sales = city_sales.iloc[0]

            else:

                best_city = "Not available"
                best_city_sales = 0

            # --------------------------------------------
            # METRICS
            # --------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "💰 Total Sales",
                    f"₹{total_sales:,.0f}"
                )

            with col2:

                st.metric(
                    "📈 Total Profit",
                    f"₹{total_profit:,.0f}"
                )

            with col3:

                st.metric(
                    "🏆 Top Product",
                    highest_sales_product
                )

            # --------------------------------------------
            # KEY FINDINGS
            # --------------------------------------------

            st.subheader("🔍 Key Findings")

            st.success(
                f"💻 {highest_sales_product} generated the "
                f"highest sales with "
                f"₹{highest_sales_value:,.0f}."
            )

            st.info(
                f"💰 {highest_profit_product} generated the "
                f"highest profit with "
                f"₹{highest_profit_value:,.0f}."
            )

            st.warning(
                f"📉 {lowest_sales_product} has the lowest "
                f"total sales among the products."
            )

            if "City" in df.columns:

                st.success(
                    f"🏙️ {best_city} generated the highest "
                    f"sales with "
                    f"₹{best_city_sales:,.0f}."
                )

            # --------------------------------------------
            # RECOMMENDATIONS
            # --------------------------------------------

            st.subheader(
                "💡 Business Recommendations"
            )

            st.write(
                f"• Focus more on **{highest_sales_product}**, "
                "which currently has the highest sales."
            )

            st.write(
                f"• Analyze why **{lowest_sales_product}** "
                "has lower sales."
            )

            st.write(
                f"• Monitor **{highest_profit_product}** "
                "because it generates the highest profit."
            )

        # ====================================================
        # STAGE 7 - INTERACTIVE DASHBOARD FILTERS
        # ====================================================

        st.markdown("---")

        st.header("🎛️ Interactive Dashboard")

        filtered_df = df.copy()

        # ----------------------------------------------------
        # PRODUCT FILTER
        # ----------------------------------------------------

        if "Product" in df.columns:

            products = (
                df["Product"]
                .dropna()
                .unique()
                .tolist()
            )

            products = sorted(products)

            product_options = ["All"] + products

            selected_product = st.selectbox(
                "💻 Select Product",
                product_options
            )

            if selected_product != "All":

                filtered_df = filtered_df[
                    filtered_df["Product"]
                    == selected_product
                ]

        # ----------------------------------------------------
        # CITY FILTER
        # ----------------------------------------------------

        if "City" in df.columns:

            cities = (
                df["City"]
                .dropna()
                .unique()
                .tolist()
            )

            cities = sorted(cities)

            city_options = ["All"] + cities

            selected_city = st.selectbox(
                "🏙️ Select City",
                city_options
            )

            if selected_city != "All":

                filtered_df = filtered_df[
                    filtered_df["City"]
                    == selected_city
                ]

        # ----------------------------------------------------
        # FILTERED METRICS
        # ----------------------------------------------------

        st.subheader("📊 Filtered Data")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Rows",
                len(filtered_df)
            )

        with col2:

            if "Sales" in filtered_df.columns:

                filtered_sales = (
                    filtered_df["Sales"].sum()
                )

                st.metric(
                    "Sales",
                    f"₹{filtered_sales:,.0f}"
                )

        with col3:

            if "Profit" in filtered_df.columns:

                filtered_profit = (
                    filtered_df["Profit"].sum()
                )

                st.metric(
                    "Profit",
                    f"₹{filtered_profit:,.0f}"
                )

        # ----------------------------------------------------
        # FILTERED TABLE
        # ----------------------------------------------------

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

        # ----------------------------------------------------
        # FILTERED CHART
        # ----------------------------------------------------

        if (
            "Product" in filtered_df.columns
            and "Sales" in filtered_df.columns
            and len(filtered_df) > 0
        ):

            st.subheader(
                "📈 Filtered Sales by Product"
            )

            filtered_product_sales = (
                filtered_df
                .groupby("Product")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.bar_chart(
                filtered_product_sales
            )

        # ====================================================
        # DOWNLOAD FILTERED DATA
        # ====================================================

        st.subheader("⬇️ Download Data")

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="filtered_data.csv",
            mime="text/csv"
        )

        # ====================================================
        # FOOTER
        # ====================================================

        st.markdown("---")

        st.caption(
            "AI Data Analyst | Python • Pandas • SQL • Streamlit • Data Analytics"
        )

    except Exception as e:

        st.error(
            f"❌ Error while processing the file: {e}"
        )

else:

    st.info(
        "👆 Please upload a CSV or Excel file to begin."
    )