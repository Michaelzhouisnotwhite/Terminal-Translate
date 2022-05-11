import os
import json

DEBUG = False


class CONFIG:
    config = {}


__ENDPOINT = 'http://api.fanyi.baidu.com'
__PATH = '/api/trans/vip/translate'
REQUEST_URL = __ENDPOINT + __PATH

LANG_TABLE = f'{os.path.dirname(os.path.abspath(__file__))}/lang_tb'
CONFIG_JSON = f'{os.path.dirname(os.path.abspath(__file__))}/config.json'
HISTORY = f'{os.path.dirname(os.path.abspath(__file__))}/history.json'
WELCOME = f'{os.path.dirname(os.path.abspath(__file__))}/welcome'


def set_key(appid, appkey, config):
    config['appid'] = appid
    config['appkey'] = appkey
    config['from_lang'] = 'en'
    config['to_lang'] = 'zh'

    with open(CONFIG_JSON, 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False)


def init():
    global CONFIG
    CONFIG.config = {}
    appid = input("> Please input your appid below:\n> ")
    appkey = input("> Please input your appkey below:\n> ")
    set_key(appid, appkey, CONFIG.config)
    with open(CONFIG_JSON, 'r', encoding='utf-8') as file:
        CONFIG.config = json.load(file)
    print("> \33[32mSet Key Success!\33[0m")


def check_config():
    global CONFIG
    try:
        with open(CONFIG_JSON, 'r', encoding='utf-8') as file:
            try:
                CONFIG.config = json.load(file)
            except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
                if DEBUG:
                    print(e)
                init()

    except FileNotFoundError as e:
        if DEBUG:
            print(e)
        init()

    if not CONFIG.config['appid'] or not CONFIG.config['appkey']:
        init()


def set_language(*args):
    langs = args[0].split('-')
    if DEBUG:
        print(langs)
    if len(langs) != 2:
        print('Invalid Languages! Please Try Again!')
    else:
        CONFIG.config["from_lang"] = langs[0]
        CONFIG.config['to_lang'] = langs[1]
        with open(CONFIG_JSON, 'w') as file:
            json.dump(CONFIG.config, file, ensure_ascii=False)
