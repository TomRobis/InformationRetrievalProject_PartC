
#     docs_list = [
#         ['1280921542243659111', 'Wed Jul 08 17:47:48 +0000 2020', 'Hello guys Guys alpha gUys banana GUYS good luck', '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}', '[[117,140]]', None, None, None, None, None, None, None, None, None],
#         ['1280921542243659222', 'Wed Jul 08 17:47:48 +0000 2020', 'Dana @sdklfs forever Forever King David HELLO from the other side', '{"https://t.co/4A5TDSyjoY":"https://twitter.com/i/web/status/1280921542243659776"}', '[[117,140]]', None, None, None, None, None, None, None, None, None]
#                 ]
import math


ranked_docs_list_of_lists = {222:3,223:40}
print({v for k, v in sorted(ranked_docs_list_of_lists.items(), key=lambda item: item[1])})