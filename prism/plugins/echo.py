def register_to(bot):

    def echo(bot, msg, match):
        bot.send_message(match.group(1), msg['from'].bare)

    bot.respond('echo (.*)$', echo,
                help='echo TEXT: posts TEXT')

    def broadcast(bot, _, match):
        bot.send_message(match.group(1))

    bot.respond('broadcast (.*)$', broadcast,
                help='broadcast TEXT: posts TEXT in all channels')

    def all(bot, _, match):
        for room in bot.get_joined_rooms():
            roster = [nick for nick in bot.get_roster(room)
                      if nick not in bot.nicks]

            message = '%s: %s' % (', '.join(roster), match.group(1))

            bot.send_message(message, room)

    bot.respond('all (.*)$', all,
                help='all TEXT: highlights all people and posts TEXT')
