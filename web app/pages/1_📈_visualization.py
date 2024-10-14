import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time


# Loading the data with cache
@st.cache_data
def load_data():
    data = pd.read_csv(
        "C:\\Users\\LENOVO\\Documents\\AI-IBM_Data_Scientist\\Projects\\final_project\\Graduation-project-DEPI\\Data\\modified_Bank_Customer_Churn_Prediction.csv"
    )
    return data


data = load_data()

def plot_gauge(
    target_value, indicator_color, indicator_suffix, indicator_title, max_bound
):
    num_frames = 30  # Total number of frames for the animation
    values = np.linspace(
        0, target_value, num_frames
    )  # Create a sequence from 0 to target_value

    frames = [
        go.Frame(
            data=[
                go.Indicator(
                    value=value,
                    mode="gauge+number",
                    domain={"x": [0, 1], "y": [0, 1]},
                    number={
                        "suffix": indicator_suffix,
                        "font.size": 18,
                        "font.weight": "bold",
                        "font.color": indicator_color,
                    },
                    gauge={
                        "axis": {"range": [0, max_bound], "tickwidth": 1},
                        "bar": {"color": indicator_color},
                    },
                    title={
                        "text": indicator_title,
                        "font": {"size": 10, "weight": "bold"},
                    },
                )
            ],
            name=f"Value: {value}",  # Frame name
        )
        for value in values
    ]

    # Create the initial figure
    fig = go.Figure(
        data=frames[0].data,  # Start with the first frame
        layout=frames[0].layout,
        frames=frames,
    )

    # Layout adjustments
    fig.update_layout(
        height=200,
        margin=dict(l=26, r=26, t=0, b=0, pad=0),
    )

    # Placeholder for the plot
    placeholder = st.empty()

    # Run the animation automatically
    for frame in frames:
        fig.update_traces(value=frame.data[0].value)  # Update the gauge value
        placeholder.plotly_chart(
            fig, use_container_width=True
        )  # Render the updated figure
        time.sleep(0.00001)  # Adjust speed of animation


