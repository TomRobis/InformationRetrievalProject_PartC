from rankers.abstract_ranker import abstract_ranker


class simple_ranker(abstract_ranker):

    def rank_relevant_docs(self) -> list:
        """
        calculates cos-sim for every tweet in relevant tweets received from searcher.
        :return: list: of tweet ids sorted by descending cos-sim.
        """
        tweet_id_to_rank = dict()
        for tweet in self.relevant_tweets_with_info.keys():
            tweet_id, rank = self.rank_relevant_doc(tweet)
            tweet_id_to_rank[tweet_id] = rank
        tweets_sorted_by_rank_list = self.sort_relevant_docs(tweet_id_to_rank)
        return tweets_sorted_by_rank_list


