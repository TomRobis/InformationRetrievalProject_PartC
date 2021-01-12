# from os.path import  join
#
# origin = ''
# added = 'WithStem'
# combined = join(origin,added)
# print(combined)
import math

from parser_classes.parsers.parser_module import Parse
from query_expanders.thesaurus_expander import thesaurus_expander

# a = ['fuck','my','life']
# print(str1.join(a))

#
te = thesaurus_expander()
p = Parse(True)
q = 'gates implant microchips'
parsed_q = p.parse_sentence(q)
expanded_q = te.expand_query(parsed_q)

print(expanded_q)


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