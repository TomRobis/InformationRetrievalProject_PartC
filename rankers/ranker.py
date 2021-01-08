import math


class Ranker:
    def __init__(self, sigma_Wiq_squared, Wiq_dict, relevant_tweets_with_information):
        self.sigma_Wiq_squared = sigma_Wiq_squared
        self.Wiq_dict = Wiq_dict
        self.relevant_tweets_with_info = relevant_tweets_with_information

    def rank_relevant_docs(self):
        """
        calculates cos-sim for every tweet in relevant tweets received from searcher.

        :return: list: of tweet ids sorted by descending cos-sim.
        """
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

    def retrieve_top_k(self, sorted_relevant_doc, k=250):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return k, sorted_relevant_doc[:k]
