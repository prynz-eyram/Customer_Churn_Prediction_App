import streamlit as st
import numpy as np
import pandas as pd
 
st.set_page_config(
    page_title='History',
    page_icon=':)',
    layout='wide'
)
 
# History page to display previous predictions
def history_page():
    st.title('Prediction History')
 
    # Check if prediction details exist in session state
    if 'prediction_details' not in st.session_state:
        st.write('No prediction history available.')
        return
 
    # Get all prediction details stored in session state
    prediction_details = st.session_state.prediction_details
 
    # Convert prediction details to DataFrame
    df_prediction = pd.DataFrame(prediction_details, index=[0])
 
    # Display prediction details
    st.header('Details')
    st.dataframe(df_prediction)
 
if __name__ == '__main__':
    history_page()
    