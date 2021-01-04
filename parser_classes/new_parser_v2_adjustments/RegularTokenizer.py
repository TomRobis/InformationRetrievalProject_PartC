from parser_classes.new_parser_v2_adjustments.NonTokenizingTokenizer import NonTokenizingTokenizer


class RegularTokenizer(NonTokenizingTokenizer):

    def __init__(self) -> None:
        super().__init__(False)

    def tokenize(self, token, next_token) -> list:
        return token
