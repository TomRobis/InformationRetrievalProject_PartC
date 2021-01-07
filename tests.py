#     docs_list = [
#         ['1280921542243659111', 'Wed Jul 08 17:47:48 +0000 2020', 'Hello guys Guys alpha gUys banana GUYS good luck', '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}', '[[117,140]]', None, None, None, None, None, None, None, None, None],
#         ['1280921542243659222', 'Wed Jul 08 17:47:48 +0000 2020', 'Dana @sdklfs forever Forever King David HELLO from the other side', '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}', '[[117,140]]', None, None, None, None, None, None, None, None, None]
#                 ]
import math

from nltk.corpus import wordnet
synonyms = []
antonyms = []

syn = wordnet.synsets("covid")
print(syn[0].lemma_names()[0])
    # for l in syn.lemmas():
    #     synonyms.append(l.name())
    #     if l.antonyms():
    #         antonyms.append(l.antonyms()[0].name())



print(set(synonyms))
print(set(antonyms))


