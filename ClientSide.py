import logging
from getpass import getpass
from argparse import ArgumentParser
from slixmpp import Iq

import slixmpp
#Test3
#1234

class ClientChat(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0066')

    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()
        self.disconnect()


    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(msg['body'])

def second_menu():
    print("""
    1. Delete user
    3. Exit
    """)
    return int(input("Enter your choice: "))

def third_menu():
    print("""
    1. Iniciar sesion
    2. Exit
    """)
    return int(input("Enter your choice: "))