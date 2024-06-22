import datetime as dt
import StreamMethods as sm

def Page(page):
    print(intestazione)
    for i in range(len(comandi[page])):
        print(f'{i+1}. {comandi[page][i]}')
    


def wrg_cmd():
    print('Comando non valido')


def chats(diz):
    lista = list(diz.keys())
    for i in range(len(lista)):
        print(f'{i+1}  {lista[i]}')
    return lista


def msgs(user,messaggi:list):
    if messaggi:
        for el in messaggi:
            msg = el[1]
            if msg['mittente'] == user:
                mitt = '>'
            else:
                mitt = '<'
            print(f'{mitt} {msg['messaggio']}\t{msg['datetime']}')


def speak(user):
    messaggio = input('>> ')
    date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {'mittente':user,'messaggio':messaggio,'datetime':date}
