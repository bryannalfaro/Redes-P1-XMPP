#Referencias
#https://stackoverflow.com/questions/58454190/python-async-waiting-for-stdin-input-while-doing-other-stuff

from Authentication import *
from aioconsole import ainput, aprint

'''
TODO
    -Aceptar chat mientras input es ingresado
    -Notificaciones
    -Enviar recibir archivos
    - VCard de usuarios
'''
import slixmpp

'''
Function to display a menu when the user is logged in the chat
ARGS:
    None
'''
async def second_menu():
    print("""
    1. Mostrar usuarios
    2. Agregar usuario a contactos
    3. Mostrar detalles de un contacto
    4. Comunicacion 1 a 1
    5. Grupos
    6. Presencia
    7. Eliminar cuenta
    8. Cerrar Sesion
    """)

    return await ainput("Enter your choice: ")

'''
Class to handle the client side of the chat

ARGS:
    jid: username of the user
    password: password of the user
'''
class ClientChat(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.jid, password = jid, password
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0065')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0231')
        self.register_plugin('xep_0071')
        self.register_plugin('xep_0363')
        self.register_plugin('xep_0059')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0085')
        self.register_plugin('xep_0054')
        self.add_event_handler('chatstate_active', self.chat_state_active)
        self.add_event_handler('changed_status', self.chat_changed)
        self.add_event_handler('chatstate_gone', self.chat_state_gone)
        self.add_event_handler('chatstate_composing', self.chat_composing)
        self.add_event_handler('chatstate_paused', self.chat_paused)

        self.user_chat = None
        self.FLAG_AUTH = False
        self.received_message = False
        self.TERMINATE_USER = 0
        self.groups_deleted = []
        self.validate_group_presence = False

    '''
    Function to manage the session

    ARGS:
        event: event that is triggered when the session starts
    '''
    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()

        self.FLAG_AUTH = True

        while self.TERMINATE_USER != 1:
            await self.get_roster()
            option = await second_menu()
            try:
                option = int(option)
            except ValueError:
                print("Por favor, elige un numero")
                continue
            if option not in [1,2,3,4,5,6,7,8]:
                print("No existe esa opcion")
                await self.get_roster()

            if option == 1:
                await self.get_roster()
                await self.mostrar_usuarios(1)

            if option ==2:
                print("Ingrese usuario a agregar")
                user = input()
                user = user+"@alumchat.fun"
                self.send_presence_subscription(user)
                await self.get_roster()
                print("Usuario agregado")

            if option == 3:
                await self.get_roster()
                await self.mostrar_usuarios(2)

            if option == 4:
                print("Ingresa el usuario a comunicar")
                user = input()
                user = user+"@alumchat.fun"
                self.user_chat = user
                await self.comunicacion_1_1(user,'personal_chat')

            if option == 5:
                print("1. Entrar a un grupo")
                print("2. Salir de un grupo")
                menu_group = input()
                try:
                    menu_group = int(menu_group)
                except ValueError:
                    print("Por favor, elige un numero")
                    continue
                if menu_group not in [1,2]:
                    print("No existe esa opcion")
                    await self.get_roster()

                if menu_group == 1:
                    result = await self['xep_0030'].get_items(jid='conference.alumchat.fun')
                    for room in result['disco_items']:
                        print ("Found room: %s, jid is %s" % (room['name'], room['jid']))

                    print("\nIngresa el jid del grupo: ")
                    self.group = await ainput()
                    self.group = self.group+"@conference.alumchat.fun"
                    self.add_event_handler("muc::%s::got_online" % self.group, self.muc_online)
                    self.add_event_handler("muc::%s::got_offline" % self.group, self.muc_offline)
                    print("Ingresa tu nickname: ")
                    self.nickname = await ainput()

                    self.plugin['xep_0045'].join_muc(self.group,self.nickname)
                    if self.groups_deleted != []:
                        if self.group in self.groups_deleted:
                            self.groups_deleted.remove(self.group)
                    await self.comunicacion_1_1(self.group,'group_chat')
                    await self.get_roster()

                if menu_group == 2:
                    self.show_my_groups()
                    if self.validate_group_presence == False:
                        print("No tienes grupos")
                    else:
                        print("Ingresa el jid del grupo: ")
                        self.group = await ainput()
                        self.group = self.group+"@conference.alumchat.fun"
                        user = self.jid +"@alumchat.fun"

                        self.plugin['xep_0045'].leave_muc(self.group,user)
                        self.groups_deleted.append(self.group)
                        self.validate_group_presence = False
                        await self.get_roster()

            if option ==6:
                print("Ingresa tu mensaje: ")
                mensaje = input(">> ")
                self.send_presence(pshow='Available', pstatus=mensaje)
                await self.get_roster()

            if option == 7:
                self.TERMINATE_USER = 2
                self.disconnect()

            elif option == 8:

                self.TERMINATE_USER = 1
                self.disconnect()


    '''
    Function to manage the 1 to 1 comunnication and group chat comunnication
    ARGS:
        user: user to communicate with
        type: type of chat (individual or group)

    '''
    async def comunicacion_1_1(self,user,type):

        close_chat = True
        while close_chat:

            if type == 'personal_chat':
                print("e para salir\n")
                m = self.Message()
                m['to'] = user
                m['type'] = 'chat'
                m['chat_state'] = 'composing'
                m.send()
                mensaje = await ainput(">> ")
                m = self.Message()
                m['to'] = user
                m['type'] = 'chat'
                m['chat_state'] = 'paused'
                m.send()
                if mensaje == "e":
                    m = self.Message()
                    m['to'] = user
                    m['type'] = 'chat'
                    m['chat_state'] = 'gone'
                    m.send()
                    close_chat = False
                elif mensaje=="file":
                    print("Ingresa el nombre del archivo")
                    filename = input()
                    url = await self.plugin['xep_0363'].upload_file(filename,domain='alumchat.fun')
                    await self.get_roster()
                    print(url)
                    m = self.Message()
                    m['to'] = user
                    m['type'] = 'chat'
                    m['body'] = 'Tried sending an image using OOB'
                    m['oob']['url'] = url
                    m.send()
                    await self.get_roster()
                else:

                    self.send_message(mto=user, mbody=mensaje, mtype='chat')
                    m = self.Message()
                    m['to'] = user
                    m['type'] = 'chat'
                    m['chat_state'] = 'active'
                    m.send()
                    await self.get_roster()
            if type == 'group_chat':
                print("e para salir\n")
                mensaje = await ainput(">> ")
                if mensaje == "e":
                    close_chat = False
                elif mensaje=="file":
                    print("Ingresa el nombre del archivo")
                    filename = input()
                    url = await self.plugin['xep_0363'].upload_file(filename,domain='alumchat.fun')
                    await self.get_roster()
                    print(url)
                    m = self.Message()
                    m['to'] = self.group
                    m['type'] = 'groupchat'
                    m['body'] = 'Tried sending an image using OOB'
                    m['oob']['url'] = url
                    m.send()
                    await self.get_roster()
                else:
                    self.send_message(mto=user, mbody=mensaje, mtype='groupchat')

                    await self.get_roster()
    '''
    Function to show the groups of the user in the chat session
    ARGS:
        None
    '''
    def show_my_groups(self):
        print("---------Lista de Grupos---------\n")
        list_users = self.client_roster.groups()
        for user in list_users:
            for username in list_users[user]:
                if str(username).find("@conference.alumchat.fun")!=-1 and str(username) not in self.groups_deleted:
                    self.validate_group_presence= True
                    if username != self.jid:
                        print("Grupo: " + username)
                        get_presence = self.client_roster.presence(username)
                        for res, pres in get_presence.items():
                            print("Estado: " + pres['show'])
                            print("Mensaje: " + pres['status'])
                            print("\n")

    '''
    Function to show the contact list of the user including individual contacts and groups
    and details of a contact depending of the selection
    ARGS:
        selection: option to select display all list or details of a contact
    '''
    async def mostrar_usuarios(self,selection):
        if selection == 1:
            print("---------Lista de usuarios---------\n")
            list_users = self.client_roster.groups()
            for user in list_users:
                print(user)
                for username in list_users[user]:
                    if str(username).find("@conference.alumchat.fun")!=-1:
                        self.show_my_groups()
                    else:
                        if username != self.jid:
                            print("Usuario: " + username)
                            get_presence = self.client_roster.presence(username)
                            for res, pres in get_presence.items():
                                print("Estado: " + pres['show'])
                                print("Mensaje: " + pres['status'])
                                print("\n")

        if selection == 2:
            list_users = self.client_roster.groups()

            print("---------Informacion de contacto---------\n")
            print("Ingresa el usuario a consultar")
            user = input()
            user = user+"@alumchat.fun"
            #vcard = await self.plugin['xep_0054'].get_vcard(user)
            #print(vcard)
            try:
                for username in list_users:
                    if user in list_users[username]:
                        j = self.client_roster.presence(user)
                for res, pres in j.items():
                    print("Estado: " + pres['show'])
                    print("Mensaje: " + pres['status'])
                    print("\n")
            except:
                print("Usuario no encontrado")

    '''
    Function to handle the connection in group chat
    ARGS:
        presence: presence stanza
    '''
    def muc_online(self, presence):
        if presence['muc']['nick'] != self.nickname:
            print(presence['muc']['nick'] + " esta conectado")


    '''
    Function to handle the disconnection in group chat
    ARGS:
        presence: presence stanza
    '''
    def muc_offline(self, presence):
        if presence['muc']['nick'] != self.nickname:
            print(presence['muc']['nick'] + " esta desconectado")

    '''
    Function to receive a message from a personal or group chat
    ARGS:
        msg: xml with the message
    '''
    def message(self,msg):

        self.received_message = True
        if msg['type'] in ('chat', 'normal'):
            print("*************Mensaje personal***********************")
            print(msg["from"].bare.split("@")[0],":",msg['body'])
            print("****************************************************\n")
        elif msg['type'] == 'groupchat':

                if str(msg['from']).split('/')[1]!=self.nickname:

                    print("*************Mensaje en grupo: ", msg["from"].bare.split("@")[0],"********************")
                    print(msg['mucnick'],":",msg['body'])
                    print("*******************************************************************\n")

    '''
    Function to handle the composition of a message
    ARGS:
        msg: xml with the message
    '''
    def chat_composing(self,msg):
        if self.user_chat != None:
            print("Composing...")

    '''
    Function to handle the gone state of a chat
    ARGS:
        msg: xml with the message
    '''
    def chat_state_gone(self,msg):
        if self.user_chat != None:
            print(msg["from"].bare.split("@")[0],": salio del chat")

    '''
    Function to handle the paused state of a chat
    ARGS:
        msg: xml with the message
    '''
    def chat_paused(self,msg):
        if self.user_chat != None:
            print("Paused...")

    '''
    Function to handle a change in an user's status
    ARGS:
        event: xml with the event
    '''
    def chat_changed(self,event):
        print(event["from"].bare.split("@")[0],": cambio de estado\n")

    '''
    Function to handle the active presence in a chat
    ARGS:
        msg: xml with the message
    '''
    def chat_state_active(self,msg):
        if self.user_chat != None:
            print("Esta activo en el chat")