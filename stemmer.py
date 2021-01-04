from nltk import PorterStemmer


class Stemmer:
    def __init__(self):
        self.ps = PorterStemmer()

    def stem_term(self, token):
        """
        This function stem a token
        :param token: string of a token
        :return: stemmed token
        """

        return self.ps.stem(token[0])

    def porter_stemmer(self, terms_list):

        index = 0
        for w in terms_list:
            new_stem = self.stem_term(w)
            if new_stem != w[0]:
                terms_list[index] = (new_stem, terms_list[index][1])
            index += 1
        return terms_list