# -*- coding: cp1251 -*-

import config
import os

def test_parsePath_with_codec():
    config.codec = "cp1251"
    base = "C:\Users\Гоша Егорян\.pyfa"
    base = os.path.realpath(os.path.abspath(base))

    create_result = config.parsePath(base, None, "Skip")

    assert create_result
    assert type(create_result) == unicode
    assert type(create_result) != str

    assert create_result == ("C:\\Users\\Гоша Егорян\\.pyfa").decode(config.codec)
    assert create_result != "C:\\Users\\Гоша Егорян\\.pyfa"
    assert create_result != "C:\\Users\\???? ??????\\.pyfa"
    assert create_result != "C:\\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\\.pyfa"

    assert base != ("C:\\Users\\Гоша Егорян\\.pyfa").decode(config.codec)
    assert base == "C:\\Users\\Гоша Егорян\\.pyfa"
    assert base != "C:\\Users\\???? ??????\\.pyfa"
    assert base == "C:\\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\\.pyfa"


def test_parsePath_without_codec():
    codec = "cp1251"
    base = "C:\Users\Гоша Егорян\.pyfa"
    base = os.path.realpath(os.path.abspath(base))

    create_result = config.parsePath(base, None, "Skip")

    assert create_result
    assert type(create_result) == unicode
    assert type(create_result) != str

    assert create_result == ("C:\\Users\\Гоша Егорян\\.pyfa").decode(codec)
    assert create_result != "C:\\Users\\Гоша Егорян\\.pyfa"
    assert create_result != "C:\\Users\\???? ??????\\.pyfa"
    assert create_result != "C:\\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\\.pyfa"

    assert base != ("C:\\Users\\Гоша Егорян\\.pyfa").decode(codec)
    assert base == "C:\\Users\\Гоша Егорян\\.pyfa"
    assert base != "C:\\Users\\???? ??????\\.pyfa"
    assert base == "C:\\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\\.pyfa"
