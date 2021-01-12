import unicodedata


def write_list_to_text_file(file_path,target_list):
    """
    converts list to string and writes to text file, with spaces between each entry.
    :param file_path:
    :param target_list:
    :return:
    """
    text_file = open(file_path, "w",encoding='utf-8')
    text_file.write(convert_list_to_string(target_list))
    text_file.close()


def read_tid_from_txt(f_path):
    f = open("D:\\Python\\IR_Project\\Part_C\\data\\q10\\q12478_top_5.txt", "r")
    return f.read()

def convert_string_to_list(some_string):
    return list(some_string.split(" "))

def convert_list_to_string(some_list):
    str1 = ' '
    return str1.join(some_list)


def init_modulu_to_query_num_dict():
    modulu_to_query_num = dict()
    modulu_to_query_num[0] = '1'
    modulu_to_query_num[1] = '2'
    modulu_to_query_num[2] = '4'
    modulu_to_query_num[3] = '7'
    modulu_to_query_num[4] = '8'
    return modulu_to_query_num


def get_rank_as_str(idx_of_tweet):
    to_ret = idx_of_tweet % 5 + 1
    return to_ret

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')





# code for parser in parse_doc
# todo q10
# try:
#     idx_of_tweet = self.tweet_ids.index(str(tweet_id))
#     self.queries_and_full_text += ('tweet_id: ' + str(tweet_id) + '\n')
#     self.queries_and_full_text += ('query_num: ' + self.modulu_to_query_num_dict[math.floor(idx_of_tweet / 5)] + '\n')
#     self.queries_and_full_text += 'rank: '
#     self.queries_and_full_text += str(q10.get_rank_as_str(idx_of_tweet))
#     self.queries_and_full_text += '\n'
#     self.queries_and_full_text += ('full_text: ' + full_text + '\n\n')
# except:
#     return

#code for parser in constructor
# # todo q10
# self.tweet_ids = q10.read_tid_from_txt('D:\\Python\\IR_Project\\Part_C\\data\\q10\\q12478_top_5.txt')
# self.tweet_ids = q10.convert_string_to_list(self.tweet_ids)  # tweets ids as list
# self.modulu_to_query_num_dict = q10.init_modulu_to_query_num_dict()
# self.queries_and_full_text = ''


#code for search_engine - build index from parquet.
# # todo q10
# print(self._parser.queries_and_full_text)
# # q10.write_list_to_text_file('D:\\Python\\IR_Project\\Part_C\\data\\q10\\queries_with_full_text.txt',self._parser.queries_and_full_text )
# sys.exit(-1)


#code for search_engine

# def main():
#
#     config = ConfigClass()
#
#     se = SearchEngine(config)
#     se.build_index_from_parquet(config.get_corpusPath())
    # results_in_line = []
    # queries = pd.read_csv(os.path.join('data', 'queries_train.tsv'), sep='\t')
    # for i, row in queries.iterrows():
    #     q_id = row['query_id']
    #     q_keywords = row['keywords']
    #     q_n_res, q_res = se.search(q_keywords)
    #     # results_in_line.append('q_id: ' + str(q_id) + ' ')
    #     results_in_line += q_res
    #     q_res.append('\n')
    #
    # q10.write_list_to_text_file('D:\\Python\\IR_Project\\Part_C\\data\\q10\\q12478_top_5.txt',results_in_line)