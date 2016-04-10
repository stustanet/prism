import sleekxmpp
import re
import traceback

import threading
import signal

from os import listdir
from os.path import isfile, join
import importlib

from listener import Listener

class Prism():
    def __init__(self, jid, password, nick):
        self._xmpp = sleekxmpp.ClientXMPP(jid, password)

        self.config = None

        self.rooms = []
        self.nick = nick
        self.listener = []

        self._xmpp.add_event_handler('session_start', self._start)
        self._xmpp.add_event_handler('groupchat_message', self._muc_message)

        self._xmpp.register_plugin('xep_0030') # Service Discovery
        self._xmpp.register_plugin('xep_0045') # Multi-User Chat
        self._xmpp.register_plugin('xep_0199') # XMPP Ping


    def join_muc(self, muc):
        self.rooms.append(muc)


    def start(self, endpoint = None):
        if self._xmpp.connect(endpoint):
            self._xmpp.process(block=True)
        else:
            print('Unable to connect')


    def stop(self):
        self._xmpp.disconnect(wait=True)


    def hear(self, regex, func):
        self.listener.append(Listener(self, regex, func))


    def respond(self, regex, func):
        newRegex = re.compile('')
        flags = re.UNICODE

        if isinstance(regex, str):
            newRegex = regex
        elif isinstance(regex, newRegex):
            newRegex = regex.pattern
            flags = regex.flags
        else:
            raise TypeError('regex must be either str or regex')

        newRegex = '(?:/|%s |@%s |%s: )%s'%(self.nick, self.nick, self.nick, regex)

        newRegex = re.compile(newRegex, flags)

        self.hear(newRegex, func)


    def send_message(self, msg, room=None):
        rooms = [room] if room is not None else self.rooms

        for room in rooms:
            self._xmpp.send_message(mto=room,
                                    mbody=msg,
                                    mtype='groupchat')


    def change_subject(self, subject, room=None):
        rooms = [room] if room is not None else self.rooms

        for room in rooms:
           self._xmpp.send_message(mto=room,
                                   mbody='',
                                   msubject=subject,
                                   mtype='groupchat')


    def _start(self, event):
        self._xmpp.get_roster()
        self._xmpp.send_presence()

        for room in self.rooms:
            self._xmpp.plugin['xep_0045'].joinMUC(room,
                                                  self.nick,
                                                  wait=True)


    def _muc_message(self, msg):
        try:
            if msg['mucnick'] != self.nick:
                for listener in self.listener:
                    listener.call(msg)

        except Exception as e:
            print(e)
            traceback.print_exc()
            raise



if __name__ == "__main__":

    import config

    prism = Prism(config.JID, config.PASSWORD, config.NICK)
    for room in config.ROOMS:
        prism.join_muc(room)

    prism.config = config

    # loading plugins

    plugin_path = './plugins'
    python_matcher = re.compile('([^\.]+)\.py', re.I)
    plugin_files = [python_matcher.match(f).group(1)
                        for f in listdir(plugin_path)
                            if isfile(join(plugin_path, f))
                                and python_matcher.match(f)]

    for plugin in plugin_files:
        module = importlib.import_module('plugins.%s' % plugin)
        module.register(prism)

    # starting

    # def start_prism():
    prism.start((config.HOST, config.PORT))


    # t = threading.Thread(target=start_prism)
    # t.start()


    pass
