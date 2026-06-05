import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE CONFIG
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(__file__)

    file_path = os.path.join(
        BASE_DIR,
        "main_data.csv"
    )

    df = pd.read_csv(file_path)


    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    return df

main_df = load_data()

# SIDEBAR
st.sidebar.header("Filter Data")

years = sorted(
    main_df["order_purchase_timestamp"].dt.year.unique()
)

selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    years
)

filtered_df = main_df[
    main_df["order_purchase_timestamp"].dt.year
    == selected_year
]

# HEADER
st.title("📊 E-Commerce Public Dataset Dashboard")

st.markdown(
    """
    Dashboard ini menampilkan hasil analisis data
    E-Commerce Public Dataset.
    """
)

# KPI
total_revenue = filtered_df["price"].sum()

total_orders = filtered_df["order_id"].nunique()

total_customers = filtered_df["customer_unique_id"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Total Customers",
    f"{total_customers:,}"
)

st.markdown("---")

# TOP PRODUCT CATEGORY
st.subheader(
    "Top 10 Product Categories by Revenue"
)

revenue_category = (
    filtered_df
    .groupby("product_category_name_english")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(
    x=revenue_category.values,
    y=revenue_category.index,
    palette="Blues_r",
    ax=ax
)

ax.set_xlabel("Revenue")
ax.set_ylabel("Category")

st.pyplot(fig)

# MONTHLY ORDERS TREND
st.subheader(
    "Monthly Orders Trend"
)

monthly_orders = (
    filtered_df
    .set_index("order_purchase_timestamp")
    .resample("M")
    .size()
)

fig, ax = plt.subplots(figsize=(12,5))

monthly_orders.plot(
    marker="o",
    ax=ax
)

ax.set_xlabel("Month")
ax.set_ylabel("Orders")

st.pyplot(fig)

# CUSTOMER SATISFACTION
st.subheader(
    "Top Categories by Review Score"
)

review_summary = (
    filtered_df
    .groupby("product_category_name_english")
    .agg(
        avg_review_score=("review_score","mean"),
        total_reviews=("review_score","count")
    )
)

review_summary = review_summary[
    review_summary["total_reviews"] >= 50
]

review_summary = review_summary.sort_values(
    by="avg_review_score",
    ascending=False
).head(10)

fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(
    x=review_summary["avg_review_score"],
    y=review_summary.index,
    palette="Greens_r",
    ax=ax
)

ax.set_xlim(0,5)

st.pyplot(fig)

# RFM ANALYSIS
st.subheader(
    "Customer Segmentation (RFM)"
)

snapshot_date = (
    filtered_df["order_purchase_timestamp"].max()
    + pd.Timedelta(days=1)
)

rfm = filtered_df.groupby(
    "customer_unique_id"
).agg(
    recency=(
        "order_purchase_timestamp",
        lambda x: (snapshot_date - x.max()).days
    ),
    frequency=("order_id","nunique"),
    monetary=("price","sum")
)

rfm["R_score"] = pd.qcut(
    rfm["recency"],
    4,
    labels=[4,3,2,1]
)

rfm["F_score"] = pd.qcut(
    rfm["frequency"].rank(method="first"),
    4,
    labels=[1,2,3,4]
)

rfm["M_score"] = pd.qcut(
    rfm["monetary"],
    4,
    labels=[1,2,3,4]
)

def customer_segment(row):

    if row["R_score"] == 4 and row["F_score"] >= 3:
        return "Best Customers"

    elif row["F_score"] >= 3:
        return "Loyal Customers"

    elif row["M_score"] >= 3:
        return "Big Spenders"

    elif row["R_score"] <= 2:
        return "At Risk Customers"

    else:
        return "Potential Customers"

rfm["segment"] = rfm.apply(
    customer_segment,
    axis=1
)

segment_counts = (
    rfm["segment"]
    .value_counts()
)

fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(
    x=segment_counts.values,
    y=segment_counts.index,
    palette="Set2",
    ax=ax
)

st.pyplot(fig)
