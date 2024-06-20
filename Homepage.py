import streamlit as st
from conn import connect
import redis


r = connect()

st.set_page_config(
    page_title="Homepage",
    page_icon="🔥",
)

st.title('🔥 :red[Red]Chat 💬')

# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"


# Insert a form in the container
def streamlit_login(log, user=None, password=None):
    if r.exists(email) and r.get("user:"+ email)==hash(password+'42'):
        st.session_state['user'] = user
        return True
    else:
        return False
def streamlit_logout():
    del st.session_state['user']


# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your credentials")
    email = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")
    f"{hash('a')}"

if submit and streamlit_login(email, email, password):
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
    st.success("Login successful")
    st.switch_page('pages/Friends.py')
elif submit and streamlit_login(email, email, password) == False:
    'Credenziali errate!'
    f'{password}'
    f'{hash(password+'42')}'
#elif submit and email != actual_email and password != actual_password:
    #st.error("Login failed")

