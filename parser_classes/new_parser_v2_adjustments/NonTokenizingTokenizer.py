class NonTokenizingTokenizer:

    def __init__(self):
        self.uses_next_token = False

    def tokenize(self, token=None, next_token=None) -> list:
        pass

    def uses_next_token(self):
        return self.uses_next_token()
