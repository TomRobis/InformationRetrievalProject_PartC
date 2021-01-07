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

    def __init__(self, stemming):
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

    def parse_sentence(self, text):
        """
        based on Factory Design Pattern, every token has a special tokenizer that parses it.
        :param text: string containing words to be parsed
        :return: a list of tokenized words
        """
        parsed_tokens = []
        text_tokens = word_tokenize(text)
        i = 0
        while i in range(len(text_tokens)):
            token = text_tokens[i]
            if token not in self.useless_token_list:
                # some terms are consisted of two tokens, in which case, the next token is skipped.

                if i < len(text_tokens) - 1 and self.is_symbol(token, text_tokens[i + 1]):
                    parsed_tokens += self.string_to_tokenizer['symbol'].tokenize(token, text_tokens[i + 1])
                    i += 1
                elif i < len(text_tokens) - 1 and self.has_special_suffix(token, text_tokens[i + 1]):
                    parsed_tokens += self.string_to_tokenizer['suffix'].tokenize(token, text_tokens[i + 1])
                    i += 1
                elif i < len(text_tokens) - 1 and self.is_entity(token, text_tokens[i + 1]):
                    parsed_tokens += self.string_to_tokenizer['entity'].tokenize(token, text_tokens[i + 1])
                    i += 1
                # while other terms are consisted of only one.

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

        document = Document(tweet_id, tokenized_text, term_dict)
        return document

    def is_number(self, token):
        """
        determines if num is in fact a number
        :param token: token tested
        :return: bool: True if number else False
        """
        return search("[0-9]", token) and (False if any(ord(c) > 57 or ord(c) < 44 for c in token) else True) and \
               token.count('.') < 2 and token.count('/') < 2

    def create_term_doc_dict(self, tokenized_text):
        """
        creates a dictionary that maps a term to its' num of appearances in the current tweet, while
        also taking into account lower-case and upper-case letters.
        :param tokenized_text: list of words from which to create the dictionary
        :return: said dictionary.
        """
        term_dict = dict()
        for term in tokenized_text:
            lower_case_term = term[0].lower() + term[1:]
            upper_case_term = term[0].upper() + term[1:]
            if lower_case_term not in term_dict.keys() and upper_case_term not in term_dict.keys():  # new entry
                term_dict[term] = 1
            elif term == lower_case_term and upper_case_term in term_dict.keys():  # upper-case followed by lower-case
                term_dict[lower_case_term] = term_dict.pop(upper_case_term) + 1
            elif lower_case_term in term_dict.keys():  # lower-case followed by upper-case or lower-case
                term_dict[lower_case_term] += 1
            else:  # upper case followed by upper-case
                term_dict[term] += 1
        return term_dict

    def is_symbol(self, token, next_token):
        """
        determines whether the combination of two following tokens make a special token that uses both.
        :param token: some word in the text.
        :param next_token: some string that has appeared after token in the text.
        :return: bool: True if symbol else False
        """
        return token in ["#", '@'] or (
                next_token in self.symbols and self.is_number(token))

    def init_tokenizer_dict(self):
        """
        this method acts as a "seperate class" that initiates the factory.
        every tokenizer's job is to parse a term that matches a certain characteristic
        :return: dict: mapping a pre-determined string to its' matching tokenizer
        """
        tokenizers_dict = dict()
        tokenizers_dict['symbol'] = SymbolTokenizer()
        tokenizers_dict['number'] = NumberTokenizer()
        tokenizers_dict['suffix'] = SuffixTokenizer()
        tokenizers_dict['URL'] = URLTokenizer()
        tokenizers_dict['entity'] = EntityTokenizer()
        return tokenizers_dict

    def has_special_suffix(self, last_token, token):
        """
        checks whether two tokens make a special term, based on the ending of the first token.
        :param last_token: following token.
        :param token: first token.
        :return: bool: True if has special suffix else False
        """
        return last_token.endswith("st" or "th" or "nd" or "rd") and self.is_number(
            last_token[0:-2]) and token.isalpha()

    def is_valid_token(self, token):
        """
        checks whether term is a token we want to parse
        :param token: string checked
        :return: bool: True if term is a token we want to parse, else False
        """
        return re.match("^[A-Za-z0-9]*$", token) and re.match("^[A-Za-z0-9]*$", token[0])

    def is_invalid_token(self, token):
        """
        checks whether term is a token we don't want to parse
        :param token: string checked
        :return: bool: False if term is a token we want to parse, else True
        """
        return token.lower() in self.stop_words or len(token) <= 1 or token.startswith(('/', '.', '-'))

    def is_entity(self, token, next_token):
        """
        an entity is determined as two consecutive words with upper-case
        :param token: some token.
        :param next_token: token following said token.
        :return: bool: True if combination of tokens is an entity else False
        """
        return token[0].isupper() and next_token[0].isupper()
