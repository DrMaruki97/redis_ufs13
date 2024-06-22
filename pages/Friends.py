import streamlit as st
from Login import streamlit_logout

if 'user' in st.session_state:
    st.sidebar.text(f"Currently logged in as {st.session_state['user']}")
    st.title('Friends')
    logout_button = st.sidebar.button(label='Logout')
    if logout_button:
        streamlit_logout()
        st.switch_page('Login.py')
else:
    st.info('Please Login from the Home page and try again.')
    st.stop()

friends = []

if not friends:
    st.write('***Your current friendlist:***')
    'It seems like you have no friends, just like in real life. 😂' 
else:
    friends


st.divider()
st.title('Add a friend')
friend = st.text_input(label='Type your friend username')




