
from re import findall

from parser_classes.new_parser_v2_adjustments.NonTokenizingTokenizer import NonTokenizingTokenizer


class SymbolTokenizer(NonTokenizingTokenizer):


    def __init__(self):
        self.magnitude_dict = {'Thousand': 'K', 'Million': 'M', 'Billion': 'B', 'Trillion': 'T', 'Quadrillion': 'Q',
                          'Quintillion': 'Qu', 'Sextillion': 'S',
                          'thousand': 'K', 'million': 'M', 'billion': 'B', 'trillion': 'T', 'quadrillion': 'Q',
                          'quintillion': 'Qu', 'sextillion': 'S'
                          }
        super.__init__(True)

    def tokenize(self,token,next_token) -> list:
        if next_token in ['percent','percentage','percentile']:
           next_token = '%'
        if next_token in ['$', '%'] or token == '@':
            token = [token + next_token]
        elif token == '#':
            token = [w.lower() for w in findall('[A-Z]?[a-z]+', next_token)]
            token.append("#" + next_token.lower().replace('_', ''))
        elif next_token in self.magnitude_dict.keys():
            token = [token + self.magnitude_dict[next_token]]
        else:
            raise ValueError(
                'wrong symbols got to SymbolTokenizer\nToken: ' + token + '\nNext Token: ' + next_token)
        return token

