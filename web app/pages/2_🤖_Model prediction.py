import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time

# Load the model
# model = joblib.load("model.pkl")

# get the data
st.markdown(
    """
    <style>

    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #83c9ff, #d9f1ff);  /* Light blue background for sidebar */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# progress bar with model prediction
# st.write("## Model Prediction")
st.write("## Predicting customer churn📊")
st.image("predict.jpg", use_column_width=True, width=400)
st.write("#### Please wait while we predict the customer churn status.")
my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.005)
    my_bar.progress(percent_complete + 1)
predicted_ans = True
if predicted_ans: 
    st.success("#### Great news! This customer will not churn! 🎉")
else:
    st.error("#### This customer will churn! 😢")
