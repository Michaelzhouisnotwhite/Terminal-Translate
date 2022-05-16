from utils import *
from utils import settings
import argparse
from trans_tools import TranslateTools
import sys
import pyperclip


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    with open(LANG_TABLE, 'r') as f:
        lang_tb = f.read()
    parser.add_argument(
        'query', help="target translate words. Enter number '0' to activate command mode.", type=str)
    parser.add_argument('-f', '--from_lang', help=f"language you use\n{lang_tb}", default="auto", type=str)
    parser.add_argument('-t', '--to_lang', help="translate to the lang", default='zh')
    parser.add_argument('-r', help='write to history', action='store_true')
    args = parser.parse_args()
    return args.query, args.from_lang, args.to_lang, args.r


class TranService(object):
    def __init__(self, query, from_lang='auto', to_lang='zh', history=False) -> None:
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.history = history
        self.config_tool = ConfigTools()
        self.trans_tools = TranslateTools(self.config_tool.appid, self.config_tool.appkey)
        self.query_parser(query)

    def query_parser(self, query):
        if query == '0':
            # command mode
            self.command_mode()

        elif query == '1':
            # clipboard mode
            self.clipboard_mode()

        elif len(query) > 0:
            if is_contains_chinese(query) and self.to_lang == 'zh':
                self.to_lang = 'en'
            trans_res = self.trans_tools.translate(query, self.from_lang, self.to_lang, self.history)
            print(trans_res.format_show())
            self.exit()

    def __del__(self):
        if DEBUG:
            print("__del__")
        pass

    def exit(self):
        # self.__del__()
        sys.exit(0)

    def command_mode(self):
        pass

    def clipboard_mode(self):
        while True:
            print('> waiting for new clipboard ...')
            try:
                clip_cache = pyperclip.waitForNewPaste()

                if is_contains_chinese(clip_cache) and self.to_lang == 'zh':
                    self.to_lang = 'en'
                else:
                    self.from_lang = 'auto'
                    self.to_lang = 'zh'

                trans_res = self.trans_tools.translate(clip_cache, self.from_lang, self.to_lang, self.history)
                print(trans_res.format_show())
            except KeyboardInterrupt as e:
                if DEBUG:
                    print(e)
                print('See you next time')
                self.exit()


def main():
    TranService(*get_args())


if __name__ == "__main__":
    main()
