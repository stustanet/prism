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
