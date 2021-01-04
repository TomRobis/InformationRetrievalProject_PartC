from re import search

from parser_classes.NumberTokenizer import NumberTokenizer
from parser_classes.SuffixTokenizer import SuffixTokenizer
from parser_classes.SymbolTokenizer import SymbolTokenizer
from parser_classes.URLTokenizer import URLTokenizer
from parser_classes.new_parser_v2_adjustments.NonTokenizingTokenizer import NonTokenizingTokenizer
from parser_classes.new_parser_v2_adjustments.RegularTokenizer import RegularTokenizer


class TokenizerFactory:

    def __init__(self) -> None:
        self.string_to_tokenizer = self.init_tokenizer_dict()
        self.symbols = {"percentage", "percent", "%", '$'}.union(
            {'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion',
             'Quintillion', 'Sextillion',
             'thousand', 'million', 'billion', 'trillion', 'quadrillion',
             'quintillion', 'sextillion'
             })


    '''
    important to note here that if we pass all conditions, we receive a token we don't wish to parse.  
    therefore, we have the original "interface" which does not implement tokenize, throwing away the token.
    '''
    def get_tokenizer(self,token,next_token):
        if self.is_symbol(token, next_token):
            tokenizer_identifier = 'symbol'
        elif self.has_special_suffix(token,next_token):
            tokenizer_identifier = 'suffix'
        elif self.is_number(token):
            tokenizer_identifier = 'number'
        elif next_token == 'URL':  # URL tokenizer, no need for a specific condition check
            tokenizer_identifier = 'URL'
        elif self.is_valid_token(token):
            tokenizer_identifier = 'regular'
        else:
            tokenizer_identifier = 'none'
        return self.string_to_tokenizer[tokenizer_identifier]


    def is_symbol(self, token, next_token):
        return token in ["#", '@'] or (
                next_token in self.symbols and self.is_number(token))

    def init_tokenizer_dict(self):
        tokenizers_dict = dict()
        tokenizers_dict['symbol'] = SymbolTokenizer()
        tokenizers_dict['number'] = NumberTokenizer()
        tokenizers_dict['suffix'] = SuffixTokenizer()
        tokenizers_dict['regular'] = RegularTokenizer()
        tokenizers_dict['URL'] = URLTokenizer()
        tokenizers_dict['none'] = NonTokenizingTokenizer()
        return tokenizers_dict

    def has_special_suffix(self, last_token, token):
        return last_token.endswith("st" or "th" or "nd" or "rd") and self.is_number(
            last_token[0:-2]) and token.isalpha()

    def is_valid_token(self, token):
        return len(token) > 1 and search("[A-Z a-z 0-9]", token)

    def is_invalid_token(self, token):
        return token in self.useless_token_list


    def is_number(self, num):
        return search("[0-9]", num) and (False if any(ord(c) > 57 or ord(c) < 44 for c in num) else True) and \
               num.count('.') < 2 and num.count('/') < 2