import os

APP_ID = '20210819000921635'
APP_KEY = '_RuALqBSiy2n3ri5WSjT'
__ENDPOINT = 'http://api.fanyi.baidu.com'
__PATH = '/api/trans/vip/translate'
REQUEST_URL = __ENDPOINT + __PATH

LANG_TABLE = f'{os.path.dirname(os.path.abspath(__file__))}/lang_tb'
