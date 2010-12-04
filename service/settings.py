#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import cPickle
import os.path
import config

class SettingsProvider():
    BASE_PATH = os.path.join(config.savePath, "settings")
    settings = {}
    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = SettingsProvider()

        return cls._instance

    def __init__(self):
        if not os.path.exists(self.BASE_PATH):
            os.mkdir(self.BASE_PATH);

    def getSettings(self, area, defaults=None):
        s = self.settings.get(area)
        if s is None:
            p = os.path.join(self.BASE_PATH, area)

            if not os.path.exists(p):
                info = {}
                if defaults:
                    for item in defaults:
                        info[item] = defaults[item]

            else:
                try:
                    f = open(p, "rb")
                    info = cPickle.load(f)

                except:
                    info = {}
                    if defaults:
                        for item in defaults:
                            info[item] = defaults[item]

            self.settings[area] = s = Settings(p, info)

        return s

    def saveAll(self):
        for settings in self.settings.itervalues():
            settings.save()

class Settings():
    def __init__(self, location, info):
        self.location = location
        self.info = info

    def save(self):
        f = open(self.location, "wb")
        cPickle.dump(self.info, f, cPickle.HIGHEST_PROTOCOL)

    def __getitem__(self, k):
        return self.info[k]

    def __setitem__(self, k, v):
        self.info[k] = v

    def __iter__(self):
        return self.info.__iter__()

    def iterkeys(self):
        return self.info.iterkeys()

    def itervalues(self):
        return self.info.itervalues()

    def iteritems(self):
        return self.info.iteritems()

    def keys(self):
        return self.info.keys()

    def values(self):
        return self.info.values()

    def items(self):
        return self.info.items()
