import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import os

# -----------------------------
# APP TITLE
# -----------------------------
st.title("SmartVend AI 🏪")
st.subheader("Voice-Ready Analytics & Forecasting for Small Vendors")

st.write(
    "This app analyzes small vendor sales data and generates insights "
    "to support better business decisions."
)

# -----------------------------
# LOAD DATA
# -----------------------------
st.header("1️⃣ Load Sales Data")

uploaded_file = st.file_uploader("Upload sales dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

df["date"] = pd.to_datetime(df["date"])

st.success("Dataset loaded successfully!")
st.dataframe(df.head())

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
df["sales_amount"] = df["quantity"] * df["price"]
df["profit"] = (df["price"] - df["cost"]) * df["quantity"]

# -----------------------------
# SUMMARY
# -----------------------------
st.header("2️⃣ Business Summary")

col1, col2 = st.columns(2)
col1.metric("Total Sales (₹)", round(df["sales_amount"].sum(), 2))
col2.metric("Total Profit (₹)", round(df["profit"].sum(), 2))

# -----------------------------
# PRODUCT SALES
# -----------------------------
st.header("3️⃣ Product-wise Sales")

product_sales = df.groupby("product")["sales_amount"].sum()

fig1, ax1 = plt.subplots()
product_sales.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Sales Amount (₹)")
st.pyplot(fig1)

# -----------------------------
# DAILY SALES TREND
# -----------------------------
st.header("4️⃣ Daily Sales Trend")

daily_sales = df.groupby("date")["sales_amount"].sum()

fig2, ax2 = plt.subplots()
daily_sales.plot(ax=ax2)
ax2.set_ylabel("Sales Amount (₹)")
st.pyplot(fig2)

# -----------------------------
# ML FORECASTING
# -----------------------------
st.header("5️⃣ Sales Forecasting (Next 7 Days)")

daily_sales_df = daily_sales.reset_index()
daily_sales_df["date_ordinal"] = daily_sales_df["date"].map(pd.Timestamp.toordinal)

X = daily_sales_df[["date_ordinal"]]
y = daily_sales_df["sales_amount"]

model = LinearRegression()
model.fit(X, y)

future_dates = pd.date_range(
    start=daily_sales_df["date"].max() + pd.Timedelta(days=1),
    periods=7
)

future_df = pd.DataFrame({
    "date": future_dates,
    "date_ordinal": future_dates.map(pd.Timestamp.toordinal)
})

future_df["predicted_sales"] = model.predict(future_df[["date_ordinal"]])

st.dataframe(future_df[["date", "predicted_sales"]])

fig3, ax3 = plt.subplots()
ax3.plot(daily_sales_df["date"], daily_sales_df["sales_amount"], label="Historical")
ax3.plot(future

