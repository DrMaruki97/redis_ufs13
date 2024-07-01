import datetime as dt

def page(intestazione,comandi,page):
    print(intestazione)
    for i in range(len(comandi[page])):
        print(f'{i+1}. {comandi[page][i]}')
    


def wrg_cmd():
    print('Comando non valido')


def view_list(lista):
    for i in range(len(lista)):
        print(f'{i+1}  {lista[i]}')


def msgs(user,messaggi:list):
    if messaggi:
        for el in messaggi:
            msg = el[1]
            if msg['mittente'] == user:
                mitt = '>'
            else:
                mitt = '<'
            print(mitt, msg['messaggio'], msg['datetime'])


def speak(user):
    messaggio = input('>> ')
    if messaggio:
        date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {'mittente':user,'messaggio':messaggio,'datetime':date}
    else:
        return False

def action():
    action = input('>> ').lower()
    return action

def exit():
    print('premi <enter> per uscire')