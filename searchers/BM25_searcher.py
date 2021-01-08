import math
import utils
from rankers import BM25_ranker


class Searcher:

    def __init__(self, parser, indexer, model):
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
        parsed_query = self.remove_irrelevant_query_terms(parsed_query)
        qterm_to_idf_dict = self.get_qterm_to_idf_dict(parsed_query)
        relevant_tweets_with_information = self.relevant_docs_from_posting(parsed_query=parsed_query)
        if not relevant_tweets_with_information:
            return 0, 0
        self._ranker = BM25_ranker.BM25_ranker(relevant_tweets_with_information, qterm_to_idf_dict,
                                               avg_doc_length=self._indexer.get_average_doc_length(),
                                               k=self.config.get_bm25_k(), b=self.config.get_bm25_b())
        ranked_tweet_ids = self._ranker.rank_relevant_docs()
        return self._ranker.retrieve_top_k(ranked_tweet_ids)

    def relevant_docs_from_posting(self, parsed_query):
        """
        retrieves every relevant tweet from postings files found in disc based on terms in query.
        :param parsed_query: terms in query after parsing.
        :return: set: relevant documents matching the query's terms.
        """

        relevant_tweets = self.get_relevant_tweets(parsed_query)
        if not relevant_tweets:
            return
        return self.get_relevant_tweets_postings(relevant_tweets)  # get information for each term in query

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

    def get_relevant_tweets_postings(self, relevant_tweets):
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

    def remove_irrelevant_query_terms(self, parsed_query):
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

    def get_qterm_to_idf_dict(self, parsed_query):
        q_term_to_idf = dict()
        N = self._indexer.get_doc_id()  # num_of_tweets_in_corpus
        terms_index = self._indexer.get_terms_index()
        for q_term in parsed_query:
            n_qi = terms_index[q_term][0]  # df
            numerator = N - n_qi + 0.5
            denominator = n_qi + 0.5
            q_term_to_idf[q_term] = (math.log((numerator / denominator) + 1))
        return q_term_to_idf
