def register_to(bot):

    def sauce(bot, msg, _):
        bot.send_message(
            "https://gitlab.stusta.mhn.de/stustanet/prism/", msg['from'].bare)

    bot.respond('gimme-sauce', sauce,
                help_text='gimme-sauce: posts the url of the source')
    bot.respond('invoke-gpl', sauce, help_text=None)
    bot.respond('mitm', sauce, help_text=None)
