import sys
from os.path import realpath, join, dirname, abspath

from logbook import Logger
import os

istravis = os.environ.get('TRAVIS') == 'true'
pyfalog = Logger(__name__)

debug = False
gamedataCache = True
saveddataCache = True
gamedata_version = ""
gamedata_date = ""
gamedata_connectionstring = 'sqlite:///' + realpath(join(dirname(abspath(__file__)), "..", "eve.db"))

lang = ""

# Maps supported langauges to their suffix in the database
translation_mapping = {
    "en": "",
    "fr": "_fr",
    # "it": "_it",
    "ja": "_ja",
    "ko": "_ko",
    "ru": "_ru",
    "zh": "_zh",
}

def set_lang(i18n_lang):
    global lang
    lang = translation_mapping.get(i18n_lang, translation_mapping.get("en"))

pyfalog.debug("Gamedata connection string: {0}", gamedata_connectionstring)

if istravis is True or hasattr(sys, '_called_from_test'):
    # Running in Travis. Run saveddata database in memory.
    saveddata_connectionstring = 'sqlite:///:memory:'
else:
    saveddata_connectionstring = 'sqlite:///' + realpath(join(dirname(abspath(__file__)), "..", "saveddata", "saveddata.db"))

pyfalog.debug("Saveddata connection string: {0}", saveddata_connectionstring)

settings = {
    "useStaticAdaptiveArmorHardener": False,
    "strictSkillLevels": True,
    "globalDefaultSpoolupPercentage": 1.0
}

# Autodetect path, only change if the autodetection bugs out.
path = dirname(__file__)
