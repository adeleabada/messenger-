from messenger import User
from messenger import Channels
from messenger import Messages
from messenger import LocalStorage
from messenger import RemoteStorage
from messenger import UserInterface

#test de user d'abord repr marche, puis load dans local storage si fichier json et fit load, remplit bien, get user et add user apres 
def test_repr():
    u = User(70, 'Yamina')
    assert str(u) == 'user(Yamina)'

def test_get_users(): 
    fake = '''{
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ],
        "channels": [],
        "messages": []
    }'''
    with open('fake.json', 'w') as f: 
        f.write(fake)
    storage = LocalStorage('fake.json')
    users = storage.get_users()
    assert len(users)==2

def test_add_user():
    fake = '''{
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ],
        "channels": [],
        "messages": []
    }'''
    with open('fake.json', 'w') as f: 
        f.write(fake)
    storage = LocalStorage('fake.json')
    storage.create_users('helene')
    users = storage.get_users()
    # verifier taille users et helene est un nom dedans
    assert len(users)==3