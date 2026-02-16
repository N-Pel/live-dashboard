import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIG
# ==============================

SHEET_ID = "1YZW1ENJdB1n910lvtCilbG776d0HrudGV163XZzsQqA"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/1YZW1ENJdB1n910lvtCilbG776d0HrudGV163XZzsQqA/edit?usp=sharing"

st.set_page_config(layout="wide")

# ==============================
# DATA LOAD
# ==============================

@st.cache_data(ttl=30)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# ==============================
# KPI CALCULATIONS
# ==============================

total_revenue = df["total_revenue"].sum()
total_orders = df["order_id"].nunique()
avg_rating = df["rating"].mean()
total_quantity = df["quantity_sold"].sum()

# ==============================
# DASHBOARD TITLE
# ==============================

st.title("📊 Sales Performance Dashboard")

# ==============================
# KPI ROW
# ==============================

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"€ {total_revenue:,.2f}")
col2.metric("📦 Total Orders", f"{total_orders:,}")
col3.metric("⭐ Avg Rating", f"{avg_rating:.2f}")
col4.metric("🛒 Quantity Sold", f"{total_quantity:,}")

st.markdown("---")

# ==============================
# FILTERS
# ==============================

colf1, colf2 = st.columns(2)

with colf1:
    selected_category = st.multiselect(
        "Filter by Category",
        df["product_category"].unique(),
        default=df["product_category"].unique()
    )

with colf2:
    selected_region = st.multiselect(
        "Filter by Region",
        df["customer_region"].unique(),
        default=df["customer_region"].unique()
    )

filtered_df = df[
    (df["product_category"].isin(selected_category)) &
    (df["customer_region"].isin(selected_region))
]

# ==============================
# REVENUE TREND
# ==============================

st.subheader("Revenue Trend")

monthly_revenue = (
    filtered_df.groupby("month")["total_revenue"]
    .sum()
    .reset_index()
)

fig_trend = px.line(
    monthly_revenue,
    x="month",
    y="total_revenue",
    markers=True,
    template="plotly_white"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ==============================
# CATEGORY & REGION CHARTS
# ==============================

col5, col6 = st.columns(2)

with col5:
    st.subheader("Revenue by Category")
    category_revenue = (
        filtered_df.groupby("product_category")["total_revenue"]
        .sum()
        .reset_index()
    )

    fig_cat = px.bar(
        category_revenue,
        x="product_category",
        y="total_revenue",
        template="plotly_white"
    )

    st.plotly_chart(fig_cat, use_container_width=True)

with col6:
    st.subheader("Revenue by Region")
    region_revenue = (
        filtered_df.groupby("customer_region")["total_revenue"]
        .sum()
        .reset_index()
    )

    fig_region = px.bar(
        region_revenue,
        x="customer_region",
        y="total_revenue",
        template="plotly_white"
    )

    st.plotly_chart(fig_region, use_container_width=True)

# ==============================
# PAYMENT METHOD PIE
# ==============================

st.subheader("Payment Method Distribution")

payment_counts = (
    filtered_df["payment_method"]
    .value_counts()
    .reset_index()
)

payment_counts.columns = ["payment_method", "count"]

fig_payment = px.pie(
    payment_counts,
    names="payment_method",
    values="count",
    template="plotly_white"
)

st.plotly_chart(fig_payment, use_container_width=True)
