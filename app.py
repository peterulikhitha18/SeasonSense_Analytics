import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="SeasonSense Analytics",
    page_icon="🌾",
    layout="wide"
)

# Load dataset
df = pd.read_csv("agriseason-filtered (1).csv")

# Title
st.title("🌾 SeasonSense Analytics")
st.subheader("Seasonal Agriculture Performance Analysis")

st.write(
    "An interactive application for analyzing agricultural performance "
    "across seasons, crops, environmental conditions and resource usage."
)

# Sidebar
st.sidebar.header("Filters")

seasons = st.sidebar.multiselect(
    "Select Season",
    options=df["Season"].unique(),
    default=df["Season"].unique()
)

crops = st.sidebar.multiselect(
    "Select Crop",
    options=df["Crop"].unique(),
    default=df["Crop"].unique()
)

# Apply filters
filtered_df = df[
    (df["Season"].isin(seasons)) &
    (df["Crop"].isin(crops))
]

# KPI calculations
avg_yield = filtered_df["Yield_Tonnes_Ha"].mean()
total_production = filtered_df["Production_Tonnes"].sum()
total_revenue = filtered_df["Revenue_INR"].sum()
total_profit = filtered_df["Profit_INR"].sum()

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("🌱 Average Yield", f"{avg_yield:.2f} t/ha")
col2.metric("🌾 Total Production", f"{total_production:,.0f} tonnes")
col3.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
col4.metric("📈 Total Profit", f"₹{total_profit:,.0f}")

st.divider()

# Seasonal Yield
st.header("📊 Seasonal Performance")

season_data = (
    filtered_df.groupby("Season")["Yield_Tonnes_Ha"]
    .mean()
    .reset_index()
)

fig1 = px.bar(
    season_data,
    x="Season",
    y="Yield_Tonnes_Ha",
    title="Average Yield by Season",
    labels={"Yield_Tonnes_Ha": "Average Yield (Tonnes/Ha)"}
)

st.plotly_chart(fig1, use_container_width=True)

# Production and Profit
performance = (
    filtered_df.groupby("Season")[
        ["Production_Tonnes", "Profit_INR"]
    ].mean()
    .reset_index()
)

fig2 = px.bar(
    performance,
    x="Season",
    y=["Production_Tonnes", "Profit_INR"],
    barmode="group",
    title="Average Production and Profit by Season"
)

st.plotly_chart(fig2, use_container_width=True)

# Environmental analysis
st.header("🌦️ Environmental Conditions")

environment = (
    filtered_df.groupby("Season")[
        ["Rainfall_mm", "Avg_Temperature_C", "Humidity_pct", "Water_Used_m3"]
    ].mean()
    .reset_index()
)

st.dataframe(environment.round(2), use_container_width=True)

# Crop performance
st.header("🌾 Crop Performance")

crop_data = (
    filtered_df.groupby("Crop")[
        ["Yield_Tonnes_Ha", "Production_Tonnes", "Profit_INR"]
    ].mean()
    .reset_index()
    .sort_values("Yield_Tonnes_Ha", ascending=False)
)

st.dataframe(crop_data.round(2), use_container_width=True)

# Correlation
st.header("🔗 Correlation Analysis")

correlation = filtered_df[
    [
        "Rainfall_mm",
        "Avg_Temperature_C",
        "Humidity_pct",
        "Water_Used_m3",
        "Yield_Tonnes_Ha",
        "Profit_INR"
    ]
].corr()

st.dataframe(correlation.round(2), use_container_width=True)

# Key insights
st.header("💡 Key Insights")

best_season = (
    filtered_df.groupby("Season")["Yield_Tonnes_Ha"]
    .mean()
    .idxmax()
)

best_crop = (
    filtered_df.groupby("Crop")["Yield_Tonnes_Ha"]
    .mean()
    .idxmax()
)

st.write(f"• The highest average-yield season is **{best_season}**.")
st.write(f"• The highest average-yield crop is **{best_crop}**.")
st.write("• Environmental conditions and water usage vary across seasons.")
st.write("• Seasonal and crop-level analysis can support better agricultural planning.")

# Recommendations
st.header("✅ Recommendations")

st.write("1. Select crops according to seasonal yield and profitability patterns.")
st.write("2. Optimize water usage based on seasonal requirements.")
st.write("3. Monitor rainfall, temperature and humidity for better planning.")
st.write("4. Use historical agricultural data to identify unusual patterns.")
st.write("5. Use seasonal performance insights to improve resource allocation.")

st.divider()

st.caption("SeasonSense Analytics | VOIS AICTE Major Project")