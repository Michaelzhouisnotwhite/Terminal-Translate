import json
import os
import platform
import sys
from typing import Any

from colorprt import Fore, colorprt
from colorprt.default import error, warn

try:
    DEBUG = os.environ['TRANS_DEBUG']
except KeyError:
    DEBUG = False

OS_TYPE = platform.system()
__ENDPOINT = 'http://api.fanyi.baidu.com'
__PATH = '/api/trans/vip/translate'
REQUEST_URL = __ENDPOINT + __PATH
WORKSPACE_FOLDER = r'D:\Repository\Terminal-Translate'
LANG_TABLE = f'{os.path.dirname(os.path.abspath(__file__))}/lang_tb'
QUERY_HELP = f'{os.path.dirname(os.path.abspath(__file__))}/query_help_menu'
WELCOME = f'{os.path.dirname(os.path.abspath(__file__))}/welcome'


class HistoryTool:
    HISTORY = None

    def __init__(self) -> None:
        self.check_envs()

    def check_envs(self):
        if DEBUG:
            os.environ['TRANSLATE_HIS'] = f'{WORKSPACE_FOLDER}\\.trans_config'
        try:
            tran_his_folder = os.environ['TRANSLATE_HIS']
        except KeyError as e:
            if DEBUG:
                print(e)
                # os.environ['TRANSLATE_HIS'] = r'D:\Code\Terminal-Translate\.trans_config'
            else:
                if OS_TYPE == "Windows":
                    os.environ['TRANSLATE_HIS'] = os.path.join(os.getenv('USERPROFILE'), '.trans_config')
                    
                elif OS_TYPE == "Linux":
                    os.environ['TRANSLATE_HIS'] = os.path.join(os.getenv('HOME'), '.trans_config')
                    
                else:
                    error("Can't recognize this os platform!")
                    sys.exit(-1)
                    
            tran_his_folder = os.environ['TRANSLATE_HIS']

        self.HISTORY = os.path.join(tran_his_folder, 'history.json')
        if not os.path.exists(tran_his_folder):
            os.mkdir(tran_his_folder)

        if not os.path.exists(self.HISTORY):
            f = open(self.HISTORY, 'w')
            f.close()

    def write(self, one_record: Any):
        history = []
        f = open(self.HISTORY, 'r', encoding='utf8')
        try:
            history = json.load(f)
            f.close()
        except json.JSONDecodeError as e:
            if DEBUG:
                print(e)

            f.close()
            ff = open(self.HISTORY, 'w', encoding='utf8')
            json.dump(history, ff)
            ff.close()

        history.append(one_record)
        with open(self.HISTORY, 'w', encoding='utf8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def get_content(self):
        with open(self.HISTORY, 'r', encoding='utf8') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError as e:
                if DEBUG:
                    print(e)
                return []

        return history


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
        if DEBUG:
            os.environ['TRANSLATE_CONFIG'] = fr'{WORKSPACE_FOLDER}\.trans_config'

        try:
            tran_config_folder = os.environ['TRANSLATE_CONFIG']
        except KeyError as e:
            if DEBUG:
                print(e)
            else:
                if OS_TYPE == "Windows":
                    os.environ['TRANSLATE_CONFIG'] = os.path.join(os.getenv('USERPROFILE'), '.trans_config')
                    
                elif OS_TYPE == "Linux":
                    os.environ['TRANSLATE_CONFIG'] = os.path.join(os.getenv('HOME'), '.trans_config')
                    
                else:
                    error("Can't recognize current os platform.")
                    sys.exit(-1)
                    
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
