# -*- coding: cp1251 -*-

import config
import os


def test_parsePath_with_codec():
    config.codec = "cp1251"
    basepath = "\Users\Гоша Егорян\.pyfa"
    base = os.path.normpath(basepath)

    create_result = config.parsePath(base, None, "Skip")

    assert create_result
    assert type(create_result) == unicode
    assert type(create_result) != str

    assert create_result == "\\Users\\Гоша Егорян\\.pyfa".decode(config.codec)
    assert create_result != "\\Users\\Гоша Егорян\\.pyfa"
    assert create_result != "\\Users\\???? ??????\\.pyfa"
    assert create_result != "\\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\\.pyfa"

    assert base != "\\Users\\Гоша Егорян\\.pyfa".decode(config.codec)
    assert base == "\\Users\\Гоша Егорян\\.pyfa"
    assert base != "\\Users\\???? ??????\\.pyfa"
    assert base == "\\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\\.pyfa"

    assert basepath != "\Users\Гоша Егорян\.pyfa".decode(config.codec)
    assert basepath == "\Users\Гоша Егорян\.pyfa"
    assert basepath != "\Users\???? ??????\.pyfa"
    assert basepath == "\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\.pyfa"


def test_parsePath_without_codec():
    codec = "cp1251"
    basepath = "\Users\Гоша Егорян\.pyfa"
    base = os.path.normpath(basepath)

    create_result = config.parsePath(base, None, "Skip")

    assert create_result
    assert type(create_result) == unicode
    assert type(create_result) != str

    assert create_result == "\\Users\\Гоша Егорян\\.pyfa".decode(codec)
    assert create_result != "\\Users\\Гоша Егорян\\.pyfa"
    assert create_result != "\\Users\\???? ??????\\.pyfa"
    assert create_result != "\\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\\.pyfa"

    assert base != "\\Users\\Гоша Егорян\\.pyfa".decode(codec)
    assert base == "\\Users\\Гоша Егорян\\.pyfa"
    assert base != "\\Users\\???? ??????\\.pyfa"
    assert base == "\\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\\.pyfa"

    assert basepath != "\Users\Гоша Егорян\.pyfa".decode(codec)
    assert basepath == "\Users\Гоша Егорян\.pyfa"
    assert basepath != "\Users\???? ??????\.pyfa"
    assert basepath == "\Users\\\xc3\xee\xf8\xe0 \xc5\xe3\xee\xf0\xff\xed\.pyfa"
