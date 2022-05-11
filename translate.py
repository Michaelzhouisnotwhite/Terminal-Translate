from trans_tools import command_mode
from utils.settings import *
import requests
import argparse
from hashlib import md5
import random
from utils import *
from utils.api import *
import sys


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    with open(LANG_TABLE, 'r') as f:
        lang_tb = f.read()
    parser.add_argument('target_words', help="target translate words. Enter number '0' to activate command mode", type=str)
    parser.add_argument('--lang', '-l', help=f"language you use\n{lang_tb}", default="auto", type=str)
    parser.add_argument('--to_lang', '-t', '-f', help="translate to the lang", default='zh')
    parser.add_argument('-c', help='use config file', action='store_true')
    return parser.parse_args()


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


# 检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def get_salt() -> str:
    return str(random.randint(32768, 65536))


def translate():
    args = get_args()

    check_config()

    query = args.target_words
    if query[0] == '0':
        command_mode()
        return

    if args.c:
        lang = CONFIG.config['from_lang']
        to = CONFIG.config['to_lang']

    elif is_contains_chinese(query):
        lang = 'zh'
        to = 'en'

    else:
        lang = args.lang
        to = args.to_lang

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    salt = get_salt()
    params = {
        'appid': CONFIG.config['appid'],
        'q': query,
        'from': lang,
        'to': to,
        'salt': salt,
        'sign': make_md5(CONFIG.config['appid'] + query + salt + CONFIG.config['appkey'])
    }
    rjson = {}

    try:
        rjson = get_trans(params=params, headers=headers)
    except Exception as e:
        if DEBUG:
            print(e)
        print("\033[0;31;mSomething has gone Wrong! Probably due to your NetWork Status.\033[0m")
    try:
        parse_res_json(rjson)

        with open(HISTORY, "r+", encoding="utf-8") as file:
            history = json.load(file)
            history['history'].append(rjson)
            file.seek(0)
            json.dump(history, file, indent=4, ensure_ascii=False)

    except FileNotFoundError as e:
        with open(HISTORY, "w", encoding="utf-8") as file:
            history = {
                'history': []
            }
            history['history'].append(rjson)
            file.seek(0)
            json.dump(history, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    translate()
