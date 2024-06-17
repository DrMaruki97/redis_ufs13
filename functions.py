import redis

intestazione = '='*10 + '\nREDCHAT\n' + '='*10

def LandingPage():
    print(intestazione)
    comandi = r.get('system:LandingPage:comandi')
    for i in range(len(comandi)):
        print(f'{i+1}. {comandi[i]}')


def UserPage():
    print(intestazione)
    comandi = r.get('system:UserPage:comandi')
    for i in range(len(comandi)):
        print(f'{i+1}. {comandi[i]}')


def login():
    user = input('username >> ')
    psw = input('password >> ')
    password = r.get(user)
    if str(hash(psw)) == password:
        return f'user:{user}:{password}'
    else:
        print('Username o Password non corretti')


def registration():
    while True:
        user = input('Choose a username >> ')
        if r.get(user):
            print('username not available')
        else:
            break
    psw = input('Choose a password >> ')
    r.set(user,str(hash(psw)))
    r.lpush('system:all_users',user)
    return f'user:{user}:{str(hash(psw))}'