import streamlit as st
import random
import time
from datetime import datetime
from Login import streamlit_logout


def pushMessagesInSession(idroom:str):
    #Questo metodo, data un room ID, ottiene i messaggi di quella room, li formatta e li inserisce nella sessione.

    #Non potendo utilizzare i JSON su redis devo ricreare qualcosa di simile con Python
    # Ogni messaggio deve essere messages = [{timestamp:43499490, mittente:'pippo',messaggio:'ciao'},...]

    messages = st.session_state.r.zrange(f"room:{idroom}", 0, -1, withscores=True)
    #hgetall è MOLTO strano. Restituisce una lista di Tuple. Piglio tutti i messaggi. di una room.
    #print('zget from redis:')
    #print(messages)
    # Qualche print il quale fine è solo quello di visualizzare cosa sto facendo

    messages = list(messages)
    messages = [list(message) for message in messages]
    messages = [[message[0], datetime.fromtimestamp(message[1])] for message in messages]
    formatted_messages = [{'timestamp':message[1].strftime("%d/%m/%Y, %H:%M"), 'mittente':message[0].split(':')[0],'text':message[0].split(':')[1]} for message in messages]
    #print(formatted_messages)
    # Tutto sto ambaradam mi crea una lista di dizionari. Ogni dizionario è un messaggio ben formattato e facilmente accessibile.

    st.session_state['chat'] = formatted_messages 
    # Infine pusho i messaggi nella sessione.


# Streamed response emulator
def response_generator():
    # Metodo per "animare" il messaggio in arrivo. Non sono sicuro che mi servirà.
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
    # Solita sidebar
else:
    st.info('Please Login from the Home page and try again.')
    st.switch_page('Login.py')
    # Solito redirect se non sei loggato.

st.title('Chat')


# Recupero la lista di amici in modo da poter recuperare gli idroom. 
friendList = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")
# Questo hget mi fa tornare la friendlist, che altro non è che un dizionario. Pippo = {amico1 : chatroomID1, amico2 : chatroomID2}

selection = st.selectbox(label='Select who you wanna chat with.', options=friendList, index=None)

if not selection:
    'Seleziona un amico per iniziare a chattare.'
if selection:
    pushMessagesInSession(friendList[selection])    
    # Nel momento in cui seleziono un amico con cui chattare vengono recuperati tutti i messaggi. 
    for message in st.session_state.chat:        
        with st.chat_message('user' if message['mittente']==st.session_state.user else message['mittente']):
            #sto IF serve a far cambiare l'icona del mittente. L'user loggato avrà un'icona personalizzata, così da renderlo distinguibile.
            mess = st.markdown(f"*:gray[{message['timestamp']}:]* "+message['text'])


# Accept user input
if prompt := st.chat_input("What is up my man?"):
    if st.session_state.r.get(f"st:dnd:user:{selection}")=='1':
        st.error(f"{selection} non vuole essere disturbato.")
        # Se l'utente al quale stiamo scrivendo è su Do not disturb non riusciremo ad inserire un messaggio nella chat.
    else:
        st.session_state.r.zadd(f'room:{friendList[selection]}', {f"{st.session_state.user}:{prompt}" : time.time()})
        # Questa parte appende il messaggio nello z set della chatroom quando l'utente scrive qualcosa.
        pushMessagesInSession(friendList[selection])
        # Refresho la lista dei messaggi
        st.rerun()
        # Faccio un rerun se viene inviato un nuovo messaggio così da aggiornare la chat.
    


    # Display assistant response in chat message container
 #   with st.chat_message(selection):
   #     response = st.write_stream(response_generator())
    # Add assistant response to chat history
   # st.session_state.messages.append({"role": selection, "content": response})
