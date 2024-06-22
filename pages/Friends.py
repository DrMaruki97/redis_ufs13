import streamlit as st
from Login import streamlit_logout
import pandas as pd

if 'user' in st.session_state:
    st.title('Friends')
    st.sidebar.text(f"Currently logged in as {st.session_state['user']}")
    if st.session_state['status'] == '1':
        st.sidebar.text(f"Do not disturb ⛔")
    else:
        st.sidebar.text(f"Available for chat ✔️ ")
    logout_button = st.sidebar.button(label='Logout')

    if logout_button:
        streamlit_logout()
        st.switch_page('Login.py')
else:
    st.info('Please Login from the Home page and try again.')
    st.switch_page('Login.py')

friends = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")
friends_df = pd.DataFrame({'User':friends.keys() for friend in friends})
friends_df['Remove'] = [False for friend in friends]

if not friends:
    st.write('***Your current friendlist:***')
    'It seems like you have no friends, just like in real life.'
    st.image(image='pages/pepecry.gif')
else:
    friends_df = st.data_editor(friends_df, hide_index=True)
    conf_remove = st.button(label='Remove from friendlist')
    friends_to_be_removed = [user for user in friends_df[friends_df['Remove']==True]['User']]
    if conf_remove and friends_to_be_removed:
        st.session_state.r.hdel(f"st:friendList:{st.session_state.user}", *friends_to_be_removed)
        # Che comando! Semplicemente deleta dall'hash table (la friendlist) dell'user loggato gli amici che sull'interfaccia sono marchiati con una X
        st.success('Removed your buddies.')




st.divider()
st.title('Add a friend')
friend = st.text_input(label='Type your friend username')
add_button = st.button(label='Add a friend')
if add_button:
    if st.session_state.r.exists('user:'+friend):
        st.session_state.r.hset(f"st:friendList:{st.session_state.user}", friend, 'temp')
        friends = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")
        friends_df = pd.DataFrame({'User':friends.keys() for friend in friends})
        st.success(f'Added {friend}')
    else: 
        st.error("User simply ain't there buddy")






