def register(bot):
    def counter(bot, msg, match):
        brackets = [ ('(',')'), ('[',']'), ('{','}'), ('<','>') ]
        result = ''

        for (start, end) in brackets:
            start_count = msg['body'].count(start)
            end_count = msg['body'].count(end)

            if start_count > end_count:
                result += end * (start_count - end_count)

        if len(result) > 0:
            bot.send_message(result, msg['from'].bare)

    bot.hear('^(.*)$', counter)
