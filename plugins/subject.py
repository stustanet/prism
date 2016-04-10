
def register(bot):
    def subject(bot, msg, match):
        bot.change_subject(match.group(1), msg['from'].bare)

    bot.respond('set subject to (.*)$', subject)
