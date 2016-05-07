def register_to(bot):

    def subject(bot, msg, match):
        bot.change_subject(match.group(1), msg['from'].bare)

    bot.respond('set subject to (.*)$', subject,
                help_text='set subject to TEXT: sets the subject to TEXT')
