import time
from datetime import datetime

from utils import *
from utils.api import *
from colorprt import colorstr


class TranslateTools:
    class TransResult:
        fl = None
        tl = None
        trans = None
        lang_output_config = ColorprtConfig(foreground=Fore.BLUE)

        def __init__(self, rjson) -> None:
            try:
                self.fl = rjson['from']
                self.tl = rjson['to']
                self.trans = rjson["trans_result"]

            except KeyError as e:
                if DEBUG:
                    print(e)

                print("\033[0;31;mSomething has gone Wrong! Probably due to your NetWork Status.\033[0m")

        def format_show(self):
            if len(self.trans) == 1:
                res = ''
            else:
                res = str(colorstr('[{self.fl}-{self.tl}]', config=self.lang_output_config))
                # res = f'\33[36m[{self.fl}-{self.tl}]\33[0m\n'
            for idx, tran in enumerate(self.trans):
                dst = tran['dst']
                if len(self.trans) == 1:
                    format_line = colorstr(f'[{self.fl}-{self.tl}]', config=self.lang_output_config) + \
                        colorstr(f' {dst}', config=success_prt)
                    # format_line = f'\33[36m[{self.fl}-{self.tl}]\33[0m \33[32m{dst}\33[0m'
                else:
                    format_line = colorstr(f'{dst}', config=success_prt)
                    # format_line = f'\33[32m{dst}\33[0m'
                if idx == len(self.trans) - 1:
                    res += str(format_line)
                else:
                    res += str(format_line) + '\n'

            return res

    def __init__(self, appid: str, appkey: str) -> None:
        self.appid = appid
        self.appkey = appkey
        self.history_tool = HistoryTool()
        pass

    def translate(self, source: str, fl='auto', tl="zh", record=False):
        """
        translate word

        Args:
            source (str): words to be translate
            record (bool, optional): Is the word write in history. Defaults to False.
            fl (str): from language. Defaults to 'auto'
            tl (str): to language. Defaults to 'zh'
        """
        salt = get_salt()
        sign = make_md5(self.appid + source + salt + self.appkey)
        payload = {
            'appid': self.appid,
            'q': source,
            'from': fl,
            'to': tl,
            'salt': salt,
            'sign': sign
        }
        rjson = get_trans(params=payload)
        cur_time = datetime.now()
        rjson['time'] = cur_time.strftime("%Y-%m-%d, %H:%M:%S")
        if record:
            self.history_tool.write(rjson)
        return self.TransResult(rjson)
