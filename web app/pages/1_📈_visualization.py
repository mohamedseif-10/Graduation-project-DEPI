import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time
st.markdown(
    """
    <style>

    [data-testid="stSidebar"] {
        background:#e4f0ff
;  /* Light blue background for sidebar */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    data = pd.read_csv("../Data/modified_Bank_Customer_Churn_Prediction.csv")
    return data


data = load_data()

@st.cache_data
def plot_gauge(
    target_value, indicator_color, indicator_suffix, indicator_title, max_bound
):
    num_frames = 30 
    values = np.linspace(
        0, target_value, num_frames
    )  
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
                        "font": {"size": 18, "weight": "bold", "color": "#f2c453"},
                    },
                )
            ],
            name=f"Value: {value}",  # Frame name
        )
        for value in values
    ]

    fig = go.Figure(
        data=frames[0].data, 
        layout=frames[0].layout,
        frames=frames,
    )

    fig.update_layout(
        height=200,
        margin=dict(l=26, r=26, t=0, b=0, pad=0),
    )
    placeholder = st.empty()

    for frame in frames:
        fig.update_traces(value=frame.data[0].value)
        placeholder.plotly_chart(
            fig, use_container_width=True
        )  # Render the updated figure
        time.sleep(0.005)  # Adjust speed of animation


@st.cache_data
def plot_top_right():
    pass


def plot_top_left():
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


def plot_bottom_left():
    active_churn_counts = (
        data.groupby(["active_member", "churn"]).size().reset_index(name="count")
    )
    active_churn_counts["active_member_status"] = active_churn_counts["active_member"].map(
        {0: "Inactive", 1: "Active"}
    )
    active_churn_counts["label"] = active_churn_counts.apply(
        lambda row: f"{'Churn' if row['churn'] == 1 else 'Non-Churn'} - {row['active_member_status']}",
        axis=1,
    )

    # Calculate total count
    total_count = active_churn_counts['count'].sum()

    # Create a new column for percentages
    active_churn_counts['percentage'] = (active_churn_counts['count'] / total_count) * 100

    custom_colors2 = ["#193967", "#0068c9", "#83c9ff", "#f2c453"]
    fig = px.pie(
        active_churn_counts,
        names="label",
        values="count",
        title="Churn vs Non-Churn by Active Membership",
        color_discrete_sequence=custom_colors2,
    )

    # Update traces to include percentage in textinfo
    fig.update_traces(
        textinfo="percent",  # Show both label and percentage
        textposition="inside",  # Show text inside the pie chart
        hoverinfo="label+percent+value",
        marker=dict(line=dict(color="#FFFFFF", width=2)),
    )

    # Customize layout for better aesthetics
    fig.update_layout(
        annotations=[
            dict(text=f"{row['percentage']:.2f}%", x=row['count'], y=row['count'], font_size=20, showarrow=False) 
            for index, row in active_churn_counts.iterrows()
        ]
    )

    st.plotly_chart(fig)

def plot_bottom_right():
    bins = [-1, 50000, 90000, 127000, np.inf]
    labels = ["0-50k", "50k-90k", "90k-127k", "127k+"]
    data["balance_seg"] = pd.cut(data["balance"], bins=bins, labels=labels, right=False)
    churned_data = data[data["churn"] == 1]

    # Count occurrences in each balance segment
    balance_churn_counts = churned_data["balance_seg"].value_counts().reset_index()
    balance_churn_counts.columns = ["balance_seg", "count"]

    # Create a pie chart for the balance segments of churned customers
    fig = go.Figure()
    custom_colors2 = [
        "#193967" ,
        "#0068c9",
        "#83c9ff",
        "#f2c453"
    ]
    fig.add_trace(
        go.Pie(
            labels=balance_churn_counts["balance_seg"],
            values=balance_churn_counts["count"],
            textinfo="label+percent",
            hole=0.3,
            marker=dict(
                colors=custom_colors2,  # Set the custom colors here
                line=dict(color="#FFFFFF", width=2)
            ),
        )
    )

    # Update layout for better readability
    fig.update_layout(
        title="Churned Customers Distribution by Balance Segmentation",
        height=340,
        margin=dict(l=23, r=26, t=100, b=0, pad=0),
    )
    st.plotly_chart(fig)

st.title("Customer Churn visualizations")
st.image("Background.jpg", use_column_width=True, width=700)
st.write("### Discover your inner treasure💰")
st.sidebar.info(
    """
    This page provides a detailed overview of the data used for predicting customer churn with interactive visualizations and dahsboards with key insights.
    """
)


st.markdown(
    """
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


# top_left_column, top_right_column = st.columns((5,5))

# with st.container():
#     with top_left_column:
#         plot_top_left()

#     with top_right_column:
#         plot_top_right()

with st.container():
    st.header("Key Insights")
    churned_data = data[data["churn"] == 1]
    tenure_churn_counts = (
        churned_data.groupby("tenure").size().reset_index(name="count")
    )
    tenure_churn_counts["rolling_mean"] = (
        tenure_churn_counts["count"].rolling(window=1, center=True).mean()
    )
    fig6 = px.histogram(
        data,
        x="tenure",
        title="Tenure Distribution with Churn Trend",
        nbins=30,
        color="churn",
    )
    fig6.update_layout(bargap=0.2)
    fig6.update_traces(marker_line_width=0.1, marker_line_color="black")
    fig6.update_xaxes(title_text="Tenure")

    # Add mean tenure line
    mean_tenure = data["tenure"].mean()
    fig6.add_vline(
        x=mean_tenure,
        line_width=2,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Mean Tenure: {mean_tenure:.2f}",
        annotation_position="top left",
    )

    # Add trend line for churned customers (rolling mean)
    fig6.add_scatter(
        x=tenure_churn_counts["tenure"],
        y=tenure_churn_counts["rolling_mean"],
        mode="lines",
        line=dict(color="orange", width=3),
        name="Churned Customers",
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig6)

with st.container():
    col7, col8 = st.columns((2,2.4))

    with col7:


        churned_data = data[data["churn"] == 1]
        age_group_counts = churned_data["age_group"].value_counts()
        age_group_percentages = age_group_counts.reset_index()

        age_group_percentages.columns = ["age_group", "count"]
        age_group_percentages["percentage"] = (
            age_group_percentages["count"] / age_group_percentages["count"].sum() * 100
        ).round(2)

        custom_colors = ["#0068c9", "#83c9ff", "#f2c453"]
        fig = px.pie(
            age_group_percentages,
            names="age_group",
            values="percentage",
            title="Churn Percentage by Age Group",
            labels={"percentage": "Percentage"},
            color_discrete_sequence=custom_colors,
            # how to make hole in the middle
            hole=0.4,
        )
        

        fig.update_layout(
            title_text="Percentage of Churned Customers by Age Group",
            legend_title_text="Age Groups",
            height=400,
            margin=dict(l=22, r=22, t=100, b=0, pad=0),
        )

        fig.update_traces(
            hoverinfo="label+percent+value",
            textinfo="percent",
            textfont_size=16,
            marker=dict(line=dict(color="#FFFFFF", width=2)),
        )

        st.plotly_chart(fig)

    with col8:
        data["gender_country"] = data["gender"] + " " + data["country"]

        gender_country_counts = (
            data.groupby(["gender_country", "churn"]).size().unstack(fill_value=0)
        )

        gender_country_counts.reset_index(inplace=True)

        gender_country_counts_melted = gender_country_counts.melt(
            id_vars="gender_country",
            value_vars=[0, 1],
            var_name="Churn Status",
            value_name="Count",
        )

        gender_country_counts_melted["Churn Status"] = gender_country_counts_melted[
            "Churn Status"
        ].map({0: "Non-Churned", 1: "Churned"})

        gender_country_counts_melted["country"] = gender_country_counts_melted[
            "gender_country"
        ].apply(lambda x: x.split(" ")[-1])

        gender_country_counts_melted["gender_order"] = gender_country_counts_melted[
            "gender_country"
        ].apply(lambda x: x.split(" ")[0])
        
        gender_country_counts_melted.sort_values(
            by=["country", "gender_order"], inplace=True
        )

        color_map = {
            "Churned": "#f2c453",  # Color for churned
            "Non-Churned": "#0068c9"  # You can choose another color for non-churned
        }

        fig = px.bar(
            gender_country_counts_melted,
            x="gender_country",
            y="Count",
            color="Churn Status",
            labels={
                "gender_country": "Gender - Country",
                "Count": "Number of Customers",
            },
            title="Customer Count by Gender and Country for Churn Status",
            color_discrete_map=color_map,  # Apply custom color mapping
            #rotate x-axis labels
            
        )

        fig.update_layout(
            xaxis_title="Gender - Country",
            yaxis_title="Number of Customers",
            width=1200,
            height=500,
            barmode="group",
            xaxis_tickangle=90,
        )

        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig)

bottom_left_column, bottom_right_column= st.columns((3, 3))
with st.container():
    with bottom_left_column:
        plot_bottom_left()
    with bottom_right_column:
        plot_bottom_right()


print("-" * 20)


st.markdown("### Discover more Interactive Dashboards 📊")

tab1, tab2, tab3 = st.tabs(["Bar chart", "Histogram", "Pie chart"])

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
