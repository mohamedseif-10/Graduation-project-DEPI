import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_icon=":bank:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# add spinner
with st.spinner("Loading💸💸"):
    import time
    time.sleep(0.0003)

# Load the data
@st.cache_data
def load_data():
    data = pd.read_csv("https://raw.githubusercontent.com/mohamedseif-10/Graduation-project-depi/main/Data/modified_Bank_Customer_Churn_Prediction.csv")

    return data


data = load_data()

# Load the model pipeline
model_pipeline = joblib.load("../Machine_Learning/model_pipeline.pkl")


# Sidebar customization
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: #e4f0ff;  /* Light blue background for sidebar */
    }

    /* Style the form inputs */
    input {
        background-color: #e4f0ff !important;
        color: #000 !important;
    }

    /* Style the submit button */
    .stButton>button {
        background-color: #f2c453 !important;
        color: white !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none;
        padding: 10px 20px;
    }

    /* Adjust the hover effect on submit button */
    .stButton>button:hover {
        background-color: #e2b144 !important;
        color: white !important;
    }

    /* Title and text color adjustments */
    h2, h4, label {
        color: #f2c453;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state to store inputs and predictions
if "predictions" not in st.session_state:
    st.session_state.predictions = []

# Assign a unique key to the form
with st.form(key="unique_prediction_form"):
    st.write("## Predicting customer churn📊")
    st.image("https://raw.githubusercontent.com/mohamedseif-10/Graduation-project-DEPI/main/web_app/predict.jpg", use_column_width=True, width=400)
    st.write("#### Please fill in the following details:")

    credits = int(
        st.number_input(
            "Enter the credit score",
            min_value=data["credit_score"].min(),
            max_value=data["credit_score"].max(),
            value=500,
        )
    )
    gender = st.selectbox("Select the gender of the customer", ["Male", "Female"])
    tenure = int(
        st.number_input(
            "Enter the number of years the customer has been with the bank",
            min_value=data["tenure"].min(),
            max_value=data["tenure"].max(),
            value=5,
        )
    )
    balance = float(
        st.number_input(
            "Enter the account balance",
            min_value=data["balance"].min(),
            max_value=data["balance"].max(),
            value=0.0,
        )
    )
    age = int(
        st.number_input(
            "Enter the age of the customer",
            min_value=data["age"].min(),
            max_value=data["age"].max(),
            value=30,
        )
    )
    products_number = int(
        st.number_input(
            "Enter the number of bank products the customer uses",
            min_value=data["products_number"].min(),
            max_value=data["products_number"].max(),
            value=2,
        )
    )
    credit_card = st.selectbox("Does the customer have a credit card?", ["Yes", "No"])
    active_member = st.selectbox("Is the customer an active member?", ["Yes", "No"])
    estimated_salary = float(
        st.number_input(
            "Enter the estimated annual salary",
            min_value=data["estimated_salary"].min(),
            max_value=data["estimated_salary"].max(),
            value=50000.0,
        )
    )
    country = st.selectbox(
        "Select the country of residence", ["France", "Germany", "Spain"]
    )

    # Submit button
    submit_button = st.form_submit_button("Predict")

if submit_button:
    # Store user inputs in a DataFrame
    sample_data = pd.DataFrame(
        {
            "credit_score": [credits],
            "gender": [gender],
            "tenure": [tenure],
            "balance": [balance],
            "age": [age],
            "products_number": [products_number],
            "credit_card": [credit_card],  # Yes/No from user input
            "active_member": [active_member],  # Yes/No from user input
            "estimated_salary": [estimated_salary],
            "country": [country],
        }
    )

    # Make a prediction
    prediction = model_pipeline.predict(sample_data)

    # Store the input and prediction in session state
    st.session_state.predictions.append(
        {
            "credit_score": credits,
            "gender": gender,
            "tenure": tenure,
            "balance": balance,
            "age": age,
            "products_number": products_number,
            "credit_card": credit_card,
            "active_member": active_member,
            "estimated_salary": estimated_salary,
            "country": country,
            "prediction": "Will Not Churn" if not prediction[0] else "Will Churn",
        }
    )

    # Show the result based on the prediction
    if prediction[0] == 0:
        st.success("#### Great news! This customer will not churn! 🎉")
    else:
        st.error("#### This customer will churn! 😢")

# Display all previous predictions and inputs
if st.session_state.predictions:
    st.write("### Prediction History")
    history_df = pd.DataFrame(st.session_state.predictions)
    st.write(history_df)

    # Count the number of churn and non-churn customers
    churn_count = history_df["prediction"].value_counts()

    # Create a pie chart
    pie_chart = px.pie(
        churn_count,
        values=churn_count.values,
        names=churn_count.index,
        title="Churn vs Non-Churn Prediction Distribution",
        color_discrete_sequence=[
            "#0068c9",
            "#f2c453",
        ],  # Colors for churn and non-churn
    )

    # Display the pie chart
    st.plotly_chart(pie_chart)
