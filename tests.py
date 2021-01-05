import re


# print(re.match("^[A-Za-z0-9]*$", "$"))
# print(re.match("^[A-Za-z0-9]*$", "'"))
# print(re.match("^[A-Za-z0-9]*$", ".26%"))
from parser_classes import parser_module
#
# sen = ['2.109k']
# concat_sen = sen + ['doggy']
# print(concat_sen)
# # p = parser_module.Parse()
# # parsed_sen = p.parse_sentence(sen)
# # print(parsed_sen)
#
# print('@'.islower())

a = set()
b = set()
a.add('c')
b.add('c')
print(any(i in a for i in b))