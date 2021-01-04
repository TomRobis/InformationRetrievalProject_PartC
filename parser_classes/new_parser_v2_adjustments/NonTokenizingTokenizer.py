class NonTokenizingTokenizer:

    def __init__(self, uses_next_token):
        self.uses_next_token = uses_next_token

    def tokenize(self, token=None, next_token=None) -> list:
        pass

    def uses_next_token(self):
        return self.uses_next_token()
