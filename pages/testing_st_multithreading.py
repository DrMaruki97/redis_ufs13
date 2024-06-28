import streamlit as st
import redis
from functions import hash_pwd, sign_up
import time
import threading
from typing import Any, TypeVar, cast

st.set_page_config(
    page_title="Testing",
    page_icon="🔥",
)


def my_handler(message):
        print('MY HANDLER: ', message['data'])
        with open("test.txt", 'a') as test:
              test.write("\n" + message['data'])
pub = st.session_state.r.pubsub()
pub.subscribe(**{'my-channel': my_handler})
pub.get_message()
thread = pub.run_in_thread(sleep_time=0.001)

text_area_ = st.text_area(label='type')
send = st.button(label='Rereun')
toggle = st.toggle('Auto update.')
if send:
    st.session_state.r.publish('my-channel', text_area_)




            


#val = st.slider("Value", 0, 50, 0)
#val = st.session_state.pub.subscribe(**{'my-channel': my_handler})

st.session_state['queue'] = ['']

def stream_data(message):
    for word in message.split(' '):
        yield word + " "
        time.sleep(0.03)


while toggle:
    time.sleep(0.5)
    while True:
        with open("test.txt", 'r') as test2:
            read = test2.readlines()[-1]
            if read != st.session_state['queue'][-1]:
                st.session_state['queue'].append(read)
                st.write_stream(stream_data(st.session_state['queue'][-1]))
            break




#Testing multithreading
#def my_handler(message):
        #print('MY HANDLER: ', message['data'])
        #st.write(message['data'])
        #st.session_state.bob.append(message['data'])
#st.session_state.pub = st.session_state.r.pubsub()
#st.session_state.pub.subscribe(**{'my-channel': my_handler})
#pub.get_message()
#thread = st.session_state.pub.run_in_thread(sleep_time=0.001)
#add_script_run_ctx(thread)
#add_script_run_ctx(thread)
