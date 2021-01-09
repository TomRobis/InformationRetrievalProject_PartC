from spellchecker import SpellChecker


class spell_checker:

    def __init__(self) -> None:
        self.spell_checker = SpellChecker()

    def replace_with_corrected_query(self, parsed_query):
        return [self.spell_checker.correction(p_t) for p_t in parsed_query]
