import json

from colorprt import colorprt

from utils import *
from utils import settings
import argparse
from TransTools import TranslateTools
import sys
import pyperclip


def trans_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    with open(LANG_TABLE, 'r') as f:
        lang_tb = f.read()
    with open(QUERY_HELP, 'r') as f:
        query_help_menu = f.read()
    parser.add_argument(
        'query', help=f"target translate words. Enter number to select translate options.\n{query_help_menu}", type=str)
    parser.add_argument('-f', '--from_lang', help=f"language you use\n{lang_tb}", default="auto", type=str)
    parser.add_argument('-t', '--to_lang', help="translate to the lang", default='zh')
    parser.add_argument('-r', help='don\'t add to history', action='store_false')
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

        elif query == '2':
            self.show_history()

        elif len(query) > 0:
            if is_contains_chinese(query) and self.to_lang == 'zh':
                self.to_lang = 'en'
            trans_res = self.trans_tools.translate(query, self.from_lang, self.to_lang, self.history)
            print(trans_res.format_show())
            self.exit()

        else:
            self.exit()

    def show_history(self):
        content = HistoryTool().get_content()
        if len(content) > 0:
            for his in content:
                print(json.dumps(his, indent=4, ensure_ascii=False))
        else:
            warning_prt("History Empty")

    def __del__(self):
        if DEBUG:
            print("__del__")
        pass

    @staticmethod
    def exit():
        # self.__del__()
        sys.exit(0)

    def command_mode(self):
        pass

    def clipboard_mode(self):
        default_prt("Translate Clipboard Mode")
        while True:
            default_prt(f'> waiting for new clipboard ...', end="")
            colorprt(f'[{self.from_lang} - {self.to_lang}]', Fore.BLUE)
            try:
                clip_cache = pyperclip.waitForNewPaste()
                if len(clip_cache) <= 0:
                    continue
                if is_contains_chinese(clip_cache):
                    self.to_lang = 'en'
                else:
                    self.from_lang = 'auto'
                    self.to_lang = 'zh'

                trans_res = self.trans_tools.translate(clip_cache, self.from_lang, self.to_lang, self.history)

                print(trans_res.format_show())
            except KeyboardInterrupt as e:
                if DEBUG:
                    print(e)
                success_prt('See you next time')
                self.exit()


def main():
    TranService(*trans_args())


if __name__ == "__main__":
    main()
