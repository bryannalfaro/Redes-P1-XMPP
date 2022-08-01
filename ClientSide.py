#Referencias
#https://stackoverflow.com/questions/58454190/python-async-waiting-for-stdin-input-while-doing-other-stuff
from time import sleep
import logging
from getpass import getpass
from argparse import ArgumentParser
from slixmpp import Iq
from Authentication import *
from threading import Thread
from aioconsole import ainput

'''
TODO
    -Aceptar chat mientras input es ingresado
    -Notificaciones
    -Enviar recibir archivos
    -Grupos
'''
import slixmpp

def second_menu():
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

    return input("Enter your choice: ")

class ClientChat(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.jid, password = jid, password
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0066')
        self.FLAG_AUTH = False
        self.received_message = False
        self.TERMINATE_USER = 0

    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()
        self.FLAG_AUTH = True
        while self.TERMINATE_USER != 1:
            await self.get_roster()
            option = second_menu()
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
                self.mostrar_usuarios(1)
            if option == 3:
                await self.get_roster()
                self.mostrar_usuarios(2)
            if option == 4:
                print("Ingresa el usuario a comunicar")
                user = input()
                user = user+"@alumchat.fun"
                await self.comunicacion_1_1(user)

            if option ==2:
                print("Ingrese usuario a agregar")
                user = input()
                user = user+"@alumchat.fun"
                self.send_presence_subscription(user)
                await self.get_roster()
                print("Usuario agregado")
            if option ==6:
                print("Ingresa tu estado: Available , Busy, Away,  Not available, Offline")
                estado = (input(">> "))
                print("Ingresa tu mensaje: ")
                mensaje = input(">> ")
                self.send_presence(pshow=estado, pstatus=mensaje)
                await self.get_roster()

            if option == 7:
                self.TERMINATE_USER = 2
                self.disconnect()
            elif option == 8:

                self.TERMINATE_USER = 1

                self.disconnect()

    async def comunicacion_1_1(self,user):
        close_chat = True
        while close_chat:

            print("e para salir\n")
            mensaje = await ainput(">> ")
            if mensaje == "e":
                close_chat = False
            else:
                self.send_message(mto=user, mbody=mensaje, mtype='chat')
                await self.get_roster()



    def mostrar_usuarios(self,selection):
        if selection == 1:
            print("---------Lista de usuarios---------\n")
            list_users = self.client_roster.groups()
            for user in list_users:
                for username in list_users[user]:
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



    def message(self,msg):

        self.received_message = True
        print(msg['from'],":",msg['body'])

def third_menu():
    print("""
    1. Iniciar sesion
    2. Exit
    """)
    return int(input("Enter your choice: "))