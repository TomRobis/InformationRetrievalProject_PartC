# DO NOT MODIFY CLASS NAME
import math

import utils




class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.config = config
        self.terms_index = dict()  # maps terms to their postings

        self.tweets_postings_file = dict()  # maps tweets to their relevant information

        self.tweets_postings_counter = 0
        self.doc_id = 0  # counter for the number of tweets in the corpus

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document):
        """

        :param document:
        :return:
        """
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
        lower_case_term = term[0].lower() + term[1:]
        upper_case_term = term[0].upper() + term[1:]
        if lower_case_term not in self.terms_index.keys() and upper_case_term not in self.terms_index.keys():  # term never indexed before
            self.terms_index[term] = [0, 0, set()]
            self.insert_term_to_terms_index(term,term_freq_in_tweet)
        elif lower_case_term in self.terms_index.keys():
            self.insert_term_to_terms_index(lower_case_term, term_freq_in_tweet)
        elif term[0].islower() and term not in self.terms_index.keys():
            self.terms_index[term] = self.terms_index.pop(upper_case_term)
            self.insert_term_to_terms_index(term,term_freq_in_tweet)
        else:
            self.insert_term_to_terms_index(term, term_freq_in_tweet)

    def insert_term_to_terms_index(self, term, term_freq_in_tweet):
        """

        :param term:
        :param term_freq_in_tweet:
        :return:
        """
        self.terms_index[term][0] += 1  # df
        self.terms_index[term][1] += term_freq_in_tweet  # term_freq_in_corpus
        self.terms_index[term][2].add(self.doc_id)  # set of docs


    # after indexing the terms, updates the tweet's information in the indexer.
    # if the postings file for the tweets is too large, it is moved to the disc and emptied in memory.
    def update_tweets_information(self, document, max_tf):
        """

        :param document:
        :param max_tf:
        :return:
        """
        self.tweets_postings_file[self.doc_id] = [document.tweet_id, max_tf, document.term_doc_dictionary]

        # move tweets postings to disc if needed
        if self.postings_too_large(self.doc_id, self.config.get_tweets_postings_file_size()):
            self.dump_tweet_postings_to_disc()


    def postings_too_large(self, current_postings_size, optimal_file_size):
        """

        :param current_postings_size:
        :param optimal_file_size:
        :return:
        """
        return current_postings_size % optimal_file_size == optimal_file_size - 1

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        return utils.load_obj(name=fn)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        utils.save_obj(obj=self.terms_index, name=fn, path='')

    def post_process(self):
        self.dump_tweet_postings_to_disc()
        self.update_tweets_postings()

    def update_tweets_postings(self):
        """

        :return:
        """
        for i in range(self.tweets_postings_counter):
            tweets_postings_file = utils.load_obj(str(i+1), self.config.get_tweets_postings_path())
            for doc_id in tweets_postings_file.keys():
                tweet_posting = tweets_postings_file[doc_id]
                self.update_single_tweet_postings(tweet_posting)
            utils.save_obj(tweets_postings_file, str(i+1), self.config.get_tweets_postings_path())

    def update_single_tweet_postings(self, tweet_posting):
        """

        :param tweet_posting:
        :return:
        """
        sigma_wij = 0
        updated_term_doc_dict = dict()
        term_doc_dict = tweet_posting[2]
        for term in term_doc_dict.keys():
            lower_case_term = term[0].lower() + term[1:]
            # dont write to new dict = delete,  when term_freq_in_corpus == 1.
            # deletion from terms_index (del)  and postings (not saved in updated, "continue")
            if term in self.terms_index.keys() and self.terms_index[term][1] == 1:
                del self.terms_index[term]
                continue
            # calculates tf-idf with term_freq_in_tweet, max_tf, df and N. the upper-case term
            # is removed and replaced later with an entry of its' lower_case form as key and a tf-idf value
            elif term[0].isupper() and lower_case_term in self.terms_index.keys():
                df = self.terms_index[lower_case_term][0]
            else:
                df = self.terms_index[term][0]
            tf_idf = self.calculate_tf_idf(term_doc_dict[term], tweet_posting[1], df, self.doc_id)
            updated_term_doc_dict[lower_case_term] = tf_idf
            sigma_wij += math.pow(tf_idf, 2)
        tweet_posting[1] = sigma_wij
        tweet_posting[2] = updated_term_doc_dict

    def calculate_tf_idf(self, term_freq_in_tweet, max_tf, df, N):
        """

        :param term_freq_in_tweet:
        :param max_tf:
        :param df:
        :param N:
        :return:
        """
        tf = term_freq_in_tweet / max_tf
        idf = math.log((N / df), self.config.get_log_basis_for_idf())
        return tf * idf

    def get_config(self):
        return self.config

    def get_terms_index(self):
        return self.terms_index

    def get_tweets_postings_counter(self):
        return self.tweets_postings_counter


    def dump_tweet_postings_to_disc(self):
        #  write the postings to disc and empty the dictionary in memory.
        self.tweets_postings_counter += 1
        utils.save_obj(self.tweets_postings_file, str(self.tweets_postings_counter),
                       self.config.get_tweets_postings_path())
        self.tweets_postings_file.clear()

