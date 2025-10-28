from datetime import datetime

server = {
    'users': [
        {'id': 41, 'name': 'Alice'},
        {'id': 23, 'name': 'Bob'}
    ],
    'channels': [
        {'id': 12, 'name': 'Town square', 'member_ids': [41, 23]}
    ],
    'messages': [
        {
            'id': 18,
            'reception_date': datetime.now(),
            'sender_id': 41,
            'channel': 12,
            'content': 'Hi 👋'
        }
    ]
}
users= server['users']
channels= server['channels']
messages= server['messages']

def menu():
    print('=== Messenger ===')
    print( '1. see users')
    print('2. see channels')
    print('x. Leave')

print('=== Messenger ===')
print( '1. see users')
print('2. see channels')
print('x. Leave')

choice = input('Select an option: ')

if choice == 'x':
    print('Bye!')
    
elif choice =='1':

    for user in users:
        print (user['id'], user['name']) 
        print ('n.create user')
        print ('x.Main menu')
        choice1 = input('Enter a choice and press ENTER: ')
        identité=[]
        identite=identite.append(user['id'])
    if choice1='n'
        name= input('Name: ')
        id=
        if id in identité

elif choice=='2':

    for channel in channels:
        print(channel['id'], channel['name'])
    choice2 = int((input('choose group: , for menu enter 999 ')))
    for message in messages:
        if choice2 == message['channel']:
            print(message['sender_id'],message['content'])

        elif choice2== 999:
            menu()
        else:  

            print ("no group")
else:
    print('Unknown option:', choice)
