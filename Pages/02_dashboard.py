import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(
    page_title='Dashboard',
    page_icon='📈',
    layout='wide'
)

# Check if the user is authenticated
if not st.session_state.get("authentication_status"):
    st.info('Please log in to access the application from the homepage.')
else:

    st.title('Vodafone Data Insights Dashboard')

    # Access data from session state
    data = st.session_state.get("data_key", None)

    if data is not None:
        # EDA Dashboard
        if st.sidebar.checkbox("EDA Dashboard"):
            st.header("Exploratory Data Analysis 🔍")

            # Main function
            def main():
            
                with st.container():
                    st.header('Univariate')
                    co1, co2 = st.columns(2)
                                    
                    with co1:
                        fig = px.histogram(data, x="Contract", color="Contract", barmode="group", height=400, width=500)
                        fig.update_yaxes(title_text=None)
                        st.plotly_chart(fig)

                    with co2:
                        fig = px.box(data, x="tenure", height=400, width=500)
                        st.plotly_chart(fig)
                with st.container():
                    cn1, cn2 = st.columns(2)
                    
                    with cn1:
                        fig = px.histogram(data, x="TotalCharges", height=400, width=500)
                        fig.update_yaxes(title_text=None)
                        st.plotly_chart(fig)

                    with cn2:
                        fig = px.histogram(data, x="MonthlyCharges", height=400, width=500)
                        fig.update_yaxes(title_text=None)
                        st.plotly_chart(fig)
                        
                with st.container():
                    st.header('Bivariate')
                    c1, c2 = st.columns(2)
                
                    with c1:
                        senior_citizen_pie = px.pie(data, names='SeniorCitizen', title='Churn rate: Senior Vs Non-senior Citizens')
                        st.plotly_chart(senior_citizen_pie, use_container_width=True)

                    with c2:
                        fig = px.histogram(data, x='PaymentMethod', color='Churn', barmode='stack',
                                color_discrete_map={'Yes': 'Firebrick', 'No': 'blue'},
                                labels={'PaymentMethod': 'Payment Method', 'Churn': 'Churn'},
                                title='Churn Patterns by Payment Method')
                        fig.update_layout(xaxis_title='Payment Method', yaxis_title='Count', showlegend=True)
                        st.plotly_chart(fig, use_container_width=True)        
                    
                with st.container():
                    st.header('Multivariate')
                    ca1, ca2 = st.columns(2)
                    

                    with ca1:  
                        data1 = data[["tenure", "MonthlyCharges", "TotalCharges", "Churn"]]
                        fig = px.scatter_matrix(data1, dimensions=["tenure", "MonthlyCharges", "TotalCharges"],
                                            color="Churn", symbol="Churn", title="Pairplot of Churn Features")
                        st.plotly_chart(fig, use_container_width=True)

                    with ca2:
                        correlation_matrix = data.corr(numeric_only=True)
                        plt.figure(figsize=(10, 8))
                        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
                        plt.title("Correlation Matrix")
                        st.pyplot(plt)
                            

            if __name__ == '__main__':
                main()

        # KPIs Dashboard
        if st.sidebar.checkbox("KPIs Dashboard"):
            st.title("Key Performance Indicators")
            # Calculate KPIs
            churn_rate = (data["Churn"].sum() / data.shape[0]) * 100
            average_tenure = data['tenure'].mean()
            average_monthly_charges = data['MonthlyCharges'].mean()
            total_revenue = data['MonthlyCharges'].sum()

            # Display KPIs
            st.markdown(
                f"""
                <div style="background-color: #E6E6FA; border-radius: 10px; width: 80%; margin-top: 20px;" >
                    <h3 style="margin-left: 30px">KPI'S</h3>
                    <hr>
                    <h5 style="margin-left: 30px"> Churn Rate: {churn_rate:.2f}%.</h5>
                    <hr>
                    <h5 style="margin-left: 30px">Average Tenure: {average_tenure:.2f} months</h5>
                    <hr>
                    <h5 style="margin-left: 30px">Average Monthly Charges: ${average_monthly_charges:.2f}</h5>
                    <hr>
                    <h5 style="margin-left: 30px">Total Revenue: ${total_revenue:.2f}</h5>
                    <hr>
                    <h5 style="margin-left: 30px">Data Size: {data.size}</h5>
                </div>
                """,
                unsafe_allow_html=True,
            )

            
    else:
        st.warning("Data not found. Please load the data first.")
