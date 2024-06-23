import streamlit as st
import random
import time
from Login import streamlit_logout


a = time.strftime("%d/%m/%Y, %H:%M -")
a



if 'user' in st.session_state:
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

st.title('Chat')
selection = st.selectbox(label='Select who you wanna chat with.', options=['AI', 'Hoomanz'])


# Tutorial
# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-simple-chatbot-gui-with-streaming


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            f"***{selection}:*** Hello there! How can I assist you today?",
            f"***{selection}:*** Hi, human! Is there anything I can help you with?",
            f"***{selection}:*** Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up my man?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(f"***{st.session_state['user']}*** "+prompt)

    # Display assistant response in chat message container
    with st.chat_message(selection):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": selection, "content": response})
