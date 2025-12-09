from datetime import datetime
import json

with open("server.json", "r") as fichier:
    server=json.load(fichier)
print (server)

def sauvegarder(new_server):
    with open ("server.json","w") as fichier:
        json.dump(new_server, fichier , ensure_ascii=False, indent=4)


users= server['users']
channels= server['channels']
messages= server['messages']


def id_name(nom): #donne l'identifiant à partir du nom
    for user in users:
        if nom==user['name']:
            idnom=user['id']
            return idnom
def name_id(id):#donne le nom a parti de l'identifiant
    for user in users:
        if id==user['id']:
            nomid=user['name']
            return nomid
        
def menu():
    print('=== Messenger ===')
    print( '1. See users')
    print('2. See channels')
    print('3. Send messages')
    print('x. Leave')
    print('================')
    print()
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
    
    elif choice =='1':
        user()

    elif choice=='2':
        channel()
    elif choice=='3':
        user_id=id_name(input('votre nom?'))
        newmessages(user_id)
    else:
        print('Unknown option:', choice)

def user():
    for user in users:
        print (user['id'], user['name']) 
    print ('n.create user')
    print ('x.Main menu')
    choice1 = input('Enter a choice and press ENTER: ')
    if choice1 =='x':
          menu()
    if choice1=='n':
        name=input('Name: ')
        user_ids=[]
        for user in users:
            user_ids.append(user['id'])
        newid= max(user_ids)+1
        users.append ( {'id':newid,'name':name })
        sauvegarder(server)
        print(users)

def newgroup():
    groupname= input ('Group Name')
    print (users)
    id_menbres=[]
    nb_pers= int(input('combien utilisateurs'))
    for i in range (0,nb_pers):
        id_pers=int(input('Id du membre')) 
        id_menbres.append(id_pers)
    channel_ids=[]
    for channel in channels:
        channel_ids.append(channel['id'])
    newgroup_id= max(channel_ids)+1
    channels.append ( {'id':newgroup_id,'name':groupname,'menbers_ids':id_menbres})
    sauvegarder(server)
    print(channels)

def newmessages(user_id):
    print('voici les groupes ou vous etes:')
    for channel in channels:
        if user_id in channel['menbers_ids']:
            print(channel['id'],channel['name'],channel['menbers_ids'])

    gp = int(input('Donner l \'indentifiant du groupe '))
    texte= input('write a message')
    new_message={
        'id':int(len(messages)+1),
        'channel': gp,
        'sender_id':user_id,
        'content':texte,
        'reception_date':datetime.now().isoformat()
    }
    messages.append(new_message)
    sauvegarder(server)
    print("1.send another message")
    print("x. return")
    choicem=input('Enter a choice and press ENTER:' )
    if choicem=='1':
        newmessages(user_id)
    elif choicem=='x':
        menu()





def channel():
    for channel in channels:
        print(channel['id'], channel['name'])
    
    print("1.choose group")
    print("2.New group")
    print("x. menu ")
    choice2 = input('Enter a choice and press ENTER: ')
    if choice2=='1':  
        choice22=int(input("group number"))
        for channel in channels: #on parcourt les channels si on en un id qui match on sort de la boucle avec break ( on a utilisé un for else) 
            if choice22 == channel['id']:
                print(channel)
                for ids in channel['menbers_ids']: # on transforme l'id en nom
                    print(name_id(ids))
                    
                    for message in messages:
                        if choice22== message["channel"]:  #on affiche le message 
                            print (message['content'])
                    break
            break
        else:  
            print("no group")

        
    elif choice2== 'x':
        menu()
    elif choice2 == '2':
        newgroup()










menu()

