from datetime import datetime
import json

with open('server.json', 'r')as fichier:
    server=json.load(fichier)
print (server)



users= server['users']
channels= server['channels']
messages= server['messages']


def id_name(nom):
    for user in users:
        if nom==user:
            idnom=user['id']
            return idnom


def menu():
    print('=== Messenger ===')
    print( '1. see users')
    print('2. see channels')
    print('x. Leave')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
    
    elif choice =='1':
        user()

    elif choice=='2':
        channel()
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
    print(channels)
     



def channel():
    for channel in channels:
        print(channel['id'], channel['name'])
        print("1.choose group")
        print("2.New group")
        print("x. menu ")
        choice2 = input('Enter a choice and press ENTER: ')
    if choice2=='1':  
       choice22=int(input("group number"))
       for message in messages:
            if choice22 == message['channel']:
                print(message['sender_id'],message['content'])
            else:  
                print("no group")
    elif choice2== 'x':
        menu()
    elif choice2 == '2':
        newgroup()
        


    



menu()


