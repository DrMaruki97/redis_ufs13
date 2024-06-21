# I messaggi vanno pubblicati nel channel che ha lo stesso nome della 'room' e nella seguente forma:
# <Mittente>::<Messaggio>::<datetime>  (Datetime fino ai minuti o volendo secondi) 



import redis
import time as t

def ActivateChat(r,id1,id2):            #Incompleto
    p = r.pubsub()
    p.subscribe(f'Room:{id2}:{id1}')


def Evesdropping(user,p,r):

    while True:                    # Deve continuare a fare polling per ricevere tutti i messaggi

        msg = p.get_message()      # Cerco un nuovo messagio, se non presente ritona Null
        if msg:
            room = msg['channel']
            values = msg['data'].split('sep')
            if values[0] != user:
                print(f'< {values[1]}  {values[2]}')
                r.zadd(room, {})
        t.sleep(2)

            

