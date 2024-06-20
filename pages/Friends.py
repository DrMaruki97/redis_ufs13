import streamlit as st

if 'user' in st.session_state:
    f"{st.session_state['user']}"
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




