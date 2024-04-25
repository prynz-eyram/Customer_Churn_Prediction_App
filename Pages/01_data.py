import streamlit as st
import numpy as np
import pandas as pd
import pyodbc

# Define a key for storing the data in the session state
DATA_KEY = "data_key"

# Set page configuration
st.set_page_config(
    page_title='View Data',
    page_icon='📊',
    layout='wide'
)

# Check if the user is authenticated
if not st.session_state.get("authentication_status"):
    st.info('Please log in to access the application from the homepage.')
else:

    # Title of the page
    st.title('Vodafone Data')

    # Cache the database connection function
    # @st.cache(allow_output_mutation=True)
    def establish_connection():
        connection = pyodbc.connect(
            "DRIVER={SQL Server};SERVER="
            + st.secrets["SERVER"]
            + ";DATABASE="
            + st.secrets["DATABASE"]
            + ";UID="
            + st.secrets["UID"]
            + ";PWD="
            + st.secrets["PWD"]
        )
        return connection

    # Cache the database query results
    @st.cache_data
    def query_database(query):
        conn = establish_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                # Convert fetched rows into a DataFrame
                df = pd.DataFrame.from_records(data=rows, columns=[column[0] for column in cur.description])
            return df
        finally:
            # Close the database connection
            conn.close()

    # Function to select features based on type
    def select_features(feature_type, df):
        if feature_type == 'Numerical Features':
            # Filter numerical features
            numerical_df = df.select_dtypes(include=np.number)
            return numerical_df
        elif feature_type == 'Categorical Features':
            # Filter categorical features
            categorical_df = df.select_dtypes(include='object')
            return categorical_df
        else:
            # Return the entire DataFrame
            return df

    if __name__ == '__main__':
        # Define the database query
        query = "select * from LP2_Telco_churn_first_3000"
        # Execute the query and get the data DataFrame
        data_df = query_database(query)

        # Set the data into the session state
        st.session_state[DATA_KEY] = data_df

        # Selectbox to choose the type of features to display
        columns_1, columns_2, columns_3 = st.columns(3)  # create columns to organize/design the select box
        with columns_1:
            selected_feature_type = st.selectbox("Select data features", options=['All Features', 'Numerical Features', 'Categorical Features'],
                                            key="selected_columns")
        with columns_2:
            pass
        with columns_3:
            pass

        # Display the selected features
        if selected_feature_type == 'All Features':
            # Show all features if selected
            st.write(st.session_state[DATA_KEY])
        else:
            # Show selected type of features
            st.write(select_features(selected_feature_type, st.session_state[DATA_KEY]))
