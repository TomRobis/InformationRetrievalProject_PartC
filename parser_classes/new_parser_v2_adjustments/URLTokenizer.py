import re

from parser_classes.new_parser_v2_adjustments.NonTokenizingTokenizer import NonTokenizingTokenizer


class URLTokenizer(NonTokenizingTokenizer):

    def __init__(self) -> None:
        super().__init__(False)

    def tokenize(self, token) -> list:
        text = ""
        if token:
            urls = token.strip('{}').replace('https://www.', '')
            url_contents = re.split("[-/?=_&+:\s]", urls)
            for term in url_contents:
                text += ' ' + term
        return [text]