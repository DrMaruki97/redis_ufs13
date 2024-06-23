import redis



def login(user,psw,r):
    if psw == r.get(user.lower()):
        return True
    return False


def registration(user,psw,r):

    try:
        r.set(user.lower(),psw)
        r.set(f'DnD:{user}',0)
        return True
    except:
        return False
    

def check_disp(user,r):
    value = r.get(user.lower())
    if not value:
        return True
    return False


def check_psw(psw):
    return 4<=len(psw)<=16


def user_serch(pattern,r):
    users = r.scan(match = f'{pattern}*')[1]
    return users


def add_friend(user,friend,r):
    r.hset(f'User:{user}',friend,0)


def get_friends(user,r):
    friends = r.get(f'User:{user}')
    lista = list(friends.keys())
    return lista


        