import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import streamlit as st

# Load the dataset
@st.cache
def load_data():
    # Replace 'cleaned_superstore_sales.csv' with the path to your cleaned dataset file
    df = pd.read_csv('cleaned_superstore_sales.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# Title of the app
st.title("Superstore Sales Analysis")

# Display initial data
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(df)

# Metrics Calculation
total_sales_revenue = df['Sales'].sum()
average_profit_margin = (df['Profit'] / df['Sales']).mean() * 100

st.subheader('Key Metrics')
st.write(f"Total Sales Revenue: ${total_sales_revenue:.2f}")
st.write(f"Average Profit Margin: {average_profit_margin:.2f}%")

# Sales Trends Visualization
monthly_sales = df.resample('M', on='Order Date')['Sales'].sum()
st.subheader('Monthly Sales Trend')
st.line_chart(monthly_sales)

# Top Products Visualization
top_products = df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
st.subheader('Top 10 Selling Products')
st.bar_chart(top_products.set_index('Product Name')['Sales'])

# Sales by Customer Segment Visualization
sales_by_segment = df.groupby('Segment')['Sales'].sum().reset_index()
st.subheader('Sales by Customer Segment')
st.bar_chart(sales_by_segment.set_index('Segment')['Sales'])

# Recommendations Section
st.subheader('Recommendations')
recommendations = [
    "1. Tailor marketing efforts towards high-performing product categories.",
    "2. Focus on Consumer segment as it shows significant sales.",
    "3. Optimize stock levels based on sales forecasts to minimize stockouts.",
    "4. Adjust discount strategies based on their impact on profit margins."
]
for rec in recommendations:
    st.write(rec)

# Sales Forecasting
model = ExponentialSmoothing(monthly_sales, trend='add', seasonal='add', seasonal_periods=12)
fit_model = model.fit()
forecast = fit_model.forecast(steps=12)
forecast_index = pd.date_range(start=monthly_sales.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')

st.subheader('Sales Forecast for Next 12 Months')
forecast_df = pd.DataFrame({'Forecasted Sales': forecast}, index=forecast_index)
st.line_chart(forecast_df['Forecasted Sales'])

# Continuous Improvement Process Section
st.subheader('Continuous Improvement Process')
improvement_steps = [
    "1. Regularly update datasets and refine analysis based on new data.",
    "2. Utilize feedback from stakeholders to adjust strategies as needed."
]
for step in improvement_steps:
    st.write(step)