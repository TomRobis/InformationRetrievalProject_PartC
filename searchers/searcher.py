import math
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
            a list of tweet_ids where the first element is the most relevant
            and the last is the least relevant result.
        """
        parsed_query = self._parser.parse_sentence(query)
        parsed_query = self.remove_irrelevant_query_terms(parsed_query) #todo added
        sigma_Wiq_squared, Wiq_dict = self.get_sigma_wiq_and_relevant_words_in_query(parsed_query)
        relevant_tweets_with_information = self.relevant_docs_from_posting(parsed_query=parsed_query)
        if not relevant_tweets_with_information:
            return 0,0
        self._ranker = Ranker(sigma_Wiq_squared,Wiq_dict,relevant_tweets_with_information)
        ranked_tweet_ids = self._ranker.rank_relevant_docs()
        return self._ranker.retrieve_top_k(ranked_tweet_ids)

    def get_sigma_wiq_and_relevant_words_in_query(self, query_as_list):
        """
        calculates tf-idf values of each term in query (currently 1) and sigma_wiq_squared.
        :param query_as_list:
        :return: tuple: (sigma_Wiq_squared - float: sigma_Wiq_squared, Wiq_dict - dict: maps term of query to tf-idf)
        """
        sigma_Wiq_squared = 0
        Wiq_dict = dict()
        for q_term in query_as_list:
            Wiq_dict[q_term] = self.calculate_tf_idf_for_q_term(q_term) #todo added
            sigma_Wiq_squared +=  math.pow(Wiq_dict[q_term],2)
        # sigma_Wiq_squared = sum(map(lambda x:,Wiq_dict.values())) #todo changed
        return sigma_Wiq_squared, Wiq_dict

    def relevant_docs_from_posting(self, parsed_query):
        """
        retrieves every relevant tweet from postings files found in disc based on terms in query.
        :param parsed_query: terms in query after parsing.
        :return: set: relevant documents matching the query's terms.
        """

        relevant_tweets = self.get_relevant_tweets(parsed_query)
        if not relevant_tweets:
            return
        return self.get_relevant_tweets_information(relevant_tweets)  # get information for each term in query

    def get_relevant_tweets(self, parsed_query):
        """
        matches every term in query that has appeared in corpus to its' relevant tweets.
        :param parsed_query:
        :return: set of relevant tweets
        """
        relevant_tweets = set()
        terms_index = self._indexer.get_terms_index()
        for q_term in parsed_query:
            set_of_relevant_docs_for_q_term = terms_index[q_term][2]
            relevant_tweets.update(set_of_relevant_docs_for_q_term)
        return relevant_tweets

    def get_relevant_tweets_information(self, relevant_tweets):
        """
        iterates over tweets postings and extracts postings of all relevant tweets.
        :param relevant_tweets: set of relevant tweets based on query's terms
        :return: postings of every relevant tweet.
        """
        relevant_tweets_information = dict()
        for i in range(self._indexer.get_tweets_postings_counter()):
            tweets_postings_file = utils.load_obj(str(i + 1), self._indexer.get_config().get_tweets_postings_path())
            for doc_id in relevant_tweets:  # todo inefficient goes over all docs every time for each postings file
                if doc_id in tweets_postings_file.keys():
                    relevant_tweets_information[doc_id] = tweets_postings_file[doc_id]
        return relevant_tweets_information

    def remove_irrelevant_query_terms(self, parsed_query): #todo added
        """
        only keeps the words out of the query that have appeared in the corpus, otherwise their inner-products are 0.
        also takes into account lower-case and upper-case forms.
        :param parsed_query:
        :return: a parsed query without terms that don't appear in the corpus
        """
        terms_index = self._indexer.get_terms_index()
        parsed_query_relevant_terms = []
        for q_term in parsed_query:
            lower_case_q_term = q_term[0].lower() + q_term[1:]
            upper_case_q_term = q_term[0].upper() + q_term[1:]
            if lower_case_q_term in terms_index.keys():
                parsed_query_relevant_terms.append(lower_case_q_term)
            elif upper_case_q_term in terms_index.keys():
                parsed_query_relevant_terms.append(upper_case_q_term)
        return parsed_query_relevant_terms

    def calculate_tf_idf_for_q_term(self, q_term): #todo added
        return 1
