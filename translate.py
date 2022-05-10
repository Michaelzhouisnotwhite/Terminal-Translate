from utils.settings import *
import requests
import argparse
from hashlib import md5
import random


def main():
    pass


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    with open(LANG_TABLE, 'r') as f:
        lang_tb = f.read()
    parser.add_argument('target_words', help="target translate words", type=str)
    parser.add_argument('--lang', '-l', help=f"language you use\n{lang_tb}", default="auto", type=str)
    parser.add_argument('--to_lang', '-t', '-f', help="translate to the lang", default='zh')
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
    query = args.target_words
    if is_contains_chinese(query):
        lang = 'zh'
        to = 'en'

    else:
        lang = args.lang
        to = args.to_lang

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    salt = get_salt()
    params = {
        'appid': APP_ID,
        'q': query,
        'from': lang,
        'to': to,
        'salt': salt,
        'sign': make_md5(APP_ID + query + salt + APP_KEY)
    }
    rjson = {}

    try:
        res = requests.post(REQUEST_URL, params=params, headers=headers)
        rjson = res.json()
    except Exception as e:
        print("\033[0;31;mSomething has gone Wrong! Probably due to your NetWork Status.\033[0m")

    try:
        from_lang = rjson['from']
        to_lang = rjson['to']
        trans = rjson["trans_result"][0]['dst']
        print(f'\33[36m[{from_lang}-{to_lang}]\33[0m \33[32m{trans}\33[0m')

    except Exception:
        print(rjson)
        print('\033[0;31;40mSomething has gone Wrong! Please check your config file!\033[0m')


if __name__ == "__main__":
    translate()
