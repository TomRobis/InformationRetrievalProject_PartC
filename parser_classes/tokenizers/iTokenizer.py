from abc import ABC, abstractmethod


class iTokenizer(ABC):
    @abstractmethod
    def tokenize(self, token=None, next_token=None) -> list:
        pass
