from utils.settings import *
import requests
import argparse
from hashlib import md5
import random


def main():
    pass


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_words', help="target translate words", type=str)
    parser.add_argument('--lang', '-l', help="language you use", default="en", type=str)
    parser.add_argument('--to_lang', help="translate to the lang", default='zh')
    # parser.add_argument('--init', '-i', help="init terminal translator")
    return parser.parse_args()


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def get_salt() -> str:
    return str(random.randint(32768, 65536))


def translate():
    args = get_args()
    query = args.target_words
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
        print("\033[0;31;40mSomething has gone Wrong! Probably due to your NetWork Status.\033[0m")

    try:
        from_lang = rjson['from']
        to_lang = rjson['to']
        trans = rjson["trans_result"][0]['dst']
        print(f'From:\33[35m{from_lang}\33[0m')
        print(f'To:\33[36m{to_lang}\33[0m')
        print(f'Translation:\33[32m{trans}\33[0m')

    except Exception:
        print('\033[0;31;40mSomething has gone Wrong! Please check your config file!\033[0m')


if __name__ == "__main__":
    translate()
