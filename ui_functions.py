import redis

def Page(intestazione,comandi,page):
    print(intestazione)
    for i in range(len(comandi[page])):
        print(f'{i+1}. {comandi[page][i]}')
    action = input('>> ').lower()
    return action


def wrg_cmd():
    print('Comando non valido')