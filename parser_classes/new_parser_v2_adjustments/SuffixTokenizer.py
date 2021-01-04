from parser_classes.new_parser_v2_adjustments.NonTokenizingTokenizer import NonTokenizingTokenizer


class SuffixTokenizer(NonTokenizingTokenizer):

    def __init__(self) -> None:
        super().__init__(True)

    def tokenize(self, token, next_token) -> list:
        return [token + " " + next_token]
