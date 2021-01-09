from rankers.abstract_ranker import abstract_ranker


class mish_mash_ranker(abstract_ranker):

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
            raise TypeError('mish_mash_ranker only accepts rankers! you should be ashamed of yourself!')
        elif weight > 1 or weight < 0:
            raise ValueError('weight must be between 0 and 1')
        elif not self.ranker_to_weight_dict:  # first ranker must be weighted as 1
            weight = 1
        self.ranker_to_weight_dict[ranker] = weight
        for ranker in self.ranker_to_weight_dict.keys():
            self.ranker_to_weight_dict[ranker] *= (weight / 100)

    def rank_relevant_docs(self) -> list:
        """

        :return: a ranking taking into consideration all ranking of all rankers
        """
        tweet_id_to_final_rank = dict()
        for doc_id in self.tweets_to_rank:
            tweet_id,final_rank = self.rank_relevant_doc(doc_id)
            tweet_id_to_final_rank[tweet_id] = final_rank
        ranked_docs_as_list = self.sort_relevant_docs(tweet_id_to_final_rank)
        return ranked_docs_as_list

    def rank_relevant_doc(self, doc_id) -> (int, int):
        final_rank = 0
        for ranker in self.ranker_to_weight_dict.keys():
            tweet_id, rank = ranker.rank_relevant_doc(doc_id)
            final_rank += (rank * self.ranker_to_weight_dict[ranker])
        return tweet_id, final_rank
