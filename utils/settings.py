import os
import json


DEBUG = True


__ENDPOINT = 'http://api.fanyi.baidu.com'
__PATH = '/api/trans/vip/translate'
REQUEST_URL = __ENDPOINT + __PATH

LANG_TABLE = f'{os.path.dirname(os.path.abspath(__file__))}/lang_tb'
WELCOME = f'{os.path.dirname(os.path.abspath(__file__))}/welcome'


class HistoryTool:
    HISTORY = None

    def __init__(self) -> None:
        self.check_envs()
        self.history = []

    def check_envs(self):
        try:
            tran_his_folder = os.environ['TRANSLATE_HIS']
        except KeyError as e:
            if DEBUG:
                print(e)
                os.environ['TRANSLATE_HIS'] = r'D:\Code\Terminal-Translate\.trans_config'
            else:
                os.environ['TRANSLATE_HIS'] = os.path.join(os.getenv('USERPROFILE'), '.trans_config')
            tran_his_folder = os.environ['TRANSLATE_HIS']

        self.HISTORY = os.path.join(tran_his_folder, 'history.json')
        if not os.path.exists(tran_his_folder):
            os.mkdir(tran_his_folder)

        if not os.path.exists(self.HISTORY):
            f = open(self.HISTORY, 'w')
            f.close()

    def write(self, one_record):
        f = open(self.HISTORY, 'r')
        try:
            self.history = json.load(f)
            f.close()
        except json.JSONDecodeError as e:
            if DEBUG:
                print(e)

            f.close()
            ff = open(self.HISTORY, 'w')
            json.dump(self.history, ff)

        self.history.append(one_record)
        with open(self.HISTORY, 'w') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)


class ConfigTools:
    CONFIG_JSON = None
    HISTORY = None

    def __init__(self) -> None:
        self.check_envs()

        self.config = {}
        self.appid = ''
        self.appkey = ''
        self.from_lang = ''
        self.to_lang = ''
        
        self.check_config()

    def check_envs(self):
        try:
            tran_config_folder = os.environ['TRANSLATE_CONFIG']
        except KeyError as e:
            if DEBUG:
                print(e)
                os.environ['TRANSLATE_CONFIG'] = r'D:\Code\Terminal-Translate\.trans_config'
            else:
                os.environ['TRANSLATE_CONFIG'] = os.path.join(os.getenv('USERPROFILE'), '.trans_config')
            tran_config_folder = os.environ['TRANSLATE_CONFIG']

        self.CONFIG_JSON = os.path.join(tran_config_folder, 'config.json')
        if not os.path.exists(tran_config_folder):
            os.mkdir(tran_config_folder)

    def check_config(self):
        try:
            with open(self.CONFIG_JSON, 'r') as f:
                try:
                    self.config = json.load(f)
                except json.JSONDecodeError as e:
                    if DEBUG:
                        print(e)

                    self.init_config()

                if self.config['appid'] == '' or self.config['appkey'] == '':
                    self.init_config()

        except FileNotFoundError as e:
            if DEBUG:
                print(e)

            self.init_config()

        self.appid = self.config['appid']
        self.appkey = self.config['appkey']

        self.from_lang = self.config['from_lang']
        self.to_lang = self.config['to_lang']

    def init_config(self):
        self.appid = str(input("> Please input your appid below:\n> ")).strip()
        self.appkey = str(input("> Please input your appkey below:\n> ")).strip()
        self.from_lang = 'en'
        self.to_lang = 'zh'
        self.save_config()
        print("> \33[32mSet Key Success!\33[0m")

    def save_config(self):
        self.config['appid'] = self.appid
        self.config['appkey'] = self.appkey
        self.config['from_lang'] = self.from_lang
        self.config['to_lang'] = self.to_lang

        with open(self.CONFIG_JSON, 'w', encoding='utf-8') as file:
            json.dump(self.config, file, ensure_ascii=False)

    def set_language(self, fl=None, tl=None):
        if fl is not None:
            self.from_lang = fl
        if tl is not None:
            self.to_lang = tl

        self.save_config()
