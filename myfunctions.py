import redis
import functions as f

def login(user,psw):
    if f.hash_pwd(psw) == r.get(user.lower()):
        return True
    return False


def registration(user,psw):

    try:
        r.set(user.lower(),f.hash_pwd(psw))
        r.set(f'DnD:{user}',0)
        return True
    except:
        return False
    

def check_disp(user):
    value = r.get(user.lower())
    if value:
        return True
    return False


def check_psw(psw):
    return 4<=psw<=16
        