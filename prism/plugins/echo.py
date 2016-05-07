def register_to(bot):

    def respond_echo(_, msg, match):
        reply = msg.reply(match.group(1))
        reply.send()

        return True

    bot.respond('echo (.*)$', respond_echo,
                help_text='echo TEXT: posts TEXT')

    def respond_broadcast(bot, msg, match):
        message = '%s (by %s)' % (match.group(1), msg['from'])
        mto = None if msg['type'] == 'groupchat' else bot.rooms + [str(msg['from'])]
        bot.send_message(message, mto)

        return True

    bot.respond('broadcast (.*)$', respond_broadcast,
                help_text='broadcast TEXT: posts TEXT in all channels')

    def respond_all(bot, _, match):
        for room in bot.get_joined_rooms():
            roster = [nick for nick in bot.get_roster(room)
                      if nick not in bot.nicks]

            message = '%s: %s' % (', '.join(roster), match.group(1))

            bot.send_message(message, room)

        return True

    bot.respond('all (.*)$', respond_all,
                help_text='all TEXT: highlights all people and posts TEXT')
