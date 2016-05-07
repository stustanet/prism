def register_to(bot):

    def counter(*args):
        _, msg, _ = args
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
        smileys = [':(', ':\'(', ':-(', '<3', '+o(', ':\'-(', ';(', ';-(',
                   '>.<', ':<', ':-<', '(:']
        result = []

        message = msg['body']
        for smiley in smileys:
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
            msg.reply(''.join(result)).send()

        return False

    bot.hear('^(.*)$', counter,
             help_text='closes matching brackets')
