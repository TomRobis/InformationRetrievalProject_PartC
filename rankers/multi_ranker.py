from rankers.abstract_ranker import abstract_ranker


class Ranker(abstract_ranker):

    def __init__(self, tweets_to_rank_as_set):
        self.ranker_to_weight_dict = dict()
        self.tweets_to_rank = tweets_to_rank_as_set

    def add_ranker(self, ranker, weight):
        """
        sum of weights is equal to one. weight must be a value between 0 and 1
        when a new ranker enters, every ranker contributes a fair share of its' rank to the new ranker.
        :param ranker: a ranker of abstract_ranker type
        :param weight: importance of ranker's value in rating the query
        :return:
        """
        if not isinstance(ranker, abstract_ranker):
            print('mish_mash_ranker only accepts rankers! you should be ashamed of yourself!')
            return
        elif weight > 1 or weight <= 0:
            # print('mish_mash_ranker only accepts rankers with weighting in range (0,1]. it is not added!')
            return
        elif not self.ranker_to_weight_dict:  # first ranker must be weighted as 1
            weight = 1
        elif weight == 1:  # if a ranker wants all the weight, the rest are removed.
            self.ranker_to_weight_dict.clear()
        else:  # not the first weighting.
            for existing_ranker in self.ranker_to_weight_dict.keys():
                self.ranker_to_weight_dict[existing_ranker] -= (self.ranker_to_weight_dict[existing_ranker] * weight)
        self.ranker_to_weight_dict[ranker] = weight

    def rank_relevant_docs(self) -> list:
        """

        :return: a ranking taking into consideration all ranking of all rankers
        """
        tweet_id_to_final_rank = dict()
        for doc_id in self.tweets_to_rank:
            tweet_id, final_rank = self.rank_relevant_doc(doc_id)
            tweet_id_to_final_rank[tweet_id] = final_rank
        ranked_docs_as_list = self.sort_relevant_docs(tweet_id_to_final_rank)
        return ranked_docs_as_list

    def rank_relevant_doc(self, doc_id) -> (int, int):
        final_rank = 0
        for ranker in self.ranker_to_weight_dict.keys():
            tweet_id, rank = ranker.rank_relevant_doc(doc_id)
            final_rank += (rank * self.ranker_to_weight_dict[ranker])
        return tweet_id, final_rank
