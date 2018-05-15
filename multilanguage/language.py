import configparser
from multilanguage import packs

current_language = ""
conf = configparser.ConfigParser()
conf.read("language.ini")


def get_current_language():
    global current_language
    current_language = conf.get("language", "current_language")
    if current_language not in packs.packs_list:
        change_current_language("default")
        current_language = "default"


def change_current_language(new_language):
    global current_language
    current_language = new_language
    conf.set("language", "current_language", new_language)
    conf.write(open('language.ini', 'w'))


get_current_language()
