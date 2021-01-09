from rankers.simple_ranker import simple_ranker


class Ranker(simple_ranker):
    def __init__(self, relevant_tweets_with_info, q_term_to_idf_dict, avg_doc_length, k, b):
        self.relevant_tweets_with_info = relevant_tweets_with_info
        self.q_term_to_idf_dict = q_term_to_idf_dict
        self.avg_doc_length = avg_doc_length
        self.k_param = k
        self.b_param = b

    def rank_relevant_doc(self, doc) -> (int, int):
        tweet_posting = self.relevant_tweets_with_info[doc]
        term_to_term_freq_dict = tweet_posting[2]
        len_of_tweet = len(term_to_term_freq_dict)
        bm25_sim_rank = 0
        for term_in_tweet in term_to_term_freq_dict.keys():
            if term_in_tweet not in self.q_term_to_idf_dict.keys():
                continue
            #todo remember to change in bm25_indexer to have term_freq_ and idf
            f_qi_D = term_to_term_freq_dict[term_in_tweet][0]  # term_freq_in_tweet
            numerator = f_qi_D * (self.k_param + 1)
            denominator = f_qi_D + (
                    self.k_param * (1 - self.b_param + (self.b_param * (len_of_tweet / self.avg_doc_length))))
            bm25_sim_rank += (self.q_term_to_idf_dict[term_in_tweet] * (numerator / denominator))

        # todo added because of mish_mash_ranker - add to config
        normalized_bm_25_sim_rank = 0.05 * bm25_sim_rank

        return tweet_posting[0], normalized_bm_25_sim_rank
