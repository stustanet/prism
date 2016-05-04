def register_to(bot):

    def counter(bot, msg, _):
        brackets = {
            '(': ')', '[': ']', '{': '}', '<': '>',
            '„': '“',
            '“': '”', '‘': '’', '‹': '›', '«': '»',
            '（': '）', '［': '］', '｛': '｝', '｟': '｠',
            '⦅': '⦆', '〚': '〛', '⦃': '⦄',
            '「': '」', '〈': '〉', '《': '》', '【': '】', '〔': '〕', '⦗': '⦘',
            '『': '』', '〖': '〗', '〘': '〙',
            '⟦': '⟧', '⟨': '⟩', '⟪': '⟫', '⟮': '⟯', '⟬': '⟭', '⌈': '⌉',
            '⌊': '⌋', '⦇': '⦈', '⦉': '⦊',
            '❛': '❜', '❝': '❞', '❨': '❩', '❪': '❫', '❴': '❵', '❬': '❭',
            '❮': '❯', '❰': '❱',
            '❲': '❳', '﴾': '﴿',
            '〈': '〉', '⦑': '⦒', '⧼': '⧽',
            '﹙': '﹚', '﹛': '﹜', '﹝': '﹞',
            '⁽': '⁾', '₍': '₎',
            '⦋': '⦌', '⦍': '⦎', '⦏': '⦐', '⁅': '⁆',
            '⸢': '⸣', '⸤': '⸥',
        }
        smilies = [ ':(', ':\'(', ':-(', '<3', '+o(', ':\'-(', ';(', ';-(' ]
        result = []

        message = msg['body']
        for smiley in smilies:
            message = message.replace(smiley, '')

        for character in message:
            char = brackets.get(character)
            if len(result) > 0:
                if character == result[-1]:
                    result.pop()
                    continue
            if char is not None:
                result.append(char)

        if len(result) > 0:
            result.reverse()
            bot.send_message(''.join(result), msg['from'].bare)

    bot.hear('^(.*)$', counter,
             help='closes matching brackets')
