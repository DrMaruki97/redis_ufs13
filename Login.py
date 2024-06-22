import streamlit as st
import redis 

st.set_page_config(
    page_title="Login",
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
            st.session_state['status'] = r.get('dnd:user:'+user)
            return True
        else:
            return False

def streamlit_logout():
    del st.session_state['user']

r = redis.Redis(
    host='redis-16230.c328.europe-west3-1.gce.redns.redis-cloud.com',
    port=16230,
    password='y6ORUWqEjBvQZU3ICfuV8dgU8glOYFwL',
    decode_responses=True
    )
st.session_state['r'] = r


st.title('🔥 :red[Red]Chat 💬')

# Create an empty container
placeholder = st.empty()

# Insert a form in the container

if 'user' not in st.session_state:
  login_form = st.form(key='login_form')
  username = login_form.text_input(label='username')
  password = login_form.text_input(label='password', type='password')
  col1, col2, col3 = st.columns([1,1,1])
  submit_button = login_form.form_submit_button(label='submit')
  register_button = login_form.form_submit_button(label='register')




  if submit_button:
    login = streamlit_login(username, password, r)
    if login:
        st.session_state['user'] = username
        st.success("Login successful")
        st.switch_page('pages/Friends.py')
    else:
        st.error("Login failed")
  if register_button:
    if not r.exists('user:'+username):
        r.set("user:"+ username, password)
        f"Congratulations, {username}. You're in."
        st.session_state['user'] = username
        st.switch_page('pages/Friends.py')
    else:
        'Username already exists.'

      

if 'user' in st.session_state:
    st.empty()
    st.switch_page('pages/Friends.py')