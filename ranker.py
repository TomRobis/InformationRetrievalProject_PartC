import math


class Ranker:
    def __init__(self, relevant_tweets, query_terms_dict, num_of_docs_in_corpus, Wiq_dict):
        self.relevant_tweets = relevant_tweets  # doc_id -> tweet_id, tweet_date, max_tf, unique words, inner_product
        self.query_terms = query_terms_dict  # term -> df and term_tweet_dic
        self.num_of_docs_in_corpus = num_of_docs_in_corpus  # N
        self.Wiq_vector = Wiq_dict # q_term -> Wiq

    def rank_relevant_docs(self):
        for q_term in self.query_terms.keys():  # for every term in query (only ones relevant to every doc)
            q_term_tweet_dict = self.query_terms[q_term][1]  # q_term -> freq in document
            for doc_id in q_term_tweet_dict.keys():  # for every doc the q_term has appeared in
                doc_postings = self.relevant_tweets[doc_id]  # tweet_id, tweet_date, max_tf, unique words, Wij
                if not doc_postings:
                    continue
                max_tf = doc_postings[2]
                # add q_term W to inner product of doc
                self.relevant_tweets[doc_id][4] += self.Wiq_mul_wij(doc_id,q_term,max_tf)
        ranked_docs_list_of_lists = list(self.relevant_tweets.values())
        ranked_docs_list_of_lists.sort(key=lambda x: x[4], reverse=True)
        return ranked_docs_list_of_lists


    def tf_idf(self, term_freq_doc, max_tf, df):
        try:
            return (term_freq_doc / max_tf) * math.log2(self.num_of_docs_in_corpus / df)
        except:
            raise ValueError()

    def retrieve_top_k(self,sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]

    def Wiq_mul_wij(self, doc_id, q_term, doc_max_tf):
            tf_idf = self.tf_idf(self.query_terms[q_term][1][doc_id],doc_max_tf,self.query_terms[q_term][0])
            Wiq = self.Wiq_vector[q_term]
            return  tf_idf * Wiq
        # term_freq_in doc, doc_max_tf,df,Wiq
