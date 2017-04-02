'''
 string manipulation module
'''
import re


def sequential_rep(text_, *args):
    """
    params
        text_: string content
        args : <pattern>, <replacement>, <pattern>, <replacement>, ...

    return
        empty string when text_ length was zero or invalid.
    """

    if not text_ or not len(text_):
        return ""

    arg_len = len(args)
    i = 0
    while i < arg_len:
        text_ = re.sub(args[i], args[i + 1], text_)
        i += 2

    return text_


def replaceLTGT(text_):
    """if fit name contained "<" or ">" then reprace to named html entity by EVE client.

       for fit name.
    """
    return text_.replace("&lt;", "<").replace("&gt;", ">") if isinstance(text_, unicode) else text_
