class Document:

    def __init__(self, tweet_id=None, tokenized_text=None,term_doc_dictionary=None):
        """
        :param tweet_id: tweet id
        :param tokenized_text: tokenized_text
        :param term_doc_dictionary: dictionary of term and documents.
        :param buzzwords_coefficient: measurement of entities in tweet #todo remember to add because it is mandatory
        """
        self.tweet_id = tweet_id
        self.tokenized_text = tokenized_text
        self.term_doc_dictionary = term_doc_dictionary

