import os

import utils
from parser_classes.URLTokenizer import URLTokenizer
from parser_classes.parser_module import Parse
from reader import ReadFile


def parser_parse_sentence_tester():
    works_properly = "45 percent 33% 8 Million #COVIDEpdemic Naor Suban marvin king_of pycharm he took the 1st place @Winner #Brad_Pit 256.9 888 Thousand 96500 from Belgium to France   24/7 100$ 1st place @Winner #Brad_Pit 256.9 888 Thousand 96500 from Belgium to France  24/7 100$ Cohen's family"
    text = "45 percent 33% 8 Million #COVIDEpdemic Naor Suban marvin king_of pycharm he took the 1st place @Winner 24/7 100$ 1st place @Winner #Brad_Pit 256.9 888 Thousand 96500 from Belgium to France 10000000000 10,000,000 70%"
    p = Parse(False)
    text_tokens = p.parse_sentence(text)
    # return text_tokens
    print(text_tokens)


def parse_URL_tester():
    full_text = 'this is the full text'
    URL = "https://www.660citynews.com/2020/07/08/feds-promise-recovery-will-focus-on-people-hurt-most-by-covid-19-economic-crisis/;https://twitter.com/i/web/status/1280947323879686145"
    URLT = URLTokenizer()
    full_text += ''.join(URLT.tokenize(URL))
    print(full_text)


def save_docs_from_parquet_to_disc():
    pass
    # r = ReadFile('Data')
    # parquetPaths = []
    # for (dirPath, dirNames, fileNames) in os.walk('Data'):
    #         for fileName in fileNames:
    #                 parquetPaths.append((dirPath + '\\' + fileName))
    #
    # # Iterate over every parquet
    # for i in range(len(parquetPaths)):
    #         parquetPaths[i] = parquetPaths[i][parquetPaths[i].find('\\') + 1:]
    #         documents_list = r.read_file(file_name=parquetPaths[i])

    # utils.save_obj(obj=docs_as_list,name='first_parquet')


def parser_parquet_test():
    p = Parse()
    docs_as_list = utils.load_obj('first_parquet')
    for document in docs_as_list:
        parsed_document = p.parse_doc(document)
        print(parsed_document)


# parser_parse_sentence_tester()
# parse_URL_tester()
# save_docs_from_parquet_to_disc()
# parser_parquet_test()

def compare_terms_indexes_in_different_parsers():
    new_terms_index = utils.load_obj('terms_index', 'D:\\Python\\IR_Project\\parser_comparison\\new_parser\\posting')
    old_terms_index = utils.load_obj('terms_index', 'D:\\Python\\IR_Project\\parser_comparison\\old_parser\\posting')
    for term in new_terms_index.keys():
        if term not in old_terms_index.keys():
            print(term)
            print(new_terms_index[term])
# compare_terms_indexes_in_different_parsers()
