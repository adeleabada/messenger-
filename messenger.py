from datetime import datetime

import json

import requests

import argparse

    



class User:

    def __init__(self, id:int,name:str):

        self.id=id

        self.name=name

    def __repr__(self)->str:

        return "user("+self.name+")"

        

        return

class Channels:

    def __init__(self,name:str,id:int, menbers_ids:list):

        self.name=name

        self.id=id

        self.menbers_ids= menbers_ids

    def __repr__(self)->str:

        return "channel("+self.name+")"

class Messages:

    def __init__(self,channel:int,id:int, content:str, sender_id:int, reception_date: str):

        self.channel=channel

        self.id=id 

        self.content=content

        self.sender_id=sender_id
        # Le type datetime de la bibliothèque datetime est plus
        # adapté pour représenter des horodatages. Il vous permet
        # notamment de gérer l'affichage de façon unifiée, quelle qu'ait
        # été la source des données.
        # Son utilisation demande de convertir les str que vous recevez
        # en datetime, puis d'utiliser datetime dans tout le programme,
        # puis de convertir datetime en str lors de l'affichage.
        self.reception_date=reception_date



class LocalStorage:

    def __init__(self, file_path:str):

        self.file_path=file_path



    def load_server(self):

        with open(self.file_path, "r") as fichier:

            server=json.load(fichier)

            self.user_list:list[User]=[]

            self.channel_list:list[Channels]=[]

            self.message_list:list[Messages]=[]

        for user in server['users']:

            self.user_list.append(User(user['id'],user['name']))

           

        for channel in server['channels']:

            self.channel_list.append(Channels(channel['name'],channel['id'],channel['menbers_ids'] ))

            

        for message in server['messages']:

            self.message_list.append(Messages(message['channel'],message['id'],message['content'],message['sender_id'],message['reception_date']))



    def sauvegarder(self):

        server2 = {}

        dico_user_list:list[dict]=[]

        for user in self.user_list:

            dico_user_list.append({'name': user.name, 'id': user.id})

            server2['users']= dico_user_list

            dico_channel_list:list[dict]=[]

        for channel in self.channel_list:

            dico_channel_list.append({'name': channel.name, 'id': channel.id, 'menbers_ids': channel.menbers_ids})

            server2['channels']= dico_channel_list

            dico_mess_list:list[dict]=[]

        for mess in self.message_list:

            dico_mess_list.append({ "id": mess.id, "reception_date": mess.reception_date, "sender_id": mess.sender_id, "channel": mess.channel, "content": mess.content})

            server2['messages']=dico_mess_list

        with open(self.file_path, 'w') as fichier:

            json.dump(server2, fichier, indent=4)



            

    def get_users(self) -> list[User]:

        self.load_server()

        return self.user_list


    # N'oubliez pas de typer toutes vos fonctions
    def create_users(self,name: str) -> None:

        # Pas besoin d'affecter le résultat de load_server
        # à une variable (d'ailleurs load_server ne renvoie rien)
        self.load_server()

        user_ids=[]

        for user in self.user_list:

            user_ids.append(user.id)

        newid= max(user_ids)+1

        usnew= User (newid,name )

        self.user_list.append( usnew)

        self.sauvegarder()



    def get_channels(self) -> list[Channels]:

        self.load_server()

        return self.channel_list

    

    def create_channels(self, name:str) -> int:

        self.load_server()

        channel_ids=[]

        for channel in self.channel_list:

            channel_ids.append(channel.id)

        newgroup_id= max(channel_ids)+1

        new = Channels(name,newgroup_id,[])

        self.channel_list.append(new)

        self.sauvegarder()

        return newgroup_id

    

    def join_channel(self,channel_id: int,id_pers: int) -> None:

        self.load_server()

        for channel in self.channel_list:

            if channel.id==channel_id:

                channel.menbers_ids.append(id_pers)

                print("User added")

        self.sauvegarder()



    def get_messages_from_channel_id(self, channel_id: int) -> list[Messages]:

        self.load_server()

        mess_list:list[Messages]=[]

        for message in self.message_list:

            if message.channel==channel_id:

                mess_list.append(message)

        return mess_list



    def get_messages(self) -> list[Messages]:

        self.load_server()

        return self.message_list

    

    def new_message(self, id:int, sender:int, texte:str) -> None:

        self.load_server()

        message_ids=[]

        for message in self.message_list:

            message_ids.append(message.id)

        newid= max(message_ids)+1

        new_message= Messages(id, newid,texte,sender, datetime.now().isoformat())

        self.message_list.append(new_message)

        self.sauvegarder()

        



