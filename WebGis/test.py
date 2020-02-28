# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebGisApp.settings")
# django.setup()
#
# from WebGis.models import *
#
#
# def test(string):
#     rez = []
#     try:
#         int(string)
#         bazna = Bazne.objects.filter(cell_id__startswith=string)  # cell_id is a string
#         if len(bazna)>0:
#             rez = bazna[0].cell_id
#     except ValueError:
#         bazna = Bazne.objects.filter(name__icontains=string)
#         if len(bazna) > 0:
#             rez = bazna[0].name
#
#     return(rez)
#
# # try:
# #     val = int('sbc')
# #     print('val')
# # except ValueError:
# #     print('VE')
#
# print(test('9999'))


# S = '12345678912345'
# rng = range(len(S))
# val = 'val'
# idx = 'idx'
# n = [[{val: '', idx: []},]]
# combinations = []
#
#
# # n.append([{val:S[i], idx:[i]} for i in rng])
# # combinations+=n
#
# print(n)
# for _ in range(1, 3):
#     for comb in n[-1]:
#         print('comb',type(comb))
#         rez = [{val: comb[val] + S[i], idx: comb[idx] + [i]} for i in rng if i not in comb[idx]]
#         n.append(rez)
#         # print(rez)
#         # time.sleep(90)
#     # print(comb)
#
#     # n[-2].pop()
#     combinations.extend(n[-1])
#
# print(n)

import asn1

path = 'C:\\WorkPy\\asn\\N1'
decoder = asn1.Decoder()

with open(path, 'rb') as f:
    asn_data = f.read()

decoder.start(asn_data)
tag, value = decoder.read()