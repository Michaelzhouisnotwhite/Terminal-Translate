import json
from hashlib import md5

from .settings import *
import random


def parse_res_json(rjson: dict):
    try:
        from_lang = rjson['from']
        to_lang = rjson['to']
        trans = rjson["trans_result"][0]['dst']
        print(f'\33[36m[{from_lang}-{to_lang}]\33[0m \33[32m{trans}\33[0m')

    except KeyError as err:
        print(f'{err}')
        print(json.dumps(rjson, indent=2, ensure_ascii=False))
        print('\033[0;31;40mSomething has gone Wrong! Please check your config file!\033[0m')


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
