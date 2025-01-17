import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide', page_title = 'Company Review', page_icon = 'static/core-4.png')
SideBarLinks()

# Creating title and getting relationship of user to the company
st.title("Review a Company")


# Getting company data to select position under review
def fetch_data():
    url = f'http://api:4000/c/Company'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

# Getting CompanyID
df = fetch_data()
position = st.selectbox("Select Company", df['Name'].unique())
index = df.index[df['Name'] == position].tolist()
if index:
    comID = int(df.loc[index[0], 'CompanyID'])
    st.write(f"**CompanyID**: {comID}")
else:
    comID = None
    st.error("No PositionID found for the selected position.")



menu = ['Applied To Work For', 'Worked For']
choice = st.selectbox("Connection To Company", menu)

# Creating form for if user applied to work for them
if choice == 'Applied To Work For':
    st.subheader("Company Review Form")
    with st.form(key='appto'):
        type = st.text_input("Extent of Relationship With Company")
        review = st.text_input("Review Space")
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            if not type or not review:
                st.error("Mising Input")
            else:
                comreview_data = {
                    "CompanyId": comID,
                    "Type": type,
                    "Description": review,
                    "EnvironmentRating": None,
                    "CultureRating": None
                }
                logger.info(f"Review form submitted with data: {comreview_data}")
                try:
                    response = requests.post('http://api:4000/c/CompanyReview', json=comreview_data)
                    if response.status_code == 200:
                        st.success("Review added successfully!")
                    else:
                        st.error(f"Error adding review: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")


# Creating form for if user worked for them
if choice == 'Worked For':
    st.subheader("Company Review Form")
    with st.form(key='workedfor'):
        type = st.text_input("Extent of Relationship With Company")
        review = st.text_input("Review Space")
        env_rating = st.number_input('Rating of Environment While Working (1-5)', 1, 5)
        culture_rating = st.number_input('Rating of Culture While Working (1-5)', 1, 5)
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            if not type or not review:
                st.error("Mising Input")
            else:
                comreview_data = {
                    "CompanyId": comID,
                    "Type": type,
                    "Description": review,
                    "EnvironmentRating": env_rating,
                    "CultureRating": culture_rating
                }
                logger.info(f"Review form submitted with data: {comreview_data}")
                try:
                    response = requests.post('http://api:4000/c/CompanyReview', json=comreview_data)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")