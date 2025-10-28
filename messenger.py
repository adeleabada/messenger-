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
elif choice=='2':
    for channel in channels:
        print(channel['id'], channel['name'])
else:
    print('Unknown option:', choice)
