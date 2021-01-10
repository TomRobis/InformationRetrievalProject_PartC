# from os.path import  join
#
# origin = ''
# added = 'WithStem'
# combined = join(origin,added)
# print(combined)
from parser_classes.parsers.parser_module import Parse
from query_expanders.thesaurus_expander import thesaurus_expander

# a = ['fuck','my','life']
# print(str1.join(a))

#
# te = thesaurus_expander()
# p = Parse(True)
# q = 'gates implant microchips'
# parsed_q = p.parse_sentence(q)
# expanded_q = te.expand_query(parsed_q)
#
# print(expanded_q)

# query_num,rank,key_words,full_text,
# results = []
# queries = pd.read_csv(os.path.join('data', 'queries_train.tsv'), sep='\t')
# for i, row in queries.iterrows():
#     q_id = row['query_id']
#     q_keywords = row['keywords']
#     q_n_res, q_res = se.search(q_keywords)
#     q_res.append('\n')
#     results += q_res