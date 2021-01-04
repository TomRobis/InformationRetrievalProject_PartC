from re import search
from ranker import Ranker
import utils


# DO NOT MODIFY CLASS NAME
class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model 
    # parameter allows you to pass in a precomputed model that is already in 
    # memory for the searcher to use such as LSI, LDA, Word2vec models. 
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None):
        self._parser = parser
        self._indexer = indexer
        self._ranker = None
        self._model = model
        self.config = indexer.get_config()
        # indexes = self._indexer.load_index('indexes')
        self.tweets_index = self._indexer.tweets_postings_file
        self.terms_index = self._indexer.terms_index

        self.terms_postings_files_dir = self.config.get_terms_postings_path()
        self.tweets_postings_files_dir = self.config.get_tweets_postings_path()
        self.OPTIMAL_TWEETS_FILE_SIZE = self.config.get_tweets_postings_file_size()

        # self.spell = SpellChecker()

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query, k=None):
        """ 
        Executes a query over an existing index and returns the number of 
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and 
            a list of tweet_ids where the first element is the most relavant 
            and the last is the least relevant result.
        """
        query_as_list = self._parser.parse_sentence(query)
        if not query_as_list:
            return []
        term_doc_dict = self._parser.create_term_doc_dict(query_as_list)

        q_max_tf = max(term_doc_dict.values())
        query_tweets_postings,query_terms_postings,num_of_docs_in_corpus,q_Wiq_dict = self.relevant_docs_from_posting(query_as_list,term_doc_dict,q_max_tf)
        self._ranker = Ranker(query_tweets_postings,query_terms_postings,num_of_docs_in_corpus,q_Wiq_dict)
        ranked_docs_list_of_lists = self._ranker.rank_relevant_docs()
        top_k_ranked_docs = self._ranker.retrieve_top_k(ranked_docs_list_of_lists) #todo fetch k from somewhere
        return top_k_ranked_docs


    def relevant_docs_from_posting(self, parsed_query,term_doc_dict,q_max_tf): #todo fix parameters when switching to ranker_v1
        # set spelling correction
        spelling = False
        if spelling:
            parsed_query = self.speller(parsed_query)
        # maps first char of every term in query to its' corresponding terms in query
        query_char_to_terms_dict = self.get_char_to_query_terms_dict(parsed_query)
        query_terms_postings = self.get_information_for_q_term(query_char_to_terms_dict)  # get information for each term in query
        query_tweets_postings = self.get_information_for_q_terms_tweets(query_terms_postings)
        for term in parsed_query:
            if term in query_terms_postings.keys():
                query_terms_postings[term].append(term_doc_dict[term])
        Wiq_dict = self.calculate_Wiq_vector(term_doc_dict,q_max_tf,parsed_query)
        return query_tweets_postings, query_terms_postings,len(self.tweets_index.keys()),Wiq_dict



# from re import search
# import utils
# from spellchecker import SpellChecker
#
# class Searcher:
#
#     def __init__(self, tweets_index,terms_index, terms_postings_files_dir, tweets_postings_files_dir,OPTIMAL_TWEETS_FILE_SIZE):
#         self.tweets_index = tweets_index
#         self.terms_index = terms_index #todo irrelevant because we calculate the addresses, should remove from project
#
#         self.terms_postings_files_dir = terms_postings_files_dir
#         self.tweets_postings_files_dir = tweets_postings_files_dir
#         self.OPTIMAL_TWEETS_FILE_SIZE = OPTIMAL_TWEETS_FILE_SIZE
#
#         self.spell = SpellChecker()



    #  get all relevant postings files from disc according to the query.
    #  we extract only a set of doc_ids from each postings, because the other information isn't relevant atm.
    def get_information_for_q_term(self, char_to_query_terms):
        try:
            query_terms_postings = dict()
            for char in char_to_query_terms: #load the postings file for the terms starting with char
                char_postings_file_for_q_term = utils.load_obj(char,self.terms_postings_files_dir)
                q_terms = char_to_query_terms[char] #every term in query that starts with char
                for q_term in q_terms:  # get information for each term in query
                    if q_term in self.terms_index.keys():
                        q_term_df = self.terms_index[q_term][0]
                        q_term_tweet_dict = char_postings_file_for_q_term[q_term]
                        query_terms_postings[q_term] = [q_term_df, q_term_tweet_dict]
            return query_terms_postings
        except:
                raise IOError("Can't get information for term: " + q_term)

    # make a dict that maps a character to all terms that start with it in the query.
    def get_char_to_query_terms_dict(self, parsed_query):
        query_char_to_terms_dict = dict()
        for q_term in parsed_query:
            q_term_starts_with = q_term[0].lower()
            if search("[a-z 0-9#@]", q_term_starts_with) is None:
                q_term_starts_with = '~'  # identifier for term that doesn't start with the above letters
            if q_term_starts_with not in query_char_to_terms_dict.keys():  # if char doesn't have a word in query that starts with it
                query_char_to_terms_dict[q_term_starts_with] = []
            query_char_to_terms_dict[q_term_starts_with].append(q_term)
        return query_char_to_terms_dict

    def speller(self, query_as_list):
        spelled_query = self.spell.unknown(query_as_list)
        return spelled_query

    def get_information_for_q_terms_tweets(self,query_terms_postings):
        try:
            query_tweets_postings = dict()
            #  match every postings to its' relevant doc_ids to retrieve
            clusters_of_tweets = dict() #organizes doc_ids to match their postings in disc
            for q_term in query_terms_postings.keys():
                for doc_id in query_terms_postings[q_term][1].keys():
                    tweet_cluster = int(int(doc_id) / self.OPTIMAL_TWEETS_FILE_SIZE) + 1
                    if tweet_cluster not in clusters_of_tweets.keys():
                        clusters_of_tweets[tweet_cluster] = set() # no need to grab the same information for a single tweet more than once.
                    clusters_of_tweets[tweet_cluster].add(doc_id)
            # grab every relevant postings_file from disc and grab the information of it
            for tweets_postings_file_number in clusters_of_tweets.keys():
                tweets_postings_file = utils.load_obj(str(tweets_postings_file_number), self.tweets_postings_files_dir)
                for doc_id in clusters_of_tweets[tweets_postings_file_number]: #get information from postings file for every tweet
                    query_tweets_postings[doc_id] = tweets_postings_file[doc_id]
                    query_tweets_postings[doc_id].append(0)
            return query_tweets_postings
        except:
            raise ValueError

    def calculate_Wiq_vector(self,q_term_freq_dict,q_max_tf,parsed_query):
        Wiq_dict = dict()
        for q_term in parsed_query:
            if q_term in q_term_freq_dict:
                Wiq_dict[q_term] = (q_term_freq_dict[q_term] / q_max_tf)
            else:
                Wiq_dict[q_term] = 1
        return Wiq_dict


