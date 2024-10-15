import streamlit as st

st.set_page_config(
    page_title="Bank Churn Prediction",
    page_icon=":bank:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# st.sidebar.title("Bank Churn prediction")
# st.sidebar.info("Select a page to view")

st.title("Bank Customer Churn Prediction")

# add this photo
st.image("Bank.jpg", use_column_width=True, width=400)

st.markdown(
    """
    <style>

    [data-testid="stSidebar"] {
        background: #e4f0ff;  /* Light blue background for sidebar */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
## Overview 🔎
This web application predicts whether a bank customer will churn based on various factors such as credit score, age, balance, and account activity. The dataset includes customers from banks in France, Germany, and Spain.

## <span style="color:#f2c453">Business Problem 🙍‍♂️</span>
**<span style="color:blue">Customer churn</span>** is a significant challenge in the banking industry. Banks invest substantial resources to acquire new customers, but retaining existing customers is often more cost-effective. Understanding the factors that lead to customer churn enables banks to take proactive measures, such as offering personalized services or targeted promotions, to improve retention rates.

In this project, we aim to predict whether a customer will churn based on a range of attributes, including:

- **Credit Score**: A customer's credit rating.
- **Gender**: Male or female customers.
- **Age**: The age of the customer.
- **Tenure**: The number of years the customer has been with the bank.
- **Balance**: The customer's account balance.
- **Products Number**: Number of bank products the customer uses.
- **Credit Card**: Whether the customer has a credit card.
- **Active Member**: Whether the customer is an active member.
- **Estimated Salary**: The customer's estimated annual salary.
- **Country**: The customer's country of residence (France, Germany, Spain).

## Objectives
- To predict customer churn using machine learning models based on the factors mentioned above.
- To provide insights into which features have the most impact on churn.
- To help banks in France, Germany, and Spain reduce churn rates by identifying at-risk customers and providing targeted solutions.
""",
    unsafe_allow_html=True,
)
# # Add navigation buttons
# if st.button("Go to Summary Statistics & Dashboards"):
#     st.experimental_set_query_params(page="summary")
# elif st.button("Go to Machine Learning Prediction"):
#     st.experimental_set_query_params(page="prediction")
