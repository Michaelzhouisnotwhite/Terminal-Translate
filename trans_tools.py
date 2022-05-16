import random

import requests
from utils import *
from utils.api import *


class TranslateTools:
    class TransResult:
        fl = None
        tl = None
        trans = None

        def __init__(self, rjson) -> None:
            try:
                self.fl = rjson['from']
                self.tl = rjson['to']
                self.trans = rjson["trans_result"]

            except KeyError as e:
                if DEBUG:
                    print(e)

                print("\033[0;31;mSomething has gone Wrong! Probably due to your NetWork Status.\033[0m")

        def format_show(self):
            res = ''
            for idx, tran in enumerate(self.trans):
                dst = tran['dst']
                if len(self.trans) ==1:
                    format_line = f'\33[36m[{self.fl}-{self.tl}]\33[0m \33[32m{dst}\33[0m'
                else:
                    format_line = f''
                if idx == len(self.trans) - 1:
                    res += format_line
                else:
                    res += format_line + '\n'

            return res

    def __init__(self, appid: str, appkey: str) -> None:
        self.appid = appid
        self.appkey = appkey
        self.history_tool = HistoryTool()
        pass

    def translate(self, source: str, fl='auto', tl="zh", record=False):
        """
        translate word

        Args:
            source (str): words to be translate
            record (bool, optional): Is the word write in history. Defaults to False.
            fl (str): from language. Defaults to 'auto'
            tl (str): to language. Defaults to 'zh'
        """
        salt = get_salt()
        sign = make_md5(self.appid + source + salt + self.appkey)
        payload = {
            'appid': self.appid,
            'q': source,
            'from': fl,
            'to': tl,
            'salt': salt,
            'sign': sign
        }
        rjson = get_trans(params=payload)
        if record:
            self.history_tool.write(rjson)
        return self.TransResult(rjson)


# def display_history():
#     with open('history.json', 'r', encoding='utf-8') as file:
#         history = json.load(file)
#     for his in history["history"]:
#         from_lang = his['from']
#         to_lang = his['to']
#         origin = his["trans_result"][0]['src']
#         trans = his["trans_result"][0]['dst']
#         print(f'From:\33[35m{from_lang}\33[0m')
#         print(f'To:\33[36m{to_lang}\33[0m')
#         print(f'Origin:\33[32m{origin}\33[0m')
#         print(f'Translation:\33[34m{trans}\33[0m')
#         print('\n')


# def display_language_table():
#     with open(LANG_TABLE, 'r', encoding='utf-8') as file:
#         lang_tb = file.read()
#     print(lang_tb)


# def clear_history():
#     with open('history.json', 'r', encoding='utf-8') as file:
#         history = json.load(file)
#         history["history"].clear()

#     with open('history.json', 'w', encoding='utf-8') as file:
#         json.dump(history, file, indent=4, ensure_ascii=False)

#     print('\33[32mHistory has been cleared!\33[0m')


# hashed_function = {
#     "lang": set_language,
#     "langtb": display_language_table,

#     "disp": display_history,
#     "clr": clear_history,
# }


# def command_mode():
#     with open(WELCOME, 'r') as file:
#         welcome = file.read()
#     print(welcome)
#     while True:
#         config = CONFIG.config
#         status = config['from_lang'] + '-' + config['to_lang']
#         query = input(f"({status}) > ")

#         if not query:
#             continue
#         if query[0] == '@':
#             if len(query) > 1:
#                 cmd = query[1:].split()

#             else:
#                 continue
#             if cmd[0] == 'exit':
#                 break
#             try:
#                 hashed_function[cmd[0]](*cmd[1:])
#             except Exception as e:
#                 if DEBUG:
#                     print(e)
#                 print(
#                     '\033[0;31;40mNot supported function! Please try again!\033[0m')
#         else:
#             salt = get_salt()
#             sign = make_md5(config['appid'] + query +
#                             salt + config['appkey'])
#             headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#             payload = {'appid': config['appid'], 'q': query, 'from': config['from_lang'],
#                        'to': config['to_lang'], 'salt': salt, 'sign': sign}

#             rjson = {}
#             try:
#                 rjson = get_trans(params=payload, headers=headers)
#             except Exception as e:

#                 if DEBUG:
#                     print(e)
#                 print(
#                     "\033[0;31;40mSomething has gone Wrong! Probably due to your NetWork Status.\033[0m")

#             try:
#                 parse_res_json(rjson)

#                 with open(HISTORY, "r+", encoding="utf-8") as file:
#                     history = json.load(file)
#                     history['history'].append(rjson)
#                     file.seek(0)
#                     json.dump(history, file, indent=4, ensure_ascii=False)

#             except FileNotFoundError as e:
#                 with open(HISTORY, "w", encoding="utf-8") as file:
#                     history = {
#                         'history': []
#                     }
#                     history['history'].append(rjson)
#                     file.seek(0)
#                     json.dump(history, file, indent=4, ensure_ascii=False)

#             except Exception as e:
#                 if DEBUG:
#                     print(e)
#                 print(
#                     '\033[0;31;40mSomething has gone Wrong! Please check your config file!\033[0m')
