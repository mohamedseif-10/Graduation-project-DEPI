import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Bank Churn Prediction",
    page_icon=":bank:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Bank Customer Churn Prediction")

st.image("https://raw.githubusercontent.com/mohamedseif-10/Graduation-project-DEPI/main/web_app/Background.jpg", use_column_width=True)

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

# Main content
st.markdown(
    """
## <span style="color:black">Overview 🔎</span>
Welcome to the Bank Customer Churn Prediction web application! This platform utilizes advanced machine learning techniques to predict the likelihood of customer churn in the banking sector. By analyzing key customer attributes such as credit score, age, balance, and account activity, we aim to provide banks with actionable insights that can help retain their customers.

## <span style="color:black">Business Problem 🙍‍♂️</span>
**Customer churn** is a critical issue for financial institutions, with significant implications for profitability and long-term sustainability. Retaining existing customers is often more cost-effective than acquiring new ones. This application aims to address this challenge by leveraging data-driven strategies to predict churn and enhance customer retention efforts.

## <span style="color:black">Key Factors Influencing Churn: </span>
- **Credit Score**: The financial reliability of a customer.
- **Gender**: Identifies male and female customers.
- **Age**: The customer's age demographic.
- **Tenure**: The duration of the customer's relationship with the bank.
- **Balance**: The available funds in the customer's account.
- **Number of Products**: The variety of banking products the customer holds.
- **Credit Card Ownership**: Indicates whether the customer has a credit card.
- **Active Membership**: A measure of the customer's engagement with the bank.
- **Estimated Salary**: The customer’s approximate annual earnings.
- **Country**: The geographical location of the customer (France, Germany, or Spain).

## <span style="color:black">Objective💭</span>

- **Predict Customer Churn**: Utilize machine learning algorithms to foresee churn based on historical customer data.
- **Insights and Analysis**: Identify the most impactful features influencing churn to enable targeted interventions.
- **Support Banks**: Provide actionable recommendations for banks operating in France, Germany, and Spain to minimize churn and enhance customer satisfaction.

## <span style="color:black">Methodology 📊</span>
Our approach involves several critical steps to ensure the effectiveness of the churn prediction model:

1. **Data Collection**: Gathering comprehensive datasets from banking sources, including customer demographics and account information.
2. **Data Preprocessing**: Cleaning and preparing the data by handling missing values, encoding categorical variables, and normalizing numerical features.
3. **Exploratory Data Analysis (EDA)**: Analyzing the data to uncover patterns, trends, and relationships between different features using visualizations.
4. **Model Selection**: Comparing various machine learning algorithms such as Logistic Regression, Decision Trees, Random Forest, and Gradient Boosting to find the best-performing model.
5. **Model Training & Testing**: Splitting the dataset into training and testing sets, training the model, and evaluating its performance using metrics such as accuracy, precision, recall, and F1-score.
6. **Deployment**: Implementing the model in a user-friendly web application for real-time predictions and insights.

## <span style="color:black">Expected Outcomes 🎯</span>
- **Predictive Accuracy**: Achieve a high level of accuracy in predicting customer churn to minimize false positives and negatives.
- **Actionable Insights**: Provide banks with clear insights into the factors contributing to churn, enabling targeted marketing and retention strategies.
- **Enhanced Customer Experience**: Help banks improve customer satisfaction through personalized services based on churn predictions.
- **Strategic Decision-Making**: Equip bank management with data-driven insights for better strategic planning and resource allocation.

## <span style="color:black">Technology Stack 💻</span>
This project is built using a robust technology stack to ensure efficient performance and usability:

- **Programming Language**: Python
- **Framework**: Streamlit for developing the web application.
- **Data Manipulation**: Pandas and NumPy for data processing.
- **Data Visualization**: Plotly and Matplotlib for creating interactive charts and graphs.
- **Machine Learning Libraries**: Scikit-learn for building and evaluating machine learning models.
- **Deployment**: Docker for containerization and easy deployment.

## <span style="color:black">User Instructions 🛠️</span>
To use this application, navigate through the pages in the sidebar (Home page - visualizations - model). View summary statistics and insights or proceed to machine learning predictions by clicking the respective buttons.

### **Feedback 💬**
We value your feedback! Please share your thoughts or suggestions for improvements below:
""",
    unsafe_allow_html=True,
)

# Feedback form
with st.form(key="feedback_form"):
    name = st.text_input("Your Name")
    comments = st.text_area("Your comments or suggestions about our web app and model ??", height=100)
    submit_button = st.form_submit_button("Submit Feedback")

    if submit_button:
        feedback_data = {
            "Name": name,
            "Comments": comments,
        }
        feedback_df = pd.DataFrame([feedback_data])

        if not os.path.isfile("feedback.csv"):
            feedback_df.to_csv("feedback.csv", index=False, mode="w", header=True)
        else:
            feedback_df.to_csv("feedback.csv", index=False, mode="a", header=False)

        st.success("Thank you for your feedback! We appreciate your input.")
