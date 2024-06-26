import streamlit as st
import numpy as np
import pandas as pd
import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.base import TransformerMixin
import datetime


st.set_page_config(
    page_title='Predict',
    page_icon=':)',
    layout='wide'
)

# Check if the user is authenticated
if not st.session_state.get("authentication_status"):
    st.info('Please log in to access the application from the homepage.')
else:
    # Define the LogTransformer class
    class LogTransformer:
        def __init__(self, constant=1):
            self.constant = constant
    
        def transform(self, X_train):
            return np.log1p(X_train + self.constant)

    # Define BooleanToStringTransformer class
    class BooleanToStringTransformer(TransformerMixin):
        def fit(self, X, y=None):
            return self
    
        def transform(self, X):
            return X.astype(str)

    # Function to load logistic regression model
    @st.cache_data
    def load_logistic_model():
        model = joblib.load('./models/finished_logistic_model.joblib')
        return model

    # Function to load SGD model
    @st.cache_data
    def load_sgd_model():
        model = joblib.load('./models/finished_sgd_pipeline.joblib')
        return model

    # Create function to select model
    def select_model():

        # create columns to organize/design the select box for selecting model
        columns_1, columns_2, columns_3 = st.columns(3)
        with columns_1:
            # Display select box for choosing model
            st.selectbox('Select a Model', options=['Logistic Model', 'Sgd Model'], key='selected_model')
        with columns_2:
            pass
        with columns_3:
            pass

        if st.session_state['selected_model'] == 'Logistic Model':
            pipeline = load_logistic_model()   
        else:
            pipeline = load_sgd_model()
        
        # Load encoder
        encoder = joblib.load('./models/encoder.joblib')

        return pipeline, encoder

    if 'prediction' not in st.session_state:
        st.session_state['prediction'] = None
    if 'probability' not in st.session_state:
        st.session_state['probability'] = None

    # if not os.path.exists("./data/Prediction_history.csv"):
    #         os.mkdir("./data")

    # Create function to make prediction
    def make_prediction(pipeline, encoder):

        # Extract input features from session state
        gender = st.session_state['gender']
        SeniorCitizen = st.session_state['SeniorCitizen']
        Partner = st.session_state['Partner']
        Dependents = st.session_state['Dependents']
        tenure = st.session_state['tenure']
        PhoneService = st.session_state['PhoneService']
        MultipleLines = st.session_state['MultipleLines']
        InternetService = st.session_state['InternetService']
        OnlineSecurity = st.session_state['OnlineSecurity']
        OnlineBackup = st.session_state['OnlineBackup']
        DeviceProtection = st.session_state['DeviceProtection']
        TechSupport = st.session_state['TechSupport']
        StreamingTV = st.session_state['StreamingTV']
        StreamingMovies = st.session_state['StreamingMovies']
        Contract = st.session_state['Contract']
        PaperlessBilling = st.session_state['PaperlessBilling']
        PaymentMethod = st.session_state['PaymentMethod']
        MonthlyCharges = st.session_state['MonthlyCharges']
        TotalCharges = st.session_state['TotalCharges']

        # Define columns and create DataFrame
        columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents',
        'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
        'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
        'PaymentMethod', 'MonthlyCharges', 'TotalCharges']
        
        data = [[gender, SeniorCitizen, Partner, Dependents,
        tenure, PhoneService, MultipleLines, InternetService,
        OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
        StreamingTV, StreamingMovies, Contract, PaperlessBilling,
        PaymentMethod, MonthlyCharges, TotalCharges]]
        
        #Create a Dataframe
        df = pd.DataFrame(data, columns=columns)

        df["Date_of_prediction"] = datetime.date.today()
        df["Model"] = st.session_state["selected_model"]

        df.to_csv("./data/Prediction_history.csv", mode='a', header=not os.path.exists("./data/Prediction_history.csv"), index=False)

        # Make prediction
        predict = pipeline.predict(df)
        prediction = int(predict[0])

        # Inverse transform prediction label
        prediction = encoder.inverse_transform([prediction])

        # get probability
        probability = pipeline.predict_proba(df)

        # Update session_state with prediction and probability
        st.session_state['prediction'] = prediction
        st.session_state['probability'] = probability

        if 'prediction' not in st.session_state:
            st.session_state['prediction'] = None

        # Store prediction details in session state
        st.session_state.prediction_details = {
            'Prediction': prediction[0],
            'Probability': probability[0],
            'Gender': gender,
            'SeniorCitizen': SeniorCitizen,
            'Partner': Partner,
            'Dependents': Dependents,
            'Tenure': tenure,
            'PhoneService': PhoneService,
            'MultipleLines': MultipleLines,
            'InternetService': InternetService,
            'OnlineSecurity': OnlineSecurity,
            'OnlineBackup': OnlineBackup,
            'DeviceProtection': DeviceProtection,
            'TechSupport': TechSupport,
            'StreamingTV': StreamingTV,
            'StreamingMovies': StreamingMovies,
            'Contract': Contract,
            'PaperlessBilling': PaperlessBilling,
            'PaymentMethod': PaymentMethod,
            'MonthlyCharges': MonthlyCharges,
            'TotalCharges': TotalCharges
        }

        return prediction, probability

        return prediction, probability

    # Main function
    def main():
        
        pipeline, encoder = select_model() # Select model    
        
        # User input form
        with st.form('Features'):
            

            # Create a layout for better organization of the input form
            Demographic_Information, Contract_and_Billing, Service_Information_1, Service_Information_2 = st.columns(4)

            # Display input fields
            with Demographic_Information:
                # Demographic Information
                st.header('Demograph')
                gender = st.selectbox('Select Gender', ['Male', 'Female'], key='gender')
                SeniorCitizen = st.number_input('Is Customer a Senior Citizen (1 = yes and 0 = No)', min_value=0, max_value=1, key='SeniorCitizen' )
                Partner = st.selectbox('Partner', ['Yes', 'No'], key='Partner')
                Dependents = st.selectbox('Dependents', ['Yes', 'No'], key='Dependents')

            with Contract_and_Billing:
                # Contract and Billing Information
                st.header('Contract')
                Contract = st.selectbox('Contract', ['Month-to-month', 'One year', 'Two year'], key='Contract')
                PaperlessBilling = st.selectbox('Paperless Billing', ['Yes', 'No'], key='PaperlessBilling')
                PaymentMethod = st.selectbox('Select Payment Method', ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], key='PaymentMethod')
                MonthlyCharges = st.number_input('Enter Monthly Charges', min_value=18, max_value=118, key='MonthlyCharges')
                TotalCharges = st.number_input('Enter Total Charges', min_value=19, max_value=8670, key='TotalCharges')

            with Service_Information_1:
                # Service Information
                st.header('Services')
                tenure = st.number_input('Tenure (months)', min_value=0, max_value=72, key='tenure')
                PhoneService = st.selectbox('Select Phone Service', ['Yes', 'No'], key='PhoneService')
                MultipleLines = st.selectbox('Select Multiple Lines', ['Yes', 'No', 'No phone service'], key='MultipleLines')
                InternetService = st.selectbox('Select Internet Service', ['DSL', 'Fiber optic', 'No'], key='InternetService')
                OnlineSecurity = st.selectbox('Select Online Security', ['Yes', 'No', 'No internet service'], key='OnlineSecurity')
            
            with Service_Information_2:
                st.header("...")    
                OnlineBackup = st.selectbox('Select Online Backup', ['Yes', 'No', 'No internet service'], key='OnlineBackup')
                DeviceProtection = st.selectbox('Select Device Protection', ['Yes', 'No', 'No internet service'], key='DeviceProtection')
                TechSupport = st.selectbox('Select Tech Support', ['Yes', 'No', 'No internet service'], key='TechSupport')
                StreamingTV = st.selectbox('Select Streaming TV', ['Yes', 'No', 'No internet service'], key='StreamingTV')
                StreamingMovies = st.selectbox('Select Streaming Movies', ['Yes', 'No', 'No internet service'], key='StreamingMovies')

            
            # Submit button to make prediction
            st.form_submit_button ('Predict', on_click=make_prediction, kwargs=dict(
                pipeline=pipeline, encoder=encoder))

    if __name__ == '__main__':
        st.title('Predict Churn')
        main()

        prediction = st.session_state['prediction']
        probability = st.session_state['probability']

        if not prediction:
            st.markdown('### Prediction would show here')
        elif prediction == 'Yes':
            probability_yes = probability[0][1] * 100
            st.markdown(f"### The Customer will Churn with a probability of {round(probability_yes, 2)}%")
        else:
            probability_no = probability[0][0] * 100
            st.markdown(f"### The Customer will not Churn with a probability of {round(probability_no, 2)}%")