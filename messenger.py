from datetime import datetime
import json



class User:
    def __init__(self, id:int,name:str):
        self.id=id
        self.name=name
class Channels:
    def __init__(self,name:str,id:int, menbers_ids:list):
        self.name=name
        self.id=id
        self.menbers_ids= menbers_ids
class Messages:
    def __init__(self,channel:int,id:int, content:str, sender_id:int, reception_date: str):
        self.channel=channel
        self.id=id 
        self.content=content
        self.sender_id=sender_id
        self.reception_date=reception_date





with open("server.json", "r") as fichier:
    server=json.load(fichier)
    user_list:list[User]=[]
    channel_list:list[Channels]=[]
    message_list:list[Messages]=[]
    for user in server['users']:
        user_list.append (User(user['id'],user['name']))
        server['users']=user_list
    for channel in server['channels']:
        channel_list.append (Channels(channel['name'],channel['id'],channel['menbers_ids'] ))
        server['channels']=channel_list
    for message in server['messages']:
        print (message)
        message_list.append (Messages (message['content'],message['reception_date'],message ['sender_id'],message ['id'], message['channel']))
        server['messages']=message_list

users= server['users']
channels= server['channels']
messages= server['messages']

def sauvegarder(new_server):
    server2 = {}
    dico_user_list:list[dict]=[]
    for user in server['users']:
        dico_user_list.append({'name': user.name, 'id': user.id})
        server2['users']= dico_user_list
        dico_channel_list:list[dict]=[]
    for channel in server['channels']:
        dico_channel_list.append({'name': channel.name, 'id': channel.id, 'menbers_ids': channel.menbers_ids})
        server2['channels']= dico_channel_list
        dico_mess_list:list[dict]=[]
    for mess in server['messages']:
        dico_mess_list.append({ "id": mess.id, "reception_date": mess.reception_date, "sender_id": mess.sender_id, "channel": mess.channel, "content": mess.content})
        server2['messages']=dico_mess_list
    print(server2)
    with open('server.json', 'w') as fichier:
        json.dump(server2, fichier, indent=4)


def id_name(nom): #donne l'identifiant à partir du nom
    for user in users:
        if nom==user.name:
            idnom=user.id
            return idnom
def name_id(id):#donne le nom a parti de l'identifiant
    for user in users:
        if id==user.id:
            nomid=user.name
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
        print (user.id, user.name) 
    print ('n.create user')
    print ('x.Main menu')
    choice1 = input('Enter a choice and press ENTER: ')
    if choice1 =='x':
          menu()
    if choice1=='n':
        name=input('Name: ')
        user_ids=[]
        for user in users:
            user_ids.append(user.id)
        newid= max(user_ids)+1
        usnew= User (newid,name )
        users.append( usnew)
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
        channel_ids.append(channel.id)
    newgroup_id= max(channel_ids)+1
    gpnew=Channels(newgroup_id,groupname,id_menbres)
    channels.append (gpnew)
    sauvegarder(server)
    print(channels)

def newmessages(user_id):
    print('voici les groupes ou vous etes:')
    for channel in channels:
        if user_id in channel.menbers_ids:
            print(channel.id,channel.name,channel.menbers_ids)

    gp = int(input('Donner l \'indentifiant du groupe '))
    texte= input('write a message')
    new_message= Messages(gp, int(len(messages)+1),texte,user_id, datetime.now().isoformat())
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
        print(channel.id, channel.name)
    
    print("1.choose group")
    print("2.New group")
    print("x. menu ")
    choice2 = input('Enter a choice and press ENTER: ')
    if choice2=='1':  
        choice22=int(input("group number"))
        for channel in channels: #on parcourt les channels si on en un id qui match on sort de la boucle avec break ( on a utilisé un for else) 
            if choice22 == channel.id:
                print(channel)
                for ids in channel.menbers_ids: # on transforme l'id en nom
                    print(name_id(ids))
                    
                    for message in messages:
                        if choice22== message.channel:  #on affiche le message 
                            print (message.content)
                    break
            break
        else:  
            print("no group")

        
    elif choice2== 'x':
        menu()
    elif choice2 == '2':
        newgroup()










menu()

