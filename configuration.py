import os

from query_expandors.thesaurus_expandor import thesaurus_expandor
from query_expandors.wordnet_expandor import wordnet_expandor


class ConfigClass:
    def __init__(self):
        # link to a zip file in google drive with your pretrained model
        self._model_url = None
        '''
        False/True flag indicating whether the testing system will download 
        and overwrite the existing model files. In other words, keep this as 
        False until you update the model, submit with True to download 
        the updated model (with a valid model_url), then turn back to False 
        in subsequent submissions to avoid the slow downloading of the large 
        model file with every submission.
        '''
        self._download_model = False

        self.corpusPath = os.path.join('data', 'benchmark_data_train.snappy.parquet')  # todo what is corpus path?
        self.savedFileMainFolder = ''  # todo which value does this have?

        self.stemming = True
        self.saveFilesWithStem = os.path.join(self.savedFileMainFolder, "WithStem")  # todo is this needed

        self.tweets_postings_path = os.path.join(self.saveFilesWithStem, 'tweet_postings')

        self.spell_checker = None
        self.query_expandor = None

        #  threshold for file sizes, relates to number of terms kept in each posting
        self.OPTIMAL_TWEETS_FILE_SIZE = 100000

        self.index_name = os.path.join(self.saveFilesWithStem, 'idx_bench.pkl')  # todo save this in curr dir or not?

        self.log_basis_for_idf = 2
        self.bm25_k = 1.2  # [1.2,2]
        self.bm25_b = 0.75
        self.rankers_weight_distribution = 0  # how much to shave off existing rankers.

        # print('Configurations were assigned successfully...')

    def get_corpusPath(self):
        return self.corpusPath

    def get_model_url(self):
        return self._model_url

    def get_download_model(self):
        return self._download_model

    def get_tweets_postings_path(self):
        return self.tweets_postings_path

    def get_tweets_postings_file_size(self):
        return self.OPTIMAL_TWEETS_FILE_SIZE

    def get_stemming_dir_path(self):
        return self.saveFilesWithStem

    def get_output_path(self):
        return self.savedFileMainFolder

    def get_log_basis_for_idf(self):
        return self.log_basis_for_idf

    def get_index_name(self):
        return self.index_name

    def get_spelling_correction(self):
        return self.spelling_correction

    def get_stemming(self):
        return self.stemming

    def get_bm25_k(self):
        return self.bm25_k

    def get_bm25_b(self):
        return self.bm25_b

    def get_rankers_weight_distribution(self):
        return self.rankers_weight_distribution

    def get_spell_checker(self):
        return self.spell_checker

    def get_query_expandor(self):
        return self.query_expandor

    def set_spell_checker(self, spell_checker):
        self.spell_checker = spell_checker

    def set_query_expandor(self, query_expandor):
        self.query_expandor = query_expandor
