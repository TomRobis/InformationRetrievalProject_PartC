import math

from rankers.simple_ranker import simple_ranker


class Ranker(simple_ranker):
    def __init__(self, sigma_Wiq_squared, Wiq_dict, relevant_tweets_with_information):
        self.sigma_Wiq_squared = sigma_Wiq_squared
        self.Wiq_dict = Wiq_dict
        self.relevant_tweets_with_info = relevant_tweets_with_information

    def rank_relevant_doc(self, doc) -> (int, int):
        inner_product_for_tweet = 0
        tweet_posting = self.relevant_tweets_with_info[doc]
        term_to_Wij_dict = tweet_posting[2]
        for term_in_tweet in term_to_Wij_dict.keys():
            if term_in_tweet not in self.Wiq_dict.keys():
                continue
            # todo remember to change in bm25_indexer to have term_freq_ and idf
            inner_product_for_tweet += (term_to_Wij_dict[term_in_tweet][1] * self.Wiq_dict[term_in_tweet])
        cos_sim_denominator = (math.sqrt(self.sigma_Wiq_squared * tweet_posting[1]))
        cos_sim = (inner_product_for_tweet / cos_sim_denominator) if cos_sim_denominator != 0 else 0
        return tweet_posting[0], cos_sim  # tweet_id, rank of tweet
