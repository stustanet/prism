import re

class Listener:
    def __init__(self, bot, regex, callback):
        self.bot = bot
        self.regex = re.compile(regex)
        self.callback = callback


    def call(self, msg):
        match = self.regex.match(msg['body'])

        if match is not None:
            self.callback(self.bot, msg, match)



class RespondListener(Listener):
    def call(self, msg):
        newRegex = self.regex.pattern
        flags = self.regex.flags

        nicks = '(?:%s)' % '|'.join([re.escape(nick) for nick in self.bot.nicks])

        newRegex = '(?:/|%s |@%s |%s: )%s'%(nicks, nicks, nicks, self.regex.pattern)

        newRegex = re.compile(newRegex, flags)

        match = newRegex.match(msg['body'])

        if match is not None:
            self.callback(self.bot, msg, match)
