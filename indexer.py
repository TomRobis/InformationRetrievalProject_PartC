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

        self.special_characters = ascii_lowercase + digits + '#' + '@' + '~'  # ~ stands for anything other than the rest
        for character in self.special_characters:
            self.character_to_postings_file[character] = [dict(), 0]
            # character_full_path = IO_handler.get_dir_file(terms_dir_name,character)
            # IO_handler.from_dic_to_json(dict(),character_full_path)
            utils.save_obj(dict(), character, config.get_terms_postings_path())

        #  responsible for saving tweets' information in disc and memory
        self.tweets_index = dict()  # maps tweets to their postings in disc
        self.tweets_postings_file = dict()  # maps tweets to their relevant information

        self.terms_dir_name = config.get_terms_postings_path()
        self.tweets_dir_name = config.get_tweets_postings_path()
        #  threshold for file sizes, relates to number of tweets indexed
        self.OPTIMAL_TERMS_FILE_SIZE = config.get_terms_postings_file_size()
        self.OPTIMAL_TWEETS_FILE_SIZE = config.get_tweets_postings_file_size()

        self.term_postings_counter = 1
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
        try:
            if term is not None:  # bad terms
                # update the inverted index
                if term not in self.terms_index:  # term never indexed before
                    self.terms_index[term] = [0, 0]
                self.terms_index[term][0] += 1  # df
                self.terms_index[term][1] += term_freq_in_tweet  # term_freq_in_corpus

                # update the postings file.

                #  grab the postings file for the term
                term_starts_with = term[0].lower()

                if term_starts_with in self.character_to_postings_file.keys():  # get postings file for character
                    character_postings_file = self.character_to_postings_file[term_starts_with][
                        0]  # every familiar character
                else:  # todo consider removing
                    character_postings_file = self.character_to_postings_file['~'][0]  # other special characters
                    term_starts_with = '~'
                #  update the postings file you found
                if term not in character_postings_file.keys():
                    character_postings_file[term] = dict()  # new term_tweet_dict
                if self.doc_id not in character_postings_file[term]:  # check if there's an old entry
                    character_postings_file[term][self.doc_id] = dict()
                character_postings_file[term][self.doc_id] = term_freq_in_tweet
                #  update the character's counter of terms
                self.character_to_postings_file[term_starts_with][1] += 1  # per posting, not per term.
                #  write postings to disc if necessary
                if self.postings_too_large(self.character_to_postings_file[term_starts_with][1],
                                           self.OPTIMAL_TERMS_FILE_SIZE):
                    self.merge_postings(term_starts_with)
        except:
            raise ValueError('problem with indexing term ' + term)

    # merges postings file in disc with posting file in memory, and write the merged postings file to disc.
    # empties the one in memory after writing to disc.
    def merge_postings(self, character):
        #  grab postings file from disc.

        former_postings_file_in_disc = utils.load_obj(character, self.terms_dir_name)
        current_postings_file_in_memory = self.character_to_postings_file[character][0]

        #  for each term in posting file previously stored in disc:
        for term in former_postings_file_in_disc.keys():
            former_term_tweets_dict = former_postings_file_in_disc[term]
            if term not in current_postings_file_in_memory.keys():  # new term - stored in disc but not in memory.
                current_postings_file_in_memory[
                    term] = former_term_tweets_dict  # copy the dictionary to postings file in memory
            else:  # appeared in postings both in memory and in disc
                for term_tweet_entry in former_term_tweets_dict.keys():  # update the dictionary in memory to hold all postings.
                    current_postings_file_in_memory[term][term_tweet_entry] = former_term_tweets_dict[term_tweet_entry]

        utils.save_obj(current_postings_file_in_memory, character, self.terms_dir_name)
        current_postings_file_in_memory.clear()  # remove old entries already written to disc from memory

    # after indexing the terms, updates the tweet's information in the indexer.
    # if the postings file for the tweets is too large, it is moved to the disc and emptied in memory.
    def update_tweets_information(self, document, max_tf):
        tweets_full_path = utils.get_dir_file(self.tweets_dir_name, self.tweets_postings_counter)
        self.tweets_index[self.doc_id] = tweets_full_path  # update the tweets' index with the path
        self.tweets_postings_file[self.doc_id] = [document.tweet_id, document.tweet_date, max_tf,
                                                  len(document.term_doc_dictionary.keys())]

        # move tweets postings to disc if needed
        if self.postings_too_large(self.doc_id, self.OPTIMAL_TWEETS_FILE_SIZE):
            #  write the postings to disc and empty the dictionary in memory.
            utils.save_obj(self.tweets_postings_file, str(self.tweets_postings_counter), self.tweets_dir_name)
            self.tweets_postings_counter += 1
            self.tweets_postings_file.clear()  # delete postings file after writing it to disc.

    #  calculates whether postings file is too large
    def postings_too_large(self, current_postings_size, optimal_file_size):
        return current_postings_size % optimal_file_size == optimal_file_size - 1

    def empty_postings_files_to_disc(self):
        #  write the remaining terms postings to disc
        for character in self.character_to_postings_file.keys():
            if self.character_to_postings_file[character][0]:
                self.merge_postings(character)

        #  write the remaining tweets postings to disc
        tweets_postings_full_path = utils.get_dir_file(self.tweets_dir_name, self.tweets_postings_counter)
        self.tweets_index[self.doc_id] = tweets_postings_full_path
        utils.save_obj(self.tweets_postings_file, str(self.tweets_postings_counter), self.tweets_dir_name)

    def get_config(self):
        return self.config

    def post_process(self):
        """
        firstly, dump postings of every character in memory to disc.
        secondly, enforce the following rules:
        1.make sure every word appears only once in both postings and index, thereby making sure every entity appears at least twice.
        2.unify small words' postings and capital letter words' postings
        """

        self.empty_postings_files_to_disc()
        self.enforce_parsing_rules()

    def enforce_parsing_rules(self):
        """
        initiate data structures to save every term that requires update from postings, and send it to
        methods that deal with updating the postings files and terms index according to the pre-set rules.
        """
        unified_terms = dict()
        character_to_deleted_terms = dict()
        special_characters_no_upper_case = ascii_lowercase + digits + '#' + '@' + '~'
        for character in self.special_characters:
            character_to_deleted_terms[character] = set()
            unified_terms[character] = set()

        unified_terms, character_to_deleted_terms = self.collect_terms_that_dissatisfy_rules(unified_terms,
                                                                                             character_to_deleted_terms)
        self.enforce_parsing_rules_on_collected_terms(unified_terms, character_to_deleted_terms,special_characters_no_upper_case)

    def collect_terms_that_dissatisfy_rules(self, unified_terms, character_to_deleted_terms):
        """
        prepares the data structures mentioned below, based on terms_index information.
        no deletion is performed here, only setup of the data structures.
        :param unified_terms: dict that maps a character to a set of every term that starts with that letter,
         that has had its' lower case form united with its' upper case form.
        :param character_to_deleted_terms: set of every term that has appeared only once in the corpus.
        :return: unified_terms and character_to_deleted_terms
        """
        for term in self.terms_index.keys():
            if term[0].isalpha() and term.capitalize() in self.terms_index.keys() and term.lower() in self.terms_index.keys():
                upper_case_term = term.capitalize()
                lower_case_term = term.lower()
                print(self.terms_index[lower_case_term],self.terms_index[upper_case_term])
                self.terms_index[lower_case_term][0] += self.terms_index[upper_case_term][0]
                self.terms_index[lower_case_term][1] += self.terms_index[upper_case_term][1]
                print(self.terms_index[lower_case_term], self.terms_index[upper_case_term])
                unified_terms[lower_case_term[0]].add(lower_case_term)

            elif self.terms_index[term][1] == 1:  # appears at least twice if it enters first if statement
                # save the term to delete from postings later
                if term[0] not in self.special_characters:
                    character_to_deleted_terms['~'].add(term)
                else:
                    character_to_deleted_terms[term[0].lower()].add(term)
        return unified_terms, character_to_deleted_terms

    def enforce_parsing_rules_on_collected_terms(self, unified_terms, character_to_deleted_terms,special_characters_no_upper_case):
        """
        updates postings and terms_index according to data structures holding terms that required an update.
        performs deletions if necessary.
        :param unified_terms: dict that maps a character to a set of every term that starts with that letter,
         that has had its' lower case form united with its' upper case form.
        :param character_to_deleted_terms: set of every term that has appeared only once in the corpus.
        """
        for character in special_characters_no_upper_case:
            unified_terms_for_char = unified_terms[character]
            deleted_terms_for_char = character_to_deleted_terms[character]
            if len(unified_terms_for_char) == 0 and len(deleted_terms_for_char) == 0:
                continue
            postings_file_for_char = utils.load_obj(character, self.terms_dir_name)
            if character.isalpha():
                self.unify_terms(postings_file_for_char,unified_terms_for_char)
            self.remove_terms_with_one_appearance_in_corpus(postings_file_for_char,deleted_terms_for_char)


    def unify_terms(self, postings_file_for_char, unified_terms_for_char):
        for unified_term in unified_terms_for_char:
            lower_case_term = unified_term.lower()
            upper_case_term = unified_term.capitalize()
            for doc_id in postings_file_for_char[upper_case_term].keys():
                if doc_id not in postings_file_for_char[lower_case_term].keys():
                    postings_file_for_char[lower_case_term][doc_id] = 0
                postings_file_for_char[lower_case_term][doc_id] += postings_file_for_char[upper_case_term][doc_id]
            del self.terms_index[upper_case_term]
            del postings_file_for_char[upper_case_term]

    def remove_terms_with_one_appearance_in_corpus(self, postings_file_for_char,deleted_terms_for_char):
        for deleted_term in deleted_terms_for_char:
            del self.terms_index[deleted_term]
            del postings_file_for_char[deleted_term]
