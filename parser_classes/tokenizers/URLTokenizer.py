import re

from parser_classes.tokenizers.iTokenizer import iTokenizer


class URLTokenizer(iTokenizer):

    def tokenize(self, token) -> list:
        text = ""
        if token:
            urls = token.strip('{}').replace('https://www.', '')
            url_contents = re.split("[-/?=_&+:\s]", urls)
            for term in url_contents:
                text += ' ' + term
        return [text]