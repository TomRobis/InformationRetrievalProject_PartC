import math

import utils


class post_processor:
    def __init__(self, indexer):
        self.indexer = indexer
        self.current_tweets_postings = dict()

    def post_process(self):
        """
        firstly, dump postings of every character in memory to disc.
        secondly, enforce the following rules:
        1.make sure every word appears only once in both postings and index, thereby making sure every entity appears at least twice.
        2.unify small words' postings and capital letter words' postings
        """

        self.empty_postings_files_to_disc()
        self.enforce_parsing_rules()

    def empty_postings_files_to_disc(self):
        #  write the remaining terms postings to disc
        character_to_postings_file = self.indexer.get_character_to_postings_files()
        for character in character_to_postings_file.keys():
            if character_to_postings_file[character][0]:
                self.indexer.merge_postings(character)

        utils.save_obj(self.indexer.get_tweets_postings_file(), str(self.indexer.get_tweets_postings_counter()),
                       self.indexer.get_config().get_tweets_postings_path())

    def enforce_parsing_rules(self):
        """

        :return:
        """
        character_to_terms_to_unify = dict()
        character_to_terms_once_in_corpus = dict()
        for character in self.indexer.get_special_characters():
            character_to_terms_once_in_corpus[character] = set()
            character_to_terms_to_unify[character] = set()

        character_to_terms_to_unify, character_to_terms_once_in_corpus = self.collect_terms_that_dissatisfy_rules(
            character_to_terms_to_unify, character_to_terms_once_in_corpus)
        self.remove_bad_terms_from_terms_index(character_to_terms_once_in_corpus)
        self.remove_bad_terms_from_terms_index(character_to_terms_to_unify)
        self.update_tweets_postings(character_to_terms_to_unify, character_to_terms_once_in_corpus)
        self.update_terms_postings(character_to_terms_to_unify,character_to_terms_once_in_corpus)


    def collect_terms_that_dissatisfy_rules(self, character_to_terms_to_unify, character_to_terms_to_delete):
        """

        :param character_to_terms_to_unify:
        :param character_to_terms_to_delete:
        :return:
        """
        terms_index = self.indexer.get_terms_index()
        for term in terms_index.keys():
            lower_case_term = term[0].lower() + term[1:]
            term_starts_with_lower_case = term[0].lower()
            if terms_index[term][1] == 1:
                character_to_terms_to_delete[term_starts_with_lower_case].add(term)
            # only considered if term is uppercase
            elif term[0].isupper() and term in terms_index.keys() and lower_case_term in terms_index.keys():
                terms_index[lower_case_term][0] += terms_index[term][0]  # df
                terms_index[lower_case_term][1] += terms_index[term][1]  # term_freq_in_corpus
                character_to_terms_to_unify[term_starts_with_lower_case].add(term)
        return character_to_terms_to_unify, character_to_terms_to_delete

    def remove_bad_terms_from_terms_index(self, character_to_terms_to_delete):
        terms_index = self.indexer.get_terms_index()
        for character in character_to_terms_to_delete.keys():
            for term in character_to_terms_to_delete[character]:
                del terms_index[term]

    def update_tweets_postings(self, character_to_terms_to_unify, character_to_terms_once_in_corpus):
        """

        :param character_to_terms_to_unify:
        :param character_to_terms_once_in_corpus:
        :return:
        """
        terms_index = self.indexer.get_terms_index()
        for i in range(self.indexer.get_tweets_postings_counter()):
            tweets_postings_file = utils.load_obj(str(i), self.indexer.get_config().get_tweets_postings_path())
            for tweet in tweets_postings_file.keys():
                sigma_wij = 0
                tweet_posting = tweets_postings_file[tweet]
                term_doc_dict = tweet_posting[2]
                for term in term_doc_dict.keys():
                    if term in character_to_terms_once_in_corpus[term[0]]:
                        del term_doc_dict[term]
                    elif term[0].isupper() and term in character_to_terms_to_unify[term[0]]:
                        lower_case_term = term[0].lower() + term[1:]
                        # calculates tf-idf with term_freq_in_tweet, max_tf, df and N. the upper-case term
                        # is removed and replaced later with an entry of its' lower_case form as key and a tf-idf value
                        tf_idf = self.calculate_tf_idf(term_doc_dict.pop(term),tweet_posting[1],terms_index[lower_case_term],self.indexer.get_doc_id())
                        term_doc_dict[lower_case_term] = tf_idf
                        sigma_wij += tf_idf
                tweet_posting[1] = abs(sigma_wij)
            utils.save_obj(tweets_postings_file, str(i),self.indexer.get_config().get_tweets_postings_path())

    def calculate_tf_idf(self, term_freq_in_tweet, max_tf, df, N):
        """

        :param term_freq_in_tweet:
        :param max_tf:
        :param df:
        :param N:
        :return:
        """
        return (term_freq_in_tweet / max_tf) * math.log(self.indexer.get_config().get_log_basis_for_idf(),N/df)

    def update_terms_postings(self, character_to_terms_to_unify, character_to_terms_once_in_corpus):
        """

        :param character_to_terms_to_unify:
        :param character_to_terms_once_in_corpus:
        :return:
        """
        for character in self.indexer.get_special_characters():
            terms_postings_file_for_char = utils.load_obj(character, self.indexer.get_config().get_terms_postings_path())
            for term in terms_postings_file_for_char.keys():
                if term in character_to_terms_once_in_corpus[term[0]]:
                    del terms_postings_file_for_char[term]
                elif term[0].isupper() and term in character_to_terms_to_unify[term[0]]:
                    lower_case_term = term[0].lower() + term[1:]
                    terms_postings_file_for_char[lower_case_term].update(terms_postings_file_for_char.pop(term))

            utils.save_obj(terms_postings_file_for_char, character, self.indexer.get_config().get_terms_postings_path())


