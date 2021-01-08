from query_expandors.i_query_expandor import i_query_expandor
from nltk.corpus import lin_thesaurus as thes

class thesaurus_expandor(i_query_expandor):

    def expand_query(self, parsed_query) -> list:
        """
        expands query based on synonyms given from thesaurus package.
        :param parsed_query:
        :return:
        """
        terms_from_expansion = []
        for term in parsed_query:
            scored = thes.scored_synonyms(term)[1][1]
            terms_from_expansion += [k for k, v in sorted(scored, key=lambda item: item[1], reverse=True)][:17]
        return terms_from_expansion + parsed_query
