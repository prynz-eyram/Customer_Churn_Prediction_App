import streamlit as st
import numpy as np
import pandas as pd
 
st.set_page_config(
    page_title='Home page',
    page_icon=':)',
    layout='wide'
)
 
def main():
    st.title('Customer Churn Prediction App')
    st.markdown(
        """
        <style>
            .title {
                text-align: center;
                font-size: 36px;
                color: #0066ff;
                padding-bottom: 20px;
            }
            .info {
                font-size: 18px;
                color: #333333;
                line-height: 1.6;
            }
            .subheader {
                font-size: 24px;
                color: #009933;
                padding-top: 20px;
            }
            .social-links {
                font-size: 20px;
                color: #0000ff;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
 
    st.write('Welcome to the Customer Churn Prediction App! This app predicts whether a customer will churn or not based on various features.')
 
    st.subheader('About the App')
    st.write("""
    Customer churn, also known as customer attrition, occurs when customers stop doing business with a company. This application aims to predict customer churn using machine learning algorithms.
    """)
 
    st.subheader('Source Code')
    st.write("The source code for this application is available on GitHub.")
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-View%20on%20GitHub-blue?logo=GitHub)](https://github.com/prynz-eyram/Customer-Churn-Prediction-App)")
    