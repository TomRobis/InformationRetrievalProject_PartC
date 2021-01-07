import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from parser_classes.tokenizers.EntityTokenizer import EntityTokenizer
from parser_classes.tokenizers.NumberTokenizer import NumberTokenizer
from parser_classes.tokenizers.SuffixTokenizer import SuffixTokenizer
from parser_classes.tokenizers.SymbolTokenizer import SymbolTokenizer
from parser_classes.tokenizers.URLTokenizer import URLTokenizer

from stemmer import Stemmer
from document import Document
from re import search


class Parse:

    def __init__(self, stemming=True):
        self.stop_words = stopwords.words('english')
        self.stemming = stemming
        self.stem = Stemmer()

        self.string_to_tokenizer = self.init_tokenizer_dict()
        self.symbols = {"percentage", "percent", "%", '$'}.union(
            {'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion',
             'Quintillion', 'Sextillion',
             'thousand', 'million', 'billion', 'trillion', 'quadrillion',
             'quintillion', 'sextillion'
             })
        self.useless_token_list = ['t.co', 'https', 'RT']

    '''
    based on Factory Design Pattern, but because tokenizers have different behavior, can't make a single indetical call
    for every tokenizer; therefore, making an actual factory is obsolete.
    this way, we let the information expert,parser, decide which tokenize to invoke and whether to advance the index.    
    '''

    def parse_sentence(self, text):
        parsed_tokens = []
        text_tokens = word_tokenize(text)
        i = 0
        while i in range(len(text_tokens)):
            token = text_tokens[i]
            if token not in self.useless_token_list:  # todo might add emojies later
                if i < len(text_tokens) - 1 and self.is_symbol(token, text_tokens[i + 1]):
                    parsed_tokens += self.string_to_tokenizer['symbol'].tokenize(token, text_tokens[i + 1])
                    i += 1  # next token is not necessary anymore
                elif i < len(text_tokens) - 1 and self.has_special_suffix(token, text_tokens[i + 1]):
                    parsed_tokens += self.string_to_tokenizer['suffix'].tokenize(token, text_tokens[i + 1])
                    i += 1  # next token is not necessary anymore
                elif i < len(text_tokens) - 1 and self.is_entity(token, text_tokens[i + 1]):
                    parsed_tokens += self.string_to_tokenizer['entity'].tokenize(token, text_tokens[i + 1])
                    i += 1  # next token is not necessary anymore
                elif self.is_number(token):
                    parsed_tokens += self.string_to_tokenizer['number'].tokenize(token)
                elif self.is_valid_token(token):
                    parsed_tokens += [token]
            i += 1
        return [p_t for p_t in parsed_tokens if not self.is_invalid_token(p_t)]

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        # tweet_date = doc_as_list[1] #todo updated in part c
        full_text = doc_as_list[2]
        urls = doc_as_list[3]
        quoted_text = doc_as_list[8]
        quoted_urls = doc_as_list[9]

        urls_tokens = ''

        # quoted text should be parsed as well
        if quoted_text:
            full_text += ' ' + quoted_text

        # If either full URL exists, parse separately for terms.
        urls_tokens += ''.join(self.string_to_tokenizer['URL'].tokenize(urls))
        urls_tokens += ''.join(self.string_to_tokenizer['URL'].tokenize(quoted_urls))
        full_text += urls_tokens

        tokenized_text = self.parse_sentence(full_text)

        #  stemming added according to user request.
        if self.stemming:
            tokenized_text = self.stem.porter_stemmer(tokenized_text)
        term_dict = self.create_term_doc_dict(tokenized_text)

        document = Document(tweet_id, tokenized_text, term_dict)  # todo updated in part c

        return document

    def is_number(self, num):
        return search("[0-9]", num) and (False if any(ord(c) > 57 or ord(c) < 44 for c in num) else True) and \
               num.count('.') < 2 and num.count('/') < 2

    def create_term_doc_dict(self, tokenized_text):
        term_dict = dict()
        for term in tokenized_text:
            lower_case_term = term[0].lower() + term[1:]
            upper_case_term = term[0].upper() + term[1:]
            if lower_case_term not in term_dict.keys() and upper_case_term not in term_dict.keys():
                term_dict[term] = 1
            elif term == lower_case_term and upper_case_term in term_dict.keys():
                term_dict[lower_case_term] = term_dict.pop(upper_case_term) + 1
            elif lower_case_term in term_dict.keys():
                term_dict[lower_case_term] += 1
            else:  # upper case
                term_dict[term] += 1
        return term_dict

    def is_symbol(self, token, next_token):
        return token in ["#", '@'] or (
                next_token in self.symbols and self.is_number(token))

    def init_tokenizer_dict(self):
        tokenizers_dict = dict()
        tokenizers_dict['symbol'] = SymbolTokenizer()
        tokenizers_dict['number'] = NumberTokenizer()
        tokenizers_dict['suffix'] = SuffixTokenizer()
        tokenizers_dict['URL'] = URLTokenizer()
        tokenizers_dict['entity'] = EntityTokenizer()
        return tokenizers_dict

    def has_special_suffix(self, last_token, token):
        return last_token.endswith("st" or "th" or "nd" or "rd") and self.is_number(
            last_token[0:-2]) and token.isalpha()

    def is_valid_token(self, token):
        return re.match("^[A-Za-z0-9]*$", token) and re.match("^[A-Za-z0-9]*$", token[0])

    def is_invalid_token(self, token):
        return token.lower() in self.stop_words or len(token) <= 1 or token.startswith(('/', '.', '-'))

    def is_entity(self, token, next_token):
        return token[0].isupper() and next_token[0].isupper()
