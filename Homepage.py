import streamlit as st
from conn import connect
import redis

st.set_page_config(
    page_title="Homepage",
    page_icon="🔥",
)

def streamlit_login(user, password, r):
    print(user, password)
    if r.exists("user:"+user)==1:
        print('It exists!')
        actualPass = r.get("user:"+ user)
        print(actualPass)
        if actualPass==password:
            print('Password Match')
            st.session_state['user'] = user
            return True
        else:
            return False

def streamlit_logout():
    del st.session_state['user']

r = connect()


st.title('🔥 :red[Red]Chat 💬')

# Create an empty container
placeholder = st.empty()

# Insert a form in the container

if 'user' not in st.session_state:
  login_form = st.form(key='login_form')
  username = login_form.text_input(label='username')
  password = login_form.text_input(label='password', type='password')
  submit_button = login_form.form_submit_button(label='submit')


  if submit_button:
    login = streamlit_login(username, password, r)
    if login:
        st.session_state['user'] = username
        st.success("Login successful")
    else:
        st.error("Login failed")

if 'user' in st.session_state:
    st.empty()
    st.write(f"hello, {st.session_state['user']}")
    logout_button = st.button(label='logout')
    if logout_button:
        streamlit_logout()
