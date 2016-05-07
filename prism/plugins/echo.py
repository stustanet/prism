def register_to(bot):

    def respond_echo(bot, msg, match):
        bot.send_message(match.group(1), msg['from'].bare)

    bot.respond('echo (.*)$', respond_echo,
                help_text='echo TEXT: posts TEXT')

    def respond_broadcast(bot, _, match):
        bot.send_message(match.group(1))

    bot.respond('broadcast (.*)$', respond_broadcast,
                help_text='broadcast TEXT: posts TEXT in all channels')

    def respond_all(bot, _, match):
        for room in bot.get_joined_rooms():
            roster = [nick for nick in bot.get_roster(room)
                      if nick not in bot.nicks]

            message = '%s: %s' % (', '.join(roster), match.group(1))

            bot.send_message(message, room)

    bot.respond('all (.*)$', respond_all,
                help_text='all TEXT: highlights all people and posts TEXT')
