# DO NOT MODIFY CLASS NAME
from string import ascii_lowercase, digits, ascii_uppercase

import utils


class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.config = config
        self.terms_index = dict()  # maps terms to their postings in disc

        # responsible for holding postings in disc and memory
        self.character_to_postings_file = dict()  # maps character to character postings file in memory

        # ~ stands for any character different than the rest
        self.special_characters = ascii_lowercase + digits + '#' + '@'
        for character in self.special_characters:
            self.character_to_postings_file[character] = [dict(), 0]
            utils.save_obj(dict(), character, config.get_terms_postings_path())

        self.tweets_postings_file = dict()  # maps tweets to their relevant information

        self.tweets_postings_counter = 1
        self.doc_id = 0  # counter for the number of tweets in the corpus

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document):
        # update the number of docs in the corpus
        self.doc_id += 1

        # index every term in document and return the term who appeared most frequently.
        max_tf = self.index_all_terms(document)

        self.update_tweets_information(document, max_tf)


    def index_all_terms(self, document):
        """
            indexes every term and writes terms postings to disc, if needed.
            @return: int - max_tf = maximal number of appearances of term in tweet
        """
        document_dictionary = document.term_doc_dictionary
        max_tf = 0
        for term in document_dictionary.keys():
            term_freq_in_tweet = document_dictionary[term]
            # index the term.
            self.index_term(term, term_freq_in_tweet)
            # keep max_tf updated
            max_tf = max(max_tf, term_freq_in_tweet)
        return max_tf

    def index_term(self, term, term_freq_in_tweet):
        """
            firstly, update the inverted index.
            secondly, update the correct postings file.
            additionally, if necessary, write said postings file to disc and empty its' memory.
        """
        # update the inverted index
        if term not in self.terms_index:  # term never indexed before
            self.terms_index[term] = [0, 0]
        self.terms_index[term][0] += 1  # df
        self.terms_index[term][1] += term_freq_in_tweet  # term_freq_in_corpus

        #  grab the postings file for the term
        term_starts_with = term[0].lower()
        # problems here indicate ~ needs values
        character_postings_file = self.character_to_postings_file[term_starts_with][0]

        #  update the postings file you found
        if term not in character_postings_file.keys():
            character_postings_file[term] = set()
        if self.doc_id not in character_postings_file[term]:  # check if there's an old entry
            character_postings_file[term].add(self.doc_id)
        # character_postings_file[term][self.doc_id] = term_freq_in_tweet
        #  update the character's counter of terms
        self.character_to_postings_file[term_starts_with][1] += 1  # per posting, not per term.
        #  write postings to disc if necessary
        if self.postings_too_large(self.character_to_postings_file[term_starts_with][1],self.config.get_terms_postings_file_size()):
            self.merge_postings(term_starts_with)

    # merges postings file in disc with posting file in memory, and write the merged postings file to disc.
    # empties the one in memory after writing to disc.
    def merge_postings(self, character):
        #  grab postings file from disc.

        former_postings_file_in_disc = utils.load_obj(character, self.config.get_terms_postings_path())
        current_postings_file_in_memory = self.character_to_postings_file[character][0]

        #  for each term in posting file previously stored in disc:
        for term in former_postings_file_in_disc.keys():
            former_term_tweets_set = former_postings_file_in_disc[term]
            if term not in current_postings_file_in_memory.keys():  # new term - stored in disc but not in memory.
                current_postings_file_in_memory[term] = set()
            current_postings_file_in_memory[term].update(former_term_tweets_set)

        utils.save_obj(current_postings_file_in_memory, character, self.config.get_terms_postings_path())
        current_postings_file_in_memory.clear()  # remove old entries already written to disc from memory

    # after indexing the terms, updates the tweet's information in the indexer.
    # if the postings file for the tweets is too large, it is moved to the disc and emptied in memory.
    def update_tweets_information(self, document, max_tf):
        self.tweets_postings_file[self.doc_id] = [document.tweet_id, max_tf,document.term_doc_dictionary]

        # move tweets postings to disc if needed
        if self.postings_too_large(self.doc_id, self.config.get_tweets_postings_file_size()):
            #  write the postings to disc and empty the dictionary in memory.
            utils.save_obj(self.tweets_postings_file, str(self.tweets_postings_counter),
                        self.config.get_tweets_postings_path())
            self.tweets_postings_counter += 1
            self.tweets_postings_file.clear()  # delete postings file after writing it to disc.

    #  calculates whether postings file is too large
    def postings_too_large(self, current_postings_size, optimal_file_size):
        return current_postings_size % optimal_file_size == optimal_file_size - 1


    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        indexes = utils.load_obj(name='indexes', path=fn)
        self.terms_index = indexes[0]
        self.tweets_index = indexes[1]
        return self.terms_index, self.tweets_index

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        utils.save_obj(obj=(self.terms_index, self.tweets_index), name='indexes', path=fn)

    def get_config(self):
        return self.config

    def get_special_characters(self):
        return self.special_characters

    def get_character_to_postings_files(self):
        return self.character_to_postings_file

    def get_tweets_postings_file(self):
        return self.tweets_postings_file

    def get_tweets_postings_counter(self):
        return self.tweets_postings_counter

    def get_doc_id(self):
        return self.doc_id

    def get_terms_index(self):
        return self.terms_index

