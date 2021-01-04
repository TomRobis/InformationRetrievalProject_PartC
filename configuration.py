import os


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

        self.corpusPath = os.path.join('data', 'benchmark_data_train.snappy.parquet')
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "WithStem"
        # self.saveFilesWithoutStem = self.savedFileMainFolder + "\\WithoutStem"
        self.toStem = True

        self.terms_postings_path = self.saveFilesWithStem + "\\term_postings"
        self.tweets_postings_path = self.saveFilesWithStem + "\\tweet_postings"
        #  threshold for file sizes, relates to number of terms kept in each posting
        self.OPTIMAL_TERMS_FILE_SIZE = 100000
        self.OPTIMAL_TWEETS_FILE_SIZE = 100000

        print('Project was created successfully..')

    def get_corpusPath(self):
        return self.corpusPath

    def get_model_url(self):
        return self._model_url

    def get_download_model(self):
        return self._download_model

    def get_terms_postings_path(self):
        return self.terms_postings_path

    def get_tweets_postings_path(self):
        return self.tweets_postings_path

    def get_terms_postings_file_size(self):
        return self.OPTIMAL_TERMS_FILE_SIZE

    def get_tweets_postings_file_size(self):
        return self.OPTIMAL_TWEETS_FILE_SIZE

    def get_stemming_dir_path(self):
        return self.saveFilesWithStem

    def get_output_path(self):
        return self.savedFileMainFolder
