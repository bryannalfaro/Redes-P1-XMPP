import logging
from getpass import getpass
from argparse import ArgumentParser
from slixmpp import Iq
from Authentication import *

import slixmpp
#Test3
#1234


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
    return int(input("Enter your choice: "))



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
        self.TERMINATE_USER = 0
        print("Sesion iniciada con exitdso")
    async def session_start(self, event):
        print("Sesion iniciada con exitod")
        self.send_presence()
        await self.get_roster()
        self.FLAG_AUTH = True
        print("Sesion iniciada con exito")
        while self.TERMINATE_USER != 1:
            option = second_menu()
            if option ==6:
                print("Ingresa tu estado: Available , Busy, Away,  Not available, Offline")
                estado = (input(">> "))
                print("Ingresa tu mensaje: ")
                mensaje = input(">> ")
                self.send_presence(estado, mensaje)
                await self.get_roster()

            if option == 7:
                self.TERMINATE_USER = 2
                self.disconnect()
            elif option == 8:

                self.TERMINATE_USER = 1

                self.disconnect()


    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(msg['body'])





def third_menu():
    print("""
    1. Iniciar sesion
    2. Exit
    """)
    return int(input("Enter your choice: "))