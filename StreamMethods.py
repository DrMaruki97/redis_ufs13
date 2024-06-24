import redis
import ui_functions as ui

# In tutte le funzioni l'argomento user è lo username della persona che ha effettuato il login in quell'istanza del programma,
# o_user è lo username con cui il nostro user desidera chattare

'''Metodo di invio di messaggi, prima controlla se esiste già lo stream della chat. Se presente aggiunge solo il messaggio,
altrimenti crea una voce nelle hash dei due utenti che ha come chiave il nome dell'altro utente (rispetto al proprietario dell'hash)
e come valore la stringa <nome stream>::<id dell'ultimo messaggio letto> (nel caso del ricevente questo primo messaggio l'ultimo 
messaggio letto non esiste e quindi è 0)'''
def send_message(user,o_user,r,message:dict,room=False):

    if not room:

        room = f'Room:{user}:{o_user}'
        msg_id = r.xadd(f'{room}',message)
        r.hset(f'User:{user}',f'{o_user}',f'{room}::{msg_id}')
        r.hset(f'User:{o_user}',f'{user}',f'{room}::0')
        return room

    else:

        r.xadd(f'{room}',message)



'''Metodo da far girare in un thread separato, continua a fare polling allo stream per nuovi messaggi e se li trova li printa e 
modifica l'hash dell'ascoltatore segnando l'id di quel messaggio come ultimo letto di quella chat'''

def eavesdropping(room,user,o_user,event,r):
    r_msgs = []
    while event:

        if r_msgs:
            msgs = r_msgs[0][1]
            for el in msgs:
                last_id = el[0]                                              # questa è da testare bene
                msg = el[1]
                if msg['mittente'] == user:
                    mitt = '>'
                else:
                    mitt = '<'
                print(mitt, msg['messaggio'], msg['datetime'])
            r.hset(f'Rooms:{user}',f'{o_user}',f'{room}::{last_id}')

        r_msgs = r.xread(streams={room:'$'})


'''Metodi da lanciare durante l'inizializzazione della chat per ottenere tutti i messaggi già visti (get_chat) e tutti i messagi
inviati dall'altro utente mentre noi non eravamo connessi (get_new_msgs). la parte di "printing" della chat è gestita da altre funzioni'''

def get_chat(room,last_id,r):
    chat = r.xrange(f'{room}','-',f'{last_id}')
    return chat
    

def get_new_msgs(room,last_id,user,o_user,r):
    chat = r.xrange(f'{room}',f'({last_id}','+')
    if chat:
        last_id = chat[-1][0]
        r.hset(f'Rooms:{user}',o_user,last_id)
    return chat

'''Funzione che fissa un expiration per una room'''

def set_timer(room,r):
    r.expire(room,60)


def send_timed_message(user,o_user,r,message:dict,room=False):

    if not room:

        room = f'Timed:Room:{user}:{o_user}'
        msg_id = r.xadd(f'{room}',message)
        r.hset(f'Timed:Rooms:{user}',f'{o_user}',f'{room}::{msg_id}')
        r.hset(f'Timed:Rooms:{o_user}',f'{user}',f'{room}::0')
        return room

    else:

        r.xadd(f'{room}',message)

