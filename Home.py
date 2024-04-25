import pickle
from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Set Streamlit page configuration
st.set_page_config(
    page_title='Home page',
    page_icon='🏘️',
    layout='wide'
)

# Load configuration from YAML file
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize Streamlit Authenticator with configuration settings
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Perform user authentication
name, authentication_status, username = authenticator.login(location='sidebar')

# Handle authentication status
if authentication_status == False:
    st.error("Username/Password is incorrect")  # Display error message if authentication fails
    st.code("""
            Username: deofis
            Password: abc123""")
    
if authentication_status == None:
    st.warning("Please enter username and Password")  # Prompt user to enter username and password if not authenticated
    st.code("""
            Username: deofis
            Password: abc123""")


if authentication_status == True:
    # Define main content of the app
    def main():
            # Display welcome text
        st.markdown("<p style='text-align: left; color: #0066ff; font-size: 36px;'>Welcome to the Customer Churn Prediction App! 📊</p>", unsafe_allow_html=True)
            # Display downloaded image
        image_path = './images/image.png'  # Replace 'path_to_your_image.jpg' with the actual path to your image
        st.image(image_path, use_column_width=False, output_format = "auto")

        # st.title('Customer Churn Prediction App')
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

        st.write("Experience the future of telecommunications with our cutting-edge Customer Churn Prediction App! Powered by advanced analytics and machine learning, we offer Vodafone a decisive edge in customer retention. Say goodbye to churn uncertainty and hello to proactive strategies that redefine industry standards. Together, let's shape the future of telecommunications! 💼")

        st.subheader('About the App')
        st.write("""
        Customer churn, the silent storm that erodes business growth, meets its match in our innovative application. By seamlessly integrating state-of-the-art algorithms with comprehensive data analytics, we illuminate the path forward for Vodafone. Harnessing the power of predictive insights, we empower Vodafone to anticipate churn patterns and navigate towards sustained success.
        """)

        st.subheader('Source Code')
        st.write("Unleash your creativity and collaboration by clicking the link below! Our open-source ethos invites you to explore, contribute, and innovate with the source code on GitHub. Join the revolution in customer retention strategies and pave the way for a brighter tomorrow.")
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-View%20on%20GitHub-blue?logo=GitHub)](https://github.com/prynz-eyram/Customer_Churn_Prediction_App)")

        st.subheader('Social Handles')
        st.write("""
        Connect with me on social media:
        - [GitHub](https://github.com/prynz-eyram) 🐙
        - [LinkedIn](https://www.linkedin.com/in/prince-eyram-kofi-adzanku-1768102b) 💼
        """)
    
    # Add logout button to sidebar
    authenticator.logout("Logout", "sidebar")

    # Display sidebar with user's name
    st.sidebar.title(f"Welcome {name}")

    if __name__ == '__main__':
        main()