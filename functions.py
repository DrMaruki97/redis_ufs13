import redis

def LandingPage(intestazione,comandi):
    print(intestazione)
    for i in range(len(comandi['LandingPage'])):
        print(f'{i+1}. {comandi['LandingPage'][i]}')


def UserPage(intestazione,comandi):
    print(intestazione)
    for i in range(len(comandi['UserPage'])):
        print(f'{i+1}. {comandi['UserPage'][i]}')


def login(user,psw,salt='wasd',r:Redis):
    try:
        password = r.get(user)
        print(str(hash(psw+salt)),password)
        if str(hash(psw+salt)) == password:           
            return True
        else:
            return False
    except:
        raise LookupError
   

def registration(user,psw,salt='wasd',r:Redis):
    try:
        r.set(user,str(hash(psw+salt)))
        r.lpush('system:all_users',user)
        # Mancano delle cose d ainfilare qua dentro
        return True
    except:
        return False
    

def cambio_psw(user, psw,r:Redis):
    try:
        r.set(user,str(hash(psw)))
        return True
    except:
        return False    