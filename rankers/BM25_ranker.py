import math


class BM25_ranker:
    def __init__(self, relevant_tweets_with_info, q_term_to_idf_dict, avg_doc_length, k, b):
        self.relevant_tweets_with_info = relevant_tweets_with_info
        self.q_term_to_idf_dict = q_term_to_idf_dict
        self.avg_doc_length = avg_doc_length
        self.k_param = k
        self.b_param = b

    def rank_relevant_docs(self):
        """
        calculates cos-sim for every tweet in relevant tweets received from searcher.

        :return: list: of tweet ids sorted by descending cos-sim.
        """
        tweet_id_to_rank = dict()
        for tweet in self.relevant_tweets_with_info.keys():
            tweet_posting = self.relevant_tweets_with_info[tweet]
            term_to_term_freq_dict = tweet_posting[2]
            len_of_tweet = len(term_to_term_freq_dict)
            bm25_sim_rank = 0
            for term_in_tweet in term_to_term_freq_dict.keys():
                if term_in_tweet not in self.q_term_to_idf_dict.keys():
                    continue
                f_qi_D = term_to_term_freq_dict[term_in_tweet]  # term_freq_in_tweet
                numerator = f_qi_D * (self.k_param + 1)
                denominator = f_qi_D + (
                            self.k_param * (1 - self.b_param + (self.b_param * (len_of_tweet / self.avg_doc_length))))
                bm25_sim_rank += (self.q_term_to_idf_dict[term_in_tweet] * (numerator / denominator))
            tweet_id_to_rank[tweet_posting[0]] = bm25_sim_rank  
        return [k for k, v in sorted(tweet_id_to_rank.items(), key=lambda item: item[1], reverse=True)]

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]
