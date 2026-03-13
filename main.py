from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import plotly.express as px

# PAGE CONFIG

st.set_page_config(
    page_title="Superstore Dashboard",
    layout="wide"
)

st.title("📊 Superstore Sales Dashboard")
st.markdown("Analyse des ventes par région, catégorie et période")

#  DATABASE CONNECTION

try:

    db_url = "postgresql://postgres:admin@localhost:5432/superstore_db"
    engine = create_engine(db_url)

    st.success("Connexion PostgreSQL réussie")

except Exception as e:

    st.error(f"Erreur connexion DB : {e}")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():

    df_orders = pd.read_sql("SELECT * FROM orders", engine)
    df_customer = pd.read_sql("SELECT * FROM customer", engine)
    df_location = pd.read_sql("SELECT * FROM location", engine)
    df_order_details = pd.read_sql("SELECT * FROM order_details", engine)
    df_product = pd.read_sql("SELECT * FROM product", engine)

    # Merge tables
    df = pd.merge(df_orders, df_order_details, on="order_id")
    df = pd.merge(df, df_customer, on="customer_id")
    df = pd.merge(df, df_product, on="product_id")
    df = pd.merge(df, df_location, on="postal_code")

    return df


df = load_data()

# DATA PREPARATION

df["profit"] = df["sales"] - df["cost"]

df["margin"] = df["profit"] / df["sales"]

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month

# BASIC STATISTICS

stats = df[["sales", "profit"]].agg(["mean", "median", "min", "max", "std"])

st.subheader("Statistiques ventes et profits")

st.dataframe(stats)

# KPIs
total_sales = df["sales"].sum()

total_profit = df["profit"].sum()

avg_margin = df["margin"].mean()

total_orders = df["order_id"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📊 Profit Margin", f"{avg_margin:.2%}")
col4.metric("🧾 Total Orders", total_orders)

# SIDEBAR FILTERS
st.sidebar.header("Filtres")

region_filter = st.sidebar.multiselect(
    "Region",
    df["region"].dropna().unique(),
    default=df["region"].dropna().unique()
)

category_filter = st.sidebar.multiselect(
    "Category",
    df["category"].dropna().unique(),
    default=df["category"].dropna().unique()
)

year_filter = st.sidebar.multiselect(
    "Year",
    df["year"].dropna().unique(),
    default=df["year"].dropna().unique()
)

# Apply filters
df_filtered = df[
    (df["region"].isin(region_filter)) &
    (df["category"].isin(category_filter)) &
    (df["year"].isin(year_filter))
]

# SALES BY REGION
col1, col2 = st.columns(2)

with col1:

    sales_region = df_filtered.groupby("region")["sales"].sum().reset_index()

    fig = px.bar(
        sales_region,
        x="region",
        y="sales",
        color="region",
        title="Sales by Region"
    )

    st.plotly_chart(fig, use_container_width=True)

# SALES EVOLUTION
with col2:

    sales_year = df_filtered.groupby("year")["sales"].sum().reset_index()

    fig = px.line(
        sales_year,
        x="year",
        y="sales",
        markers=True,
        title="Sales Evolution"
    )

    st.plotly_chart(fig, use_container_width=True)

# TOP PRODUCTS

col3, col4 = st.columns(2)

with col3:

    top_products = (
        df_filtered.groupby("product_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="sales",
        y="product_name",
        orientation="h",
        title="Top 10 Products"
    )

    st.plotly_chart(fig, use_container_width=True)

# TOP CLIENTS
with col4:

    top_clients = (
        df_filtered.groupby("customer_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_clients,
        x="sales",
        y="customer_name",
        orientation="h",
        title="Top 10 Clients"
    )

    st.plotly_chart(fig, use_container_width=True)

# HEATMAP

st.subheader("Heatmap Sales Region vs Category")

pivot = df_filtered.pivot_table(
    values="sales",
    index="region",
    columns="category",
    aggfunc="sum"
)

fig = px.imshow(
    pivot,
    text_auto=True,
    color_continuous_scale="RdBu_r"
)

st.plotly_chart(fig, use_container_width=True)