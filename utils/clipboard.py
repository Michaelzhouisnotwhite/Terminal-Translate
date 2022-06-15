import pyperclip


def pretty_str(src: str):
    split_list = src.splitlines()
    res: str = ""
    end_punction = ".!?。！？"
    for s in split_list:
        s = s.strip()
        if s[-1] in end_punction:
            res += "\n" + s
        else:
            res += " " + s

    return res


def get_clipboard():
    clip_cache = pyperclip.waitForNewPaste()
    return pretty_str(clip_cache)


if __name__ == "__main__":
    print(get_clipboard())
