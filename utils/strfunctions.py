'''
 string manipulation module
'''
import re


def sequential_rep(text_, *args):
    # type: (basestring, tuple) -> basestring
    """
    :param text_: string content
    :param args: like <pattern>, <replacement>, <pattern>, <replacement>, ...
    :return: if text_ length was zero or invalid parameters then no manipulation to text_
    """
    arg_len = len(args)
    if arg_len % 2 == 0 and isinstance(text_, basestring) and len(text_) > 0:
        i = 0
        while i < arg_len:
            text_ = re.sub(args[i], args[i + 1], text_)
            i += 2

    return text_


def replace_ltgt(text_):
    # type: (basestring) -> basestring
    """if fit name contained "<" or ">" then reprace to named html entity by EVE client.
    :param text_: string content of fit name from exported by EVE client.
    :return: if text_ is not instance of basestring then no manipulation to text_.
    """
    return text_.replace("&lt;", "<").replace("&gt;", ">") if isinstance(text_, basestring) else text_
