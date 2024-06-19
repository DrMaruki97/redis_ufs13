import redis

def LandingPage(intestazione,comandi):
    print(intestazione)
    for i in range(len(comandi['LandingPage'])):
        print(f'{i+1}. {comandi['LandingPage'][i]}')


def UserPage(intestazione,comandi):
    print(intestazione)
    for i in range(len(comandi['UserPage'])):
        print(f'{i+1}. {comandi['UserPage'][i]}')


def login(user,psw,r,salt='wasd'):
    try:
        password = r.get(user)
        if str(hash(psw+salt)) == password:           
            return r.get(f'id:{user}')
        else:
            return False
    except:
        raise LookupError
   

def registration(user,psw,r,salt='wasd'):
    try:
        r.set(user.lower(),str(hash(psw+salt)))   #Dobbiamo ancora decidere come creare l'id
        return True
    except:
        return False
    

def cambio_psw(user, psw,r):
    try:
        r.set(user,str(hash(psw)))
        return True
    except:
        return False    