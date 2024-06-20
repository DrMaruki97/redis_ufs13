import streamlit as st

friends = []

if not friends:
    st.write('***Your current friendlist:***')
    'It seems like you have no friends, just like in real life. 😂' 
else:
    friends


st.divider()
st.title('Add a friend')
friend = st.text_input(label='Type your friend username')