class RemoteStorage:

    def __init__(self, url:str):

        self.url=url



    def get_users(self) -> list[User]:
        # Maintenant que vous avez stocké l'URL de base dans un attribut
        # self.url, il vaut mieux vous en servir ici.
        response = requests.get(f'{self.url}/users')
        # N'oubliez pas de vérifier le code de retour HTTP,
        # soit avec response.raise_for_status(), soit manuellement
        # avec une vérification de repsonse.status_code
        response.raise_for_status()

        data = json.loads(response.text)

        users: list[User] = []

        for u in data:

            users.append(User(u["id"], u["name"]))

        return users

    

    def create_users(self,name: str) -> None:

        jsonname={'name':name}

        envoi=requests.post(f'{self.url}/users/create', json=jsonname)

        if envoi.status_code==200:

            print("User created")

        else:

            print(envoi.text,envoi.status_code)



    def get_channels(self)->list[Channels]:

        response_gp = requests.get(f'{self.url}/channels')
        response_gp.raise_for_status()

        data = json.loads(response_gp.text)

        channels: list[Channels] = []

        count = 0

        for channel in data:

            menbersid=requests.get(f'{self.url}/channels/{channel["id"]}/members')

            data_members=json.loads(menbersid.text)

            ids_members=[m['id'] for m in data_members]

            channels.append(Channels(channel['name'],channel['id'],ids_members))

            count += 1

            # TB utilisation de '\r'
            print(f"loading {len(data)} groups... ({count}/{len(data)})", end='\r')

        print()

        return channels

    

    def create_channels(self, name: str)-> int:

        jsonname={'name':name}

        send=requests.post(f'{self.url}/channels/create', json=jsonname)
        send.raise_for_status()

        channel_dict=send.json()

        return int(channel_dict['id'])



    def join_channel(self,id:int,menbers_id:int) -> None:

        menbers_id_dict={'user_id': menbers_id}

        envoi=requests.post(f'{self.url}/channels/{id}/join', json=menbers_id_dict)

        if envoi.status_code==200:

            print("User added to the group")

        else:

            print(envoi.text,envoi.status_code)



    def get_messages(self) -> list[Messages]:

        response_mess = requests.get(f'{self.url}/messages')
        response_mess.raise_for_status()

        data = json.loads(response_mess.text)

        messages: list[Messages] = []

        for m in data:

            messages.append(Messages(int(m['channel_id']), int(m['id']), m['content'], int(m['sender_id']), m['reception_date']))

        return messages



    def get_messages_from_channel_id(self, channel_id: int) -> list[Messages]:

        response_mess = requests.get(f'{self.url}/channels/{channel_id}/messages')
        response_mess.raise_for_status()

        data = json.loads(response_mess.text)

        messages: list[Messages] = []

        for m in data:

            messages.append(Messages(int(m['channel_id']), int(m['id']), m['content'], int(m['sender_id']), m['reception_date']))

        return messages



    def new_message(self, id:int, sender:int, texte: str) -> None:

        group_id_dict={'sender_id':sender,"content":texte}

        envoi=requests.post(f'{self.url}/channels/{id}/messages/post', json=group_id_dict)

        if envoi.status_code==200:

            print("message sent")

        else:

            print(envoi.text,envoi.status_code)





