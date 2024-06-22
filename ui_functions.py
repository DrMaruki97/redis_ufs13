import redis

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
    