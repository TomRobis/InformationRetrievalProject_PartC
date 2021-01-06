from parser_classes.parser_module import Parse
def test_create_term_doc_dict(list_of_tokens):
    p = Parse()
    term_doc_dict = p.create_term_doc_dict(list_of_tokens)
    return term_doc_dict



document_1 = ['1280921542243659111', 'Wed Jul 08 17:47:48 +0000 2020', "Banana morty Ball ping Call bing Call", '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}', '[[117,140]]', None, None, None, None, None, None, None, None, None]
document_2 = ['1280921542243659110', 'Wed Jul 08 17:47:48 +0000 2020', "banana Banana morty rick Baby BanaNa fall Ping Ball", '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}', '[[117,140]]', None, None, None, None, None, None, None, None, None]
documents_list = [document_1,document_2]