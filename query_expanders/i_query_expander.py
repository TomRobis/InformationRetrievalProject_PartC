from abc import ABC, abstractmethod


class i_query_expander(ABC):

    @abstractmethod
    def expand_query(self, parsed_query) -> dict:
        """
        interface for query expansion classes.
        :param parsed_query:
        :return:
        """
        pass
