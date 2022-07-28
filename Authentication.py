import logging
from getpass import getpass
from argparse import ArgumentParser
from slixmpp import Iq

import slixmpp

class RegisterChat(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("register", self.registration_user)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0077')

    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()
        self.disconnect()


    async def registration_user(self, iq):
        event = self.Iq()
        event['type'] = 'set'
        event['register']['username'] = self.boundjid.user
        event['register']['password'] = self.password
        try:
            await event.send()
            logging.info("User registered")
        except slixmpp.exceptions.IqError as e:
            logging.error("Could not register: %s", e.iq['error']['text'])
            self.disconnect()
        except slixmpp.exceptions.IqTimeout:
            logging.error("No response from server.")
            self.disconnect()



class DeleteUsersChat(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("register", self.delete_user)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0077')

    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.delete_user()
        self.disconnect()

    async def delete_user(self):
        event = self.Iq()
        event['type'] = 'set'
        event['from'] = self.boundjid.user
        event['register']['remove'] = True
        try:
            await event.send()
            logging.info("User deleted")
        except slixmpp.exceptions.IqError as e:
            logging.error("Could not delete: %s" % e.iq['error']['text'])
            self.disconnect()
        except slixmpp.exceptions.IqTimeout:
            logging.error("No response from server.")
            self.disconnect()