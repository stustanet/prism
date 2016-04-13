
def register(bot):
    def echo(bot, msg, match):
        bot.send_message(match.group(1), msg['from'].bare)

    bot.respond('echo (.*)$', echo)

    def broadcast(bot, msg, match):
        bot.send_message(match.group(1))

    bot.respond('broadcast (.*)$', broadcast)
