from parser_classes.parser_module import Parse
def test_create_term_doc_dict(list_of_tokens):
    p = Parse()
    term_doc_dict = p.create_term_doc_dict(list_of_tokens)
    return term_doc_dict

list_of_tokens = ['banana','Banana','morty','rick','Baby']
term_doc_dict_tested = test_create_term_doc_dict(list_of_tokens)
print(term_doc_dict_tested)