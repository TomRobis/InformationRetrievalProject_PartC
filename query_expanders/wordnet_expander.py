from nltk.corpus import wordnet

from query_expanders.i_query_expander import i_query_expander


class wordnet_expander(i_query_expander):

    def expand_query(self,parsed_query) -> list:
        """
        expands query based on wordnet package.
        :param parsed_query:
        :return:
        """
        words_added_to_query = []
        for term in parsed_query:
            syn_sets = self.get_syn_sets(term)
            if syn_sets:
                words_added_to_query += self.collect_syns_to_expand_query(syn_sets)
        return words_added_to_query + parsed_query

    def get_syn_sets(self,word):
        """
        collecting only the first synset.
        :param word: term to get synset of
        :return:a single synset of said word.
        """
        return wordnet.synsets(word)


    def collect_syns_to_expand_query(self,syn_set):
            """
            currently only expands with the "best candidate" for each term in query
            :param syn_set: SynSet object of all synonyms of a certain word that has appeared in the query
            :return: list of all synonym of said word
            """
            return syn_set[0].lemma_names()
