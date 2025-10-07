"""
 string manipulation module
"""
import re

def sequential_rep(text_, *args):
    # type: (str, *str) -> str
    """
    :param text_: string content
    :param args: like <pattern>, <replacement>, <pattern>, <replacement>, ...
    :return: if text_ length was zero or invalid parameters then no manipulation to text_
    """
    arg_len = len(args)
    if arg_len % 2 == 0 and isinstance(text_, str) and len(text_) > 0:
        i = 0
        while i < arg_len:
            text_ = re.sub(args[i], args[i + 1], text_)
            i += 2

    return text_
