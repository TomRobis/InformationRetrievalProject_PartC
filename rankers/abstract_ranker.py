from abc import ABC, abstractmethod


class abstract_ranker(ABC):

    @abstractmethod
    def rank_relevant_docs(self) -> list:
        pass

    @abstractmethod
    def rank_relevant_doc(self,tweet) -> (int, int):  # tweet_id, rank
        """

        :rtype: object
        """
        pass

    def retrieve_top_k(self, sorted_relevant_doc, k=250):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """

        return k, sorted_relevant_doc[:k]

    def sort_relevant_docs(self, tweet_id_to_rank):
        return [k for k, v in sorted(tweet_id_to_rank.items(), key=lambda item: item[1], reverse=True)]
