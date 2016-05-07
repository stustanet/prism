def register_to(bot):

    def sauce(*args):
        _, msg, _ = args
        msg.reply('https://gitlab.stusta.mhn.de/stustanet/prism/').send()

        return True

    bot.respond('gimme-sauce', sauce,
                help_text='gimme-sauce: posts the url of the source')
    bot.respond('invoke-gpl', sauce, help_text=None)
    bot.respond('mitm', sauce, help_text=None)