def plot_top_right():
    aggregated_data = data.groupby("country")["churn"].mean().reset_index()

    fig = px.bar(
        aggregated_data,
        x="country",
        y="churn",
        title="Churn Rate by Country",
        height=400,
        text_auto=True,
    )
    fig.update_traces(
        textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_bottom_left():
    monthly_churn = data.groupby("age_group")["churn"].mean().reset_index()

    fig = px.line(
        monthly_churn,
        x="age_group",
        y="churn",
        markers=True,
        text="churn",
        title="Churn Rate by Age Group",
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)


def plot_bottom_right():
    balance_by_country = data.groupby("country")["balance"].mean().reset_index()

    fig = px.bar(
        balance_by_country,
        x="country",
        y="balance",
        title="Average Balance by Country",
    )
    st.plotly_chart(fig, use_container_width=True)

st.title("Churn Prediction visualizations")
st.write("### Discover your inner treasure💰")
st.sidebar.success("Select a page to view")


st.markdown(
    """
## Data Summary
This section provides a detailed overview of the data used for predicting customer churn. 

### Features:
- **Summary Statistics**: Get insights into key statistical metrics of the data, such as averages, minimums, and maximums.
- **Interactive Dashboards**: Explore interactive visualizations to better understand the relationship between different features and customer churn. These dashboards allow for dynamic data exploration.

Use the tabs below to switch between summary statistics and interactive visuals.
"""
)


# tab1, tab2 = st.tabs(["Summary Statistics", "Interactive Visuals"])

numerical_columns = np.array(data.select_dtypes(include=[np.number]).columns.tolist())
categorical_columns = np.array(data.select_dtypes(include=[object]).columns.tolist())


st.markdown("### Descriptive Statistics")

churn_counts = data["churn"].value_counts()
# Calculate percentages
total_count = churn_counts.sum()
churn_percentage = (churn_counts.get(1, 0) / total_count) * 100
non_churn_percentage = 100 - churn_percentage
active_counts = data["active_member"].value_counts()

# Calculate percentages
total_count = active_counts.sum()
active_percentage = (active_counts.get(1, 0) / total_count) * 100
non_active_percentage = 100 - active_percentage


with st.container():
    column_1, column_2, column_3, column_4 = st.columns((15, 15, 15, 15))

    with column_1:
        # plot_metric(
        #     "Total Customers",
        #     len(data),
        #     prefix="",
        #     suffix="",
        #     show_graph=False,
        # )
        plot_gauge(len(data), "#0068C9", "", "Total Customers", 10000)
        plot_gauge(churn_percentage, "#0068C9", "%", "Churn Rate", 100)
        

    with column_2:
        plot_gauge(
            data[data["active_member"] == 1].shape[0],
            "#0068C9",
            "",
            "Total Active Members",
            10000,
        )
        plot_gauge(active_percentage, "#0068C9", "%", "Active Member Rate", 100)

    with column_3:
        plot_gauge(
            data["balance"].mean(),
            "#0068C9",
            "$",
            "Average Balance",
            data["balance"].max(),
        )
        plot_gauge(
            data["balance"].mean(),
            "#0068C9",
            "$",
            "Average Balance",
            data["balance"].max(),
        )

    with column_4:
        plot_gauge(
            data["age"].mean(),
            "#0068C9",
            "",
            "Average ages",
            data["age"].max(),
        )

        plot_gauge(
            data["age"].mean(),
            "#0068C9",
            "",
            "Average ages",
            data["age"].max(),
        )


top_left_column, top_right_column = st.columns((6, 1))
bottom_left_column, bottom_middle_columns, bottom_right_column = st.columns((5, 4, 5))

with st.container():
    with bottom_right_column:
        plot_bottom_left()
        # pie chart
        fig_pie = px.pie(data, names="gender_country", title="Products Distribution")
        st.plotly_chart(fig_pie)

    with bottom_middle_columns:
        plot_bottom_right()
        plot_top_right()

    with bottom_left_column:
        pie_chart_for_country = px.pie(
            data,
            names="country",
            title="Distribution of Customers by Country",
        )
        st.plotly_chart(pie_chart_for_country)

    # Middle Row: Financial Insights
    st.write(
        "----------------------------------------------------------------------------------------"
    )
with st.container():
    st.header("Key Insights")

    col5, col6 = st.columns(2)

    with col5:
        balance_country_data = data.groupby("country")["balance"].sum().reset_index()
        fig5 = px.bar(
            balance_country_data,
            x="country",
            y="balance",
            title="Total Balance by Country",
        )
        st.plotly_chart(fig5)

    with col6:
        fig6 = px.histogram(
            data, x="credit_score", title="Credit Score Distribution", nbins=10
        )
        st.plotly_chart(fig6)

# Bottom Row: Age and Gender Insights
with st.container():
    col7, col8 = st.columns(2)

    with col7:
        age_group_data = data["age_group"].value_counts().reset_index()
        age_group_data.columns = ["Age Group", "Count"]
        fig7 = px.pie(
            age_group_data,
            values="Count",
            names="Age Group",
            title="Age Group Distribution",
        )
        st.plotly_chart(fig7)

    with col8:
        gender_country_data = (
            data.groupby(["country", "gender"]).size().reset_index(name="Count")
        )
        fig8 = px.bar(
            gender_country_data,
            x="country",
            y="Count",
            color="gender",
            title="Gender Distribution by Country",
        )
        st.plotly_chart(fig8)


print("-" * 20)


st.markdown("### Interactive Dashboards")

st.markdown("#### Churn Distribution by Age")

tab1, tab2, tab3 = st.tabs(["Bar chart", "Histogram", "Pie chart"])

# Bar chart for age vs churn, color by gender
with tab1:
    fig_bar = px.bar(data, x="age", y="churn", color="gender")
    st.plotly_chart(fig_bar)

with tab2:

    col1, col2, col3 = st.columns(3)
    with col1:
        x_column = st.selectbox("X-axis", numerical_columns)
    with col2:
        y_column = st.selectbox("Y-axis", numerical_columns)
    with col3:
        color_column = st.selectbox("Color", ["active_member", "churn", "gender"])

    fig_hist = px.histogram(data, x=x_column, y=y_column, color=color_column)
    st.plotly_chart(fig_hist)

with tab3:
    pie_param = st.selectbox("Select a parameter", data.columns)
    fig_pie = px.pie(data, names=pie_param, title="Products Distribution")
    st.plotly_chart(fig_pie)