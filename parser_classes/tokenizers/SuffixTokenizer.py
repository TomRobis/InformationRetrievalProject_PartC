from parser_classes.tokenizers.iTokenizer import iTokenizer


class SuffixTokenizer(iTokenizer):

    def tokenize(self, token, next_token) -> list:
        return [token + " " + next_token]
