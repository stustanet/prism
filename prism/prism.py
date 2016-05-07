import traceback
import copy

import sleekxmpp

from sleekxmpp.xmlstream.handler.callback import Callback
from sleekxmpp.xmlstream.matcher.xpath import MatchXPath

from .listener import Listener
from .listener import RespondListener


class Prism():

    def __init__(self, jid, password, nick):
        self._xmpp = sleekxmpp.ClientXMPP(jid, password)

        self.config = None

        self.rooms = []
        self.nicks = [nick]
        self.listener = []
        self.commands_hear = []
        self.commands_respond = []

        self._xmpp.add_event_handler('session_start', self._start)
        self._xmpp.add_event_handler('groupchat_message', self._muc_message)
        self._xmpp.add_event_handler('message', self._message)

        self._xmpp.register_plugin('xep_0030')  # Service Discovery
        self._xmpp.register_plugin('xep_0045')  # Multi-User Chat
        self._xmpp.register_plugin('xep_0199')  # XMPP Ping

        self.respond('help', self.help_command, 'help: list of all commands')

    def get_nick(self):
        return self.nicks[-1]

    def get_joined_rooms(self):
        return self.rooms

    def get_roster(self, room):
        return self._xmpp.plugin['xep_0045'].getRoster(room)

    def join_muc(self, muc):
        self.rooms.append(muc)

    def start(self, endpoint=None):
        self.respond('.*$', self.fallback_command, None)

        if self._xmpp.connect(endpoint):
            self._xmpp.process(block=True)
        else:
            print('Unable to connect')

    def stop(self):
        self._xmpp.disconnect(wait=True)

    def hear(self, regex, func, help_text):
        self.listener.append(Listener(self, regex, func))
        if isinstance(help_text, list):
            self.commands_hear.extend(help_text)
        elif isinstance(help_text, str):
            self.commands_hear.append(help_text)
        elif help_text is not None:
            print('help for', regex, 'should be a string')

    def respond(self, regex, func, help_text):
        self.listener.append(RespondListener(self, regex, func))
        if isinstance(help_text, list):
            self.commands_respond.extend(help_text)
        elif isinstance(help_text, str):
            self.commands_respond.append(help_text)
        elif help_text is not None:
            print('help for', regex, 'should be a string')

    def send_message(self, msg, mto=None):
        recipients = mto
        if recipients is None:
            recipients = self.rooms
        elif not isinstance(recipients, list):
            recipients = [recipients]

        for recipient in recipients:
            mtype = 'groupchat' if recipient in self.rooms else 'chat'
            self._xmpp.send_message(mto=recipient,
                                    mbody=msg,
                                    mtype=mtype)

    def change_subject(self, subject, room=None):
        rooms = [room] if room is not None else self.rooms

        for room in rooms:
            self._xmpp.send_message(mto=room,
                                    mbody='',
                                    msubject=subject,
                                    mtype='groupchat')

    def restart(self):
        self._xmpp.disconnect(wait=True)
        self._xmpp.abort()

    def help_command(self, *args):
        _, msg, _ = args

        commands = sorted(self.commands_respond)

        help_message = 'Commands (usage: %s COMMAND):\n%s' \
                       '\n\nOther stuff:\n%s' % (
                           self.get_nick(),
                           '\n'.join(commands),
                           '\n'.join(self.commands_hear))

        msg.reply(help_message).send()
        return True

    @classmethod
    def fallback_command(cls, *args):
        _, msg, _ = args

        mfrom = msg['from'].resource
        msg.reply('sorry %s, '
                  'but i don\'t know that command :\'(\n' % mfrom).send()
        return True

    def _start(self, _):
        self._xmpp.get_roster()
        self._xmpp.send_presence()

        try:
            xmpp = self._xmpp.plugin['xep_0045'].xmpp
            xmpp.registerHandler(Callback('MUCError', MatchXPath(
                "{%s}presence[@type='error']" % xmpp.default_ns), self._error))
        except Exception as exception:
            print(exception)
            traceback.print_exc()
            raise

        self.join_mucs()

    def join_mucs(self):
        for room in self.rooms:
            self._xmpp.plugin['xep_0045'].joinMUC(room,
                                                  self.get_nick(),
                                                  wait=True)

    def leave_mucs(self):
        for room in self.rooms:
            self._xmpp.plugin['xep_0045'].leaveMUC(room,
                                                   self.get_nick())

    def _message(self, msg):
        if msg['type'] != 'chat':
            return

        msg['body'] = '%s %s' % (self.get_nick(), msg['body'])
        self._muc_message(msg)

    def _muc_message(self, msg):
        try:
            if msg['mucnick'] != self.get_nick():
                for listener in self.listener:
                    copied_msg = copy.copy(msg)
                    if listener.call(copied_msg):
                        break

        except Exception as exception:
            print(exception)
            traceback.print_exc()
            raise

    def _error(self, msg):
        if msg['type'] != 'error':
            return
        if msg['error'] is None:
            return
        if msg['error']['type'] != 'cancel':
            return
        if msg['error']['condition'] != 'conflict':
            return
        try:

            self.leave_mucs()

            self.nicks.append(self.get_nick() + '.')

            self.join_mucs()
        except Exception as exception:
            print(exception)
            traceback.print_exc()
            raise
