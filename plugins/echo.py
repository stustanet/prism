def register(bot):
    def echo(bot, msg, match):
        bot.send_message(match.group(1), msg['from'].bare)

    bot.respond('echo (.*)$', echo,
                help='echo TEXT: posts TEXT')

    def broadcast(bot, _, match):
        bot.send_message(match.group(1))

    bot.respond('broadcast (.*)$', broadcast,
                help='broadcast TEXT: posts TEXT in all channels')
