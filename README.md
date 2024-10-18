# Graduation-project-DEPI Bank Churn Prediction

## Table of Contents
- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Objectives](#objectives)
- [Dataset](#dataset)
- [Technologies Used](#technologies-used)
- [Build and run doccker image](#Build-and-run-doccker-image)

## Project Overview
This project aims to predict whether a bank customer will churn based on various factors such as credit score, age, balance, and account activity. The dataset includes customers from banks in France, Germany, and Spain. The goal is to provide actionable insights to reduce customer churn rates and enhance customer retention strategies.

## Business Problem
Customer churn is a significant challenge in the banking industry. Banks invest substantial resources to acquire new customers, but retaining existing customers is often more cost-effective. Understanding the factors that lead to customer churn enables banks to take proactive measures, such as offering personalized services or targeted promotions.

## Objectives
- Predict customer churn using machine learning models based on various attributes.
- Provide insights into which features impact churn the most.
- Assist banks in reducing churn rates by identifying at-risk customers.

## Dataset
The dataset consists of customer information, including:
- **Credit Score**
- **Gender**
- **Age**
- **Tenure**
- **Balance**
- **Products Number**
- **Credit Card**
- **Active Member**
- **Estimated Salary**
- **Country** (France, Germany, Spain)

## Technologies Used
- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn
- NumPy
- Docker
- Hugging face

# run these in terminal to show the board
- tensorboard --logdir=Machine_Learning/logs/Models
  
## Build and run doccker image
- ### first Command
- docker build -t final_depi .
- ### Second Command
- docker run -p 8501:8501 final_depi.






