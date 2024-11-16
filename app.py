# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import streamlit as st

# Set up the Streamlit app
st.title("Sales Data Analysis App")

# File uploader for the dataset
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    # Load the dataset
    df = pd.read_csv(uploaded_file)

    # Data Cleaning and Preparation
    st.subheader("Initial Dataset")
    st.write(df.head())

    # Remove Duplicates
    duplicates = df.duplicated().sum()
    st.write(f"Number of duplicate rows: {duplicates}")
    df = df.drop_duplicates()
    st.write(f"Dataset shape after removing duplicates: {df.shape}")

    # Correct Errors in Data Entries
    negative_sales = df[df['Sales'] < 0]
    negative_quantity = df[df['Quantity'] < 0]
    st.write(f"Number of transactions with negative sales: {len(negative_sales)}")
    st.write(f"Number of transactions with negative quantity: {len(negative_quantity)}")
    
    df = df[df['Sales'] >= 0]  # Remove negative sales
    df = df[df['Quantity'] >= 0]  # Remove negative quantity

    # Handle Missing Values
    missing_values = df.isnull().sum()
    st.write("Missing values in each column:")
    st.write(missing_values[missing_values > 0])
    
    df['Sales'].fillna(df['Sales'].mean(), inplace=True)
    df['Quantity'].fillna(df['Quantity'].mean(), inplace=True)
    df['Profit'].fillna(df['Profit'].mean(), inplace=True)
    df['Segment'].fillna(df['Segment'].mode()[0], inplace=True)
    df['Ship Mode'].fillna(df['Ship Mode'].mode()[0], inplace=True)
    
    st.write(f"Dataset shape after handling missing values: {df.shape}")

    # Create Additional Columns for Time-Based Analysis
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Quarter'] = df['Order Date'].dt.quarter

    # Metrics Calculation
    total_sales_revenue = df['Sales'].sum()
    average_profit_margin = (df['Profit'] / df['Sales']).mean()

    st.subheader("Metrics")
    st.write(f"Total Sales Revenue: ${total_sales_revenue:.2f}")
    st.write(f"Average Profit Margin: {average_profit_margin:.2f}%")

    # Sales by Category Visualization
    sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Sales', y='Category', data=sales_by_category, palette='viridis')
    plt.title('Sales by Category')
    
    st.pyplot(plt)

    # Monthly Sales Trend Visualization
    monthly_sales = df.resample('M', on='Order Date')['Sales'].sum()
    
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales, marker='o')
    plt.title('Monthly Sales Trend')
    
    st.pyplot(plt)

    # Sales Forecasting using Exponential Smoothing
    model = ExponentialSmoothing(monthly_sales, trend='add', seasonal='add', seasonal_periods=12)
    fit_model = model.fit()
    
    forecast = fit_model.forecast(steps=12)
    
    forecast_index = pd.date_range(start=monthly_sales.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales, label='Historical Sales', marker='o')
    plt.plot(forecast_index, forecast, label='Forecasted Sales', marker='o', color='orange')
    
    plt.title('Sales Forecast for Next 12 Months')
    
    st.pyplot(plt)

# New Features and Visualizations

# Top Products Visualization
st.subheader("Top Selling Products")
top_products = df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='Sales', y='Product Name', data=top_products, palette='viridis')
plt.title('Top 10 Selling Products')
st.pyplot(plt)

# Underperforming Products Visualization
st.subheader("Underperforming Products")
underperforming_products = df.groupby('Product Name')['Sales'].sum().nsmallest(10).reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='Sales', y='Product Name', data=underperforming_products, palette='rocket')
plt.title('Underperforming Products')
st.pyplot(plt)

# Customer Segmentation Visualization
st.subheader("Sales by Customer Segment")
sales_by_segment = df.groupby('Segment')['Sales'].sum().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x='Segment', y='Sales', data=sales_by_segment, palette='Blues')
plt.title('Sales by Customer Segment')
st.pyplot(plt)

# Recommendations Display
st.subheader("Recommendations")
st.write("1. Tailor marketing efforts towards high-performing product categories.")
st.write("2. Focus on Consumer segment as it shows significant sales.")
st.write("3. Optimize stock levels based on sales forecasts to minimize stockouts.")
st.write("4. Adjust discount strategies based on their impact on profit margins.")

# Continuous Improvement Process Display
st.subheader("Continuous Improvement Process")
st.write("1. Regularly update datasets and refine analysis based on new data.")
st.write("2. Utilize feedback from stakeholders to adjust strategies as needed.")
