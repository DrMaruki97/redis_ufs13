import streamlit as st
import random
import time
from Login import streamlit_logout

def pushMessagesInSession(idroom:str):
    #Questo metodo, data un room ID, ottiene i messaggi di quella room. Li formatta e li inserisce nella sessione.

    #Non potendo utilizzare i JSON su redis devo ricreare qualcosa di simile con Python
    # Ogni messaggio deve essere messages = [{timestamp:43499490, mittente:'pippo',messaggio:'ciao'},...]
    friendList = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")
    #hgetall è MOLTO strano

    messages = st.session_state.r.zrange(f"st:room:{friendList[selection]}", 0, 1, withscores=True)
    messages = list(messages)
    messages = [list(message) for message in messages]
    messages = [[message[0], str(int(message[1]))] for message in messages]
    formatted_messages = [{'timestamp':message[1], 'mittente':message[0].split(':')[0],'text':message[0].split(':')[1]} for message in messages]
    print(formatted_messages)

    st.session_state['chat'] = formatted_messages 





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

# Recupero la lista di amici in modo da poter selezionare le chat.
friendList = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")
# Questo hget mi fa tornare la friendlist, che altro non è che un dizionario. Pippo = {amico1 : chatroomID1, amico2 : chatroomID2}

selection = st.selectbox(label='Select who you wanna chat with.', options=friendList, index=None)
if not selection:
    'Seleziona un amico per iniziare a chattare.'
if selection:
    pushMessagesInSession(friendList[selection])
    for message in st.session_state.chat:        
        with st.chat_message(message['mittente']):
            mess = st.markdown(f"{message['timestamp']}: "+message['text'])

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
#if "messages" not in st.session_state:
#    st.session_state.messages = []

# Display chat messages from history on app rerun
#for message in st.session_state.messages:
 #   with st.chat_message(message["role"]):
  #      st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up my man?"):
    pass
    # Add user message to chat history
   # st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
  #  with st.chat_message("user"):
   #     st.markdown(f"***{st.session_state['user']}*** "+prompt)

    # Display assistant response in chat message container
 #   with st.chat_message(selection):
   #     response = st.write_stream(response_generator())
    # Add assistant response to chat history
   # st.session_state.messages.append({"role": selection, "content": response})
