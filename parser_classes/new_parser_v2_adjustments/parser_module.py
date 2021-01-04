from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from parser_classes.NumberTokenizer import NumberTokenizer
from parser_classes.SuffixTokenizer import SuffixTokenizer
from parser_classes.SymbolTokenizer import SymbolTokenizer
from parser_classes.URLTokenizer import URLTokenizer
from parser_classes.new_parser_v2_adjustments.TokenizerFactory import TokenizerFactory

from stemmer import Stemmer
from document import Document
from re import search, split


class Parse:

    def __init__(self, stemming):
        self.stop_words = stopwords.words('english')
        self.stemming = stemming
        self.stem = Stemmer()

        self.useless_token_list = ['t.co', 'https', 'RT']
        self.TokenizerFactory = TokenizerFactory()

    def parse_sentence(self, text):
        # to be able to always send token and next token

        parsed_tokens = []
        i = 0

        text_tokens = word_tokenize(text)

        text.append('end_of_text_token')
        text.append('end_of_text_next_token')
        token = text_tokens[i]
        next_token = text_tokens[i + 1]

        while token != 'end_of_text_token':
            if not self.is_invalid_token(token):  # todo might add emojies later
                tokenizer = self.TokenizerFactory.get_tokenizer(token, next_token)
                if tokenizer.uses_next_token():
                    parsed_tokens += tokenizer.tokenize(token, next_token)
                    i += 1
                else:
                    parsed_tokens += tokenizer.tokenize(token)
            i += 1
            token = text_tokens[i]
            next_token = text_tokens[i + 1]
        return [token for token in parsed_tokens if token not in self.stop_words]

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        urls = doc_as_list[3]
        quoted_text = doc_as_list[8]
        quoted_urls = doc_as_list[9]

        urls_tokens = ''

        # quoted text should be parsed as well
        if quoted_text:
            full_text += ' ' + quoted_text

        # If either full URL exists, parse separately for terms. next_token as identifier for URL
        urls_tokens += ''.join(self.TokenizerFactory.get_tokenizer(urls, 'URL'))

        urls_tokens += ''.join(self.TokenizerFactory.get_tokenizer(quoted_urls, 'URL'))
        full_text += urls_tokens

        tokenized_text = self.parse_sentence(full_text)

        #  stemming added according to user request.
        if self.stemming:
            tokenized_text = self.stem.porter_stemmer(tokenized_text)
        term_dict = self.create_term_doc_dict(tokenized_text)

        document = Document(tweet_id, tweet_date, tokenized_text, term_dict)

        return document

    def create_term_doc_dict(self, tokenized_text):
        term_dict = dict()
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 0
            term_dict[term] += 1
        return term_dict
