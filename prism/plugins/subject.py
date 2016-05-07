def register_to(bot):

    def subject(bot, msg, match):
        if msg['type'] == 'chat':
            msg.reply('sorry! i can only change the subject for mucs!').send()
            return True
        bot.change_subject(match.group(1), msg['from'].bare)

        return True

    bot.respond('set subject to (.*)$', subject,
                help_text='set subject to TEXT: sets the subject to TEXT')
