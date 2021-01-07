import math


class Ranker:
    def __init__(self, sigma_Wiq_squared, Wiq_dict, relevant_tweets_with_information):
        self.sigma_Wiq_squared = sigma_Wiq_squared
        self.Wiq_dict = Wiq_dict
        self.relevant_tweets_with_info = relevant_tweets_with_information

    def rank_relevant_docs(self):
        tweet_id_to_cos_sim = dict()
        for tweet in self.relevant_tweets_with_info.keys():
            inner_product_for_tweet = 0
            tweet_posting = self.relevant_tweets_with_info[tweet]
            term_to_Wij_dict = tweet_posting[2]
            for term_in_tweet in term_to_Wij_dict.keys():
                if term_in_tweet not in self.Wiq_dict.keys():
                    continue
                inner_product_for_tweet += (term_to_Wij_dict[term_in_tweet] * self.Wiq_dict[term_in_tweet])
            cos_sim_denominator = (math.sqrt(self.sigma_Wiq_squared * tweet_posting[1]))
            cos_sim = (inner_product_for_tweet / cos_sim_denominator) if cos_sim_denominator != 0 else 0
            tweet_id_to_cos_sim[tweet_posting[0]] = cos_sim  # tweet_id to cos-sim
        return [k for k, v in sorted(tweet_id_to_cos_sim.items(), key=lambda item: item[1],reverse=True)]

    def retrieve_top_k(self, sorted_relevant_doc, k=500):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return k, sorted_relevant_doc[:k]

    def Wiq_mul_wij(self, doc_id, q_term, doc_max_tf):
        tf_idf = self.tf_idf(self.query_terms[q_term][1][doc_id], doc_max_tf, self.query_terms[q_term][0])
        Wiq = self.Wiq_vector[q_term]
        return tf_idf * Wiq
    # term_freq_in doc, doc_max_tf,df,Wiq
