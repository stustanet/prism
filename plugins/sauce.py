def register(bot):
    def sauce(bot, msg, _):
        bot.send_message(
            "https://gitlab.stusta.mhn.de/stustanet/prism/", msg['from'].bare)

    bot.respond('gimme-sauce', sauce)
    bot.respond('invoke-gpl', sauce)
    bot.respond('mitm', sauce)
