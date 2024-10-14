import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

@st.cache_data
def load_data():
    return pd.read_csv(
        "https://raw.githubusercontent.com/Team-Alpha-Squad/Streamlit-Web-App/main/data/Churn_Modelling.csv", encoding="utf-8"
    )


# Set title and info
st.title("Bank Customer Churn Prediction")
st.info(
    "This is a simple web app that predicts the likelihood of a bank customer churning."
)
st.image("https://your-image-url-here", use_column_width=True)

##############################################################

# Sidebar configuration
st.sidebar.title("Customer Data")
st.sidebar.markdown(
    "Please adjust the sliders to explore the data and see how it affects the prediction."
)

st.sidebar.subheader("Customer Information")
age = st.sidebar.slider("Age", 18, 61, 37)

st.sidebar.subheader("Account Information")
balance = st.sidebar.slider("Average Balance", 0, 250000, 50000, step=1000)
numOfProducts = st.sidebar.slider("Number of Products", 1, 4, 2)
creditScore = st.sidebar.slider("Credit Score", 350, 850, 650, step=10)

st.sidebar.subheader("Activity Information")
isActiveMember = st.sidebar.selectbox("Active Member", ["Yes", "No"])
estimatedSalary = st.sidebar.slider("Estimated Salary", 0, 200000, 100000)

st.sidebar.subheader("Customer Interaction")
hasCrCard = st.sidebar.selectbox("Has Credit Card", ["Yes", "No"])
tenure = st.sidebar.slider("Tenure", 0, 10, 5)

# Taking an input from the user
thisIsAge = st.number_input("Age", min_value=18, max_value=61, value=37)
thisIsBalance = st.number_input(
    "Average Balance", min_value=0, max_value=250000, value=50000, step=1000
)

# Spinner for loading
with st.spinner("Running the model"):
    st.write("This is the prediction")

# Main section
st.title("Bank Customer Churn Prediction Visualization")

data = load_data()
# Sidebar sliders for number of rows and columns
n_rows = st.sidebar.slider(
    "Number of rows to display", max_value=len(data), min_value=1, value=5, step=1000
)

n_cols = st.sidebar.slider(
    "Number of columns to display",
    max_value=len(data.columns),
    min_value=1,
    value=5,
    step=1,
)

# Display summary statistics and head of the data
st.write(data.describe())
st.write(data.head(n_rows))

# Multiselect for column selection
columns_to_show = st.multiselect(
    "Select columns to display", data.columns.tolist(), data.columns.tolist()
)

st.write(data[columns_to_show].head(n_rows))

# Scatter plot of balance vs estimated_salary
fig_scatter = px.scatter(data, x="balance", y="estimated_salary")
st.plotly_chart(fig_scatter)

# Scatter plot of estimated_salary vs balance with churn color-coded
fig_scatter2 = px.scatter(data, x="estimated_salary", y="balance", color="churn")
st.plotly_chart(fig_scatter2)

numerical_columns = np.array(data.select_dtypes(include=[np.number]).columns.tolist())
categorical_columns = np.array(data.select_dtypes(include=[object]).columns.tolist())


tab1, tab2, tab3=st.tabs(["Bar chart", "Histogram", "Pie chart"])

# Bar chart for age vs churn, color by gender
with tab1:
    fig_bar = px.bar(data, x="age", y="churn", barmode="group", color="gender")
    st.plotly_chart(fig_bar)

with tab2:
    # Select columns for histogram plot
    col1, col2, col3 = st.columns(3)
    with col1:
        x_column = st.selectbox("X-axis", numerical_columns)
    with col2:
        y_column = st.selectbox("Y-axis", numerical_columns)
    with col3:
        color_column = st.selectbox("Color", ["active_member", "churn", "gender"])
        
    # x_column = st.selectbox("X-axis", numerical_columns)
    # y_column = st.selectbox("Y-axis", numerical_columns)
    # color_column = st.selectbox("Color", ["active_member", "churn", "gender"])
    # Plot the histogram
    fig_hist = px.histogram(data, x=x_column, y=y_column, color=color_column)
    st.plotly_chart(fig_hist)

# fig_bar = px.bar(data, x= 'products_number', barmode='group', color='churn')
# st.plotly_chart(fig_bar)

with tab3:
    pie_param = st.selectbox("Select a parameter", data.columns)
    fig_pie = px.pie(data, names=pie_param, title="Products Distribution")
    st.plotly_chart(fig_pie)


product_count = data["products_number"].value_counts().reset_index()
product_count.columns = ["products_number", "count"]

product_options = st.multiselect(
    "Select products to display",
    options=product_count["products_number"].unique(),
    default=product_count["products_number"].unique(),
)
filtered_data = product_count[product_count["products_number"].isin(product_options)]
fig_bar = px.bar(
    filtered_data,
    x="products_number",
    y="count",
    barmode="group",
    color="products_number",
)
st.plotly_chart(fig_bar)


# fig_pie = px.pie(data, names="products_number", title="Products Distribution")
# st.plotly_chart(fig_pie)


st.write(data.head(10))


# Caching machine learning model
# @st.cache_resource
# def load_model():
#     return joblib.load("model.pkl")