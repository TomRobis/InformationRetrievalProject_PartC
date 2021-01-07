from spellchecker import SpellChecker

from query_expandors.i_query_expandor import i_query_expandor


class spell_checker(i_query_expandor):

    def __init__(self) -> None:
        self.spell_checker = SpellChecker()

    def replace_with_corrected_query(self,parsed_query):
        return [self.spell_checker.correction(p_t) for p_t in parsed_query]


