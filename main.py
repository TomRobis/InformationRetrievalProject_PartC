import search_engine_best


corpus_path = 'data\\benchmark_data_train.snappy.parquet'
output_path = 'posting'
stemming = False
next_queries =  ['covid','trump','moderna','pfizer','boris johnson']
queries = ['covid']
num_doc_to_retrieve = 10


if __name__ == '__main__':
    search_engine_best.main(corpus_path=corpus_path, output_path=output_path, stemming=stemming, queries=queries, num_docs_to_retrieve = num_doc_to_retrieve)