class UserInterface:



    def id_name(self,nom: str) -> int | None: #donne l'identifiant à partir du nom
        # Vous utilisez une variable globale (storage), ce qui est
        # souvent source d'erreurs car il est difficile de savoir
        # où elle peut être modifiée dans un gros programme.
        # En règle générale, toutes les variables que vous utilisez
        # dans une méthode doivent :
        # - soit être dans les paramètres de la méthode
        # - soit être définies dans le corps de la méthode
        # Ici, il faudrait donc transformer storage en attribut,
        # donc créer une méthode __init__(self, storage) qui remplirait
        # self.storage. Vous pourriez ensuite aisément utiliser
        # self.storage dans toutes vos méthodes.
        for user in (storage.get_users()):

            if nom==user.name:

                idnom=user.id

                return idnom

    

    def name_id(self,id: int) -> str | None:#donne le nom a parti de l'identifiant

        users = storage.get_users()

        nomid = None

        for user in users:

            if user.id == id:

                nomid=user.name

                return nomid

        

    def menu(self):

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

            self.user()



        elif choice=='2':

            self.channel()

        elif choice=='3':
            # Pensez bien à vérifier si la valeur entrée par l'utilisateur
            # est valide, en vérifiant "if user_id is not None" par exemple.
            user_id=self.id_name(input('Your name?'))

            self.newmessages(user_id)

        else:

            print('Unknown option:', choice)



    def add_menber(self,channel_id: int) -> None:

        for user in storage.get_users():

            print (user.id, user.name)



        nb_pers= int(input('How many users?'))

        # Par convention, si une variable de boucle n'est pas utilisée,
        # on la remplace par le caractère _
        for _ in range (0,nb_pers):

            id_pers=int(input('menber id: ')) 

            storage.join_channel(channel_id,id_pers)





    def user(self):

        for user in storage.get_users():

            print (user.id, user.name) 

        print ('n.Create user')

        print ('x.Main menu')

        choice1 = input('Enter a choice and press ENTER: ')

        if choice1 =='x':

            self.menu()

        if choice1=='n':

            name=input('Name: ')

            storage.create_users(name)



    def newgroup(self):

        groupname= input ('Group Name')

        for user in storage.get_users():

            print (user.id, user.name) 

        id_menbres=[]

        nb_pers= int(input('Combien utilisateurs'))

        for _ in range (0,nb_pers):

            id_pers=int(input('Id du membre')) 

            id_menbres.append(id_pers)

        channel_ids=[]

        for channel in (storage.get_channels()):

            channel_ids.append(channel.id)

        newgroup_id= max(channel_ids)+1

        gpnew=Channels(newgroup_id,groupname,id_menbres)

        storage.get_channels().append (gpnew)

        storage.sauvegarder()

        print(storage.get_channels())



    def newmessages(self,user_id: int):

        channels=storage.get_channels()

        found = False

        for channel in channels:
            if user_id in channel.menbers_ids:
                print('Groups in which you are:')
                print(channel.id, channel.name, channel.menbers_ids)
                found = True

        # TB d'avoir pensé à faire cette vérification
        if not found:
            print("user not found, create new user")
            self.menu()

        gp = int(input('Group id'))

        texte= input('Write a message')

        storage.new_message(gp,user_id,texte)

        print("1.Send another message")

        print("x. Return")

        choicem=input('Enter a choice and press ENTER:' )

        if choicem=='1':

            self.newmessages(user_id)

        elif choicem=='x':

            self.menu()



    def channel(self):

        channels=storage.get_channels()

        for channel in channels:

            print (channel.id, channel.name) 

        

        print("1.Choose group")

        print("2.New group")

        print("x.Menu ")

        choice2 = input('Enter a choice and press ENTER: ')

        if choice2=='1':  

            # Il y a pas mal de conditions et boucles imbriquées
            # ici, et beaucoup de choix utilisateurs. Il vaut
            # mieux créer des fonctions intermédiaires.
            choice22=int(input("Group number: "))

            for channel in channels: #on parcourt les channels si on en un id qui match on sort de la boucle avec break ( on a utilisé un for else) 

                if choice22 == channel.id:

                    print(channel)

                    for ids in channel.menbers_ids: # on transforme l'id en nom

                        name = self.name_id(int(ids))

                        print(name,end=' ')

                    print()

                    messages=storage.get_messages_from_channel_id(choice22)

                    print("Messages du groupe:")

                    # Il vaut mieux trier les messages par
                    # reception_date pour être sure de les afficher
                    # dans le bon ordre
                    for message in messages:
                        # TB d'avoir récupéré le nom
                        name_sender=self.name_id(message.sender_id)
                        # N'oubliez pas d'afficher la reception_date
                        print(f"[{name_sender}]: {message.content}")

                    print("1. Add menbers")

                    print("x. Menu ")

                    choice3 = input('Enter a choice and press ENTER: ')

                    if choice3=='1':

                        self.add_menber(choice22)

                    if choice3=='x':

                        self.menu()



        elif choice2== 'x':

            self.menu()

        elif choice2 == '2':

            name=input('Name: ')

            channel_id=storage.create_channels(name)



            for user in storage.get_users():

                print (user.id, user.name)

            

            nb_pers= int(input('Combien utilisateurs'))

            for i in range (0,nb_pers):

                id_pers=int(input('Id du membre')) 

                storage.join_channel(channel_id,id_pers)











parser = argparse.ArgumentParser(description="programme qui permet d'envoyer des messages d'un ordinateur à l'autre en passent par un serveur")

parser.add_argument('--storage-file', type=str)

parser.add_argument('--url', type=str)



args = parser.parse_args()



if args.storage_file:

    storage = LocalStorage(args.storage_file)

elif args.url:

    storage = RemoteStorage(args.url)

else:

    parser.print_help() 













    



UserInterface().menu()