import functions as f
from time import time
import datetime

r = f.connect()


def publish_message(channel, message):
    r.publish(channel, message)
    save_msg(channel, message)


def message_handler(message):
    message = message['data'].split('::')
    print(f"{message[0]} : {message[1]}")


def subscribe_to_channel(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(**{channel: message_handler})
    thread = pubsub.run_in_thread(sleep_time=0.001)
    return thread


def chat_interface(user, channel,o_user_id):
    subscriber_thread = subscribe_to_channel(channel) #quando uno avvia la f. viene sottoscritto al canale

    try:
        while True:
            message = input(f"")
            if message.lower() == 'esc':
                break
            elif f.check_dnd(o_user_id):
                print('ERRORE: L\'utente selezionato ha la modalità Do Not Disturb attiva, non può ricevere messaggi')
            else:
                publish_message(channel, f"{user}::{message}")
    except KeyboardInterrupt:
        pass
    finally:
        subscriber_thread.stop()


def save_msg(channel, message):

    name = f"{channel[8:]}"

    instante = time()
    chat_name = r.zadd(f"room:{name}", {f"{message}": int(instante)})
    if name[0] == '£':
        r.expire(name,60)
    return chat_name


def history_chat(user,id_chat):
    history = r.zrevrange(f"room:{id_chat}", 0, 9, withscores=True)

    for message, score in history[::-1]:
        message = message.split('::')
        dt = datetime.datetime.fromtimestamp(score)
        ora = dt.strftime("%d-%m-%Y %H:%M:%S")
        print(f"{freccine(user,message[0])}  {message[1]}  {ora}")


def dnd_on(user):
    id_user = r.get(f"id_user:{user}")
    bit = r.getbit("sys:dndmap", int(id_user))
    if bit == 1:
        try:
            while True:
                input()
                print(f"L'utente selezionato ha la modalità Do Not Disturb attiva, non può ricevere messaggi")
                if bit == 0:
                    break
        except KeyboardInterrupt:
            exit()
    else:
        return False
    

def freccine(user,mittente):
    if mittente == user:
        return '>'
    else:
        return '<'
    

def group_chat(user,channel):
    subscriber_thread = subscribe_to_channel(channel) #quando uno avvia la f. viene sottoscritto al canale

    try:
        while True:
            message = input(f"")
            if message.lower() == 'esc':
                break
            else:
                publish_message(channel, f"{user}::{message}")
    except KeyboardInterrupt:
        pass
    finally:
        subscriber_thread.stop()


def group_hist(group):
    history = r.zrevrange(f"room:{group}", 0, 9, withscores=True)

    for message, score in history[::-1]:
        message = message.split('::')
        dt = datetime.datetime.fromtimestamp(score)
        ora = dt.strftime("%d-%m-%Y %H:%M:%S")
        print(f"{message[0]}> {message[1]}  {ora}")