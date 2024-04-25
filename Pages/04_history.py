import streamlit as st
import numpy as np
import pandas as pd
import os

st.set_page_config(
    page_title='History',
    page_icon=':)',
    layout='wide'
)

# Check if the user is authenticated
if not st.session_state.get("authentication_status"):
    st.info('Please log in to access the application from the homepage.')
else:

    st.title("Prediction History")

    # History page to display previous predictions
    def display_prediction_history():
        
        csv_path = "./data/Prediction_history.csv"
        df = pd.read_csv(csv_path)
        
        return df

    if __name__ == "__main__":
        df = display_prediction_history()
        st.dataframe(df)