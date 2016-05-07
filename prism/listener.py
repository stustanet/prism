import re


class Listener:

    def __init__(self, bot, regex, callback):
        self.bot = bot
        self.regex = re.compile(regex)
        self.callback = callback

    def call(self, msg):
        match = self.regex.match(msg['body'])

        if match is not None:
            return self.callback(self.bot, msg, match)

        return False


class RespondListener(Listener):

    def call(self, msg):
        new_regex = self.regex.pattern
        flags = self.regex.flags

        nicks = '(?:%s)' % '|'.join([re.escape(nick)
                                     for nick in self.bot.nicks])

        new_regex = '(?:/|%s |@%s |%s: )%s' % (nicks, nicks, nicks,
                                               self.regex.pattern)

        new_regex = re.compile(new_regex, flags)

        match = new_regex.match(msg['body'])
        if match is not None:
            return self.callback(self.bot, msg, match)

        return False
