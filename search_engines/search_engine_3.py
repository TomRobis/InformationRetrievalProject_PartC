import pandas as pd

import utils
from parser_classes.parsers.parser_module import Parse
from indexers.BM25_indexer import Indexer
from searchers.BM25_searcher import Searcher
from configuration import ConfigClass


# DO NOT CHANGE THE CLASS NAME
class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse(config.get_stemming())
        self._indexer = Indexer(config)
        self._model = None

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def build_index_from_parquet(self, fn):
        """
        Reads parquet file and passes it to the parser, then indexer.
        Input:
            fn - path to parquet file
        Output:
            No output, just modifies the internal _indexer object.
        """
        df = pd.read_parquet(fn, engine="pyarrow")
        documents_list = df.values.tolist()
        # Iterate over every document in the file
        number_of_documents = 0
        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = self._parser.parse_doc(document)
            number_of_documents += 1
            # index the document data
            self._indexer.add_new_doc(parsed_document)
        print('Finished parsing and indexing. commencing post processing...')
        # make sure the postings and indexer are up to date
        self._indexer.post_process()
        print('Finished post processing.')
        # self._indexer.save_index(fn=self._indexer.get_config().get_index_name())

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        self._indexer.load_index(fn)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_precomputed_model(self, model_dir=None):
        """
        Loads a pre-computed model (or models) so we can answer queries.
        This is where you would load models like word2vec, LSI, LDA, etc. and
        assign to self._model, which is passed on to the searcher at query time.
        """
        pass

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results.
        Input:
            query - string.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relevant
            and the last is the least relevant result.
        """
        searcher = Searcher(self._parser, self._indexer, model=self._model)
        return searcher.search(query)

    def test_build_index_from_parquet(self, fn):  # todo delete when submitting
        """
        Reads parquet file and passes it to the parser, then indexer.
        Input:
            fn - path to parquet file
        Output:
            No output, just modifies the internal _indexer object.
        """
        # df = pd.read_parquet(fn, engine="pyarrow")
        # documents_list = df.values.tolist()
        # # Iterate over every document in the file
        document_1 = ['12809215422436591023', 'Wed Jul 08 17:47:48 +0000 2020', "naor asd banana tom",
                      '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}',
                      '[[117,140]]', None, None, None, None, None, None, None, None, None]
        document_2 = ['1280921542243659110', 'Wed Jul 08 17:47:48 +0000 2020',
                      "banana morty rick Baby asd BanaNa fall Ping Ball",
                      '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}',
                      '[[117,140]]', None, None, None, None, None, None, None, None, None]
        document_3 = ['1280921542243659101', 'Wed Jul 08 17:47:48 +0000 2020',
                      "Banana asd rick banana banana banana banana banana banana",
                      '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}',
                      '[[117,140]]', None, None, None, None, None, None, None, None, None]
        document_4 = ['128092154224365910222', 'Wed Jul 08 17:47:48 +0000 2020',
                      "lalala hello lalala",
                      '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}',
                      '[[117,140]]', None, None, None, None, None, None, None, None, None]
        documents_list = [document_1, document_2, document_3, document_4]
        number_of_documents = 0
        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = self._parser.parse_doc(document)
            number_of_documents += 1
            # index the document data
            self._indexer.add_new_doc(parsed_document)

            if number_of_documents == 1:
                self._indexer.dump_tweet_postings_to_disc()
        print('Finished parsing and indexing. commencing post processing...')
        self._indexer.post_process()
        print('Finished post processing.')
        # self._indexer.save_index(self._indexer.config.get_stemming_dir_path())


def main():
    config = ConfigClass()

    # create parent directories for postings
    utils.create_parent_dir(config.get_stemming_dir_path())
    utils.create_parent_dir(config.get_terms_postings_path())
    utils.create_parent_dir(config.get_tweets_postings_path())

    se = SearchEngine(config)
    se.build_index_from_parquet(config.get_corpusPath())

    n_res, res = se.search('operation lockstep rockefeller')
    print("Tweet id: {}".format(res[:1]))
