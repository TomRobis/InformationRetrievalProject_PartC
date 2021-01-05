import pandas as pd

import utils
from parser_classes.parser_module import Parse
from indexer import Indexer
from searcher import Searcher
from reader import ReadFile
from configuration import ConfigClass


# DO NOT CHANGE THE CLASS NAME
class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse()
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
        print('Finished parsing and indexing.')
        self._indexer.post_process()
        # todo add entity processing and big - small words processing and whatever else is needed before saving
        # self._indexer.save_index(self._indexer.config.get_stemming_dir_path())
        print('lalala')

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        self._indexer.load_index(self._indexer.config.get_stemming_dir_path())

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
            a list of tweet_ids where the first element is the most relavant 
            and the last is the least relevant result.
        """
        searcher = Searcher(self._parser, self._indexer, model=self._model)
        return searcher.search(query)


def main():
    config = ConfigClass()

    # create parent directories for postings
    utils.create_parent_dir(config.get_stemming_dir_path())
    utils.create_parent_dir(config.get_terms_postings_path())
    utils.create_parent_dir(config.get_tweets_postings_path())

    se = SearchEngine(config)
    se.build_index_from_parquet(config.get_corpusPath())
    # se.load_index?
    # if num_docs_to_retrieve > 2000:
    #     num_docs_to_retrieve = 2000

    #  now answering queries given.
    answers_tuples = []
    # for i in range(len(queries)):
    n_res,res = se.search('Gates')
    print("Tweet id: {}".format(res))
    #         # doc_posting.append(i+1)
    #         # answers_tuples.append(doc_posting)

    # IO_handler.write_answers_to_csv(answers_tuples,'results.csv')
