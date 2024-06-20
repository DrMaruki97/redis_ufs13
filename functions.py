import redis

def Page(intestazione,comandi,page):
    print(intestazione)
    for i in range(len(comandi[page])):
        print(f'{i+1}. {comandi[page][i]}')

def action():
    action = input('>> ')
    return action.lower()