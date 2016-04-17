def register(bot):
    def sauce(bot, msg, _):
        bot.send_message(
            "https://gitlab.stusta.mhn.de/stustanet/prism/", msg['from'].bare)

    bot.respond('gimme-sauce', sauce,
                help='gimme-sauce: posts the url of the source')
    bot.respond('invoke-gpl', sauce, help=None)
    bot.respond('mitm', sauce, help=None)
