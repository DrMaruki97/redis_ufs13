import redis 

def LandingPage(intestazione,comandi:dict):
    print(intestazione)
    for el in comandi.keys('landingpage:*'):
        print(f'{el[el.index(':'):]} {comandi[el]}')


def UserPage(intestazione,comandi:dict):
    print(intestazione)
    for el in comandi.keys('userpage:*'):
        print(f'{el[el.index(':'):]} {comandi[el]}')


def login(r:Redis):
    user = input('username >> ')
    psw = input('password >> ')
    password = r.get(user)
    if str(hash(psw)) == password:
        return f'user:{user}:{password}'
    else:
        print('Username o Password non corretti')


def registration(r:Redis):
    user = input('Choose a username >> ')
    while r.get(user):
        print('Username not available')
        user = input('Choose a username >> ')
    psw = input('Choose a password >> ')
    r.set(user,str(hash(psw)))
    return f'user:{user}:{str(hash(psw))}'