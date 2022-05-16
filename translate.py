# from trans_tools import command_mode
from utils.settings import *
import requests
import argparse
from hashlib import md5
import random
from utils import *
from utils.api import *
import sys






# def translate():
#     args = get_args()


#     query = args.target_words
#     if query[0] == '0':
#         command_mode()
#         return

#     if args.c:
#         lang = CONFIG.config['from_lang']
#         to = CONFIG.config['to_lang']

#     elif is_contains_chinese(query):
#         lang = 'zh'
#         to = 'en'

#     else:
#         lang = args.lang
#         to = args.to_lang

#     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#     salt = get_salt()
#     params = {
#         'appid': CONFIG.config['appid'],
#         'q': query,
#         'from': lang,
#         'to': to,
#         'salt': salt,
#         'sign': make_md5(CONFIG.config['appid'] + query + salt + CONFIG.config['appkey'])
#     }
#     rjson = {}

#     try:
#         rjson = get_trans(params=params, headers=headers)
#     except Exception as e:
#         if DEBUG:
#             print(e)
#         print("\033[0;31;mSomething has gone Wrong! Probably due to your NetWork Status.\033[0m")
#     try:
#         parse_res_json(rjson)

#         with open(HISTORY, "r+", encoding="utf-8") as file:
#             history = json.load(file)
#             history['history'].append(rjson)
#             file.seek(0)
#             json.dump(history, file, indent=4, ensure_ascii=False)

#     except FileNotFoundError as e:
#         with open(HISTORY, "w", encoding="utf-8") as file:
#             history = {
#                 'history': []
#             }
#             history['history'].append(rjson)
#             file.seek(0)
#             json.dump(history, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # translate()
    pass
