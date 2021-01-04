from math import floor

from parser_classes.iTokenizer import iTokenizer


class NumberTokenizer(iTokenizer):

    def tokenize(self, token) -> list:
        number_content = []
        if ',' in token:  # 10,000
            token = token.replace(',', '')
        if (token.__contains__('.') and token.__contains__('/')) or token.__contains__('-'):  # mikre katza 4.5/6
            return number_content
        if token.__contains__('.'):
            if token.find('.') == 0:
                number_content = ['0' + token]  # .05
            elif int(token[0:token.find('.')]) > 1000:  # 1250.5
                number_content = [self.number_to_magnitude(int(token[0:token.find('.')]))]
            else:
                number_content = [token]  # 14.5
        elif token.__contains__('/'):  # 3/4
            number_content = [token]
        elif int(token) > 1000:  # 1450
            number_content = [self.number_to_magnitude(token)]
        else:  # 50
            number_content = [token]
        return number_content

    def number_to_magnitude(self, num):
        num1 = int(floor(float(num)))
        if len(str(num1)) <= 9:
            magnitude = 0
            while abs(num1) >= 1000:
                magnitude += 1
                num1 /= 1000
            return str(num1) + ['', 'K', 'M', 'B', 'T', 'Q', 'Qu', 'S'][magnitude]
        return str(num)