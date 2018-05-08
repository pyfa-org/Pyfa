# =============================================================================
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
# =============================================================================

import pickle
import os.path
import urllib.request
import urllib.error
import urllib.parse

import config
import eos.config
from logbook import Logger

pyfalog = Logger(__name__)


class SettingsProvider(object):
    if config.savePath:
        BASE_PATH = os.path.join(config.savePath, 'settings')
    settings = {}
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = SettingsProvider()

        return cls._instance

    def __init__(self):
        if hasattr(self, 'BASE_PATH'):
            if not os.path.exists(self.BASE_PATH):
                os.mkdir(self.BASE_PATH)

    # def getSettings(self, area, defaults=None):
    #     # type: (basestring, dict) -> service.Settings
    #     # NOTE: needed to change for tests
    #     settings_obj = self.settings.get(area)
    #
    #     if settings_obj is None and hasattr(self, 'BASE_PATH'):
    #         canonical_path = os.path.join(self.BASE_PATH, area)
    #
    #         if not os.path.exists(canonical_path):
    #             info = {}
    #             if defaults:
    #                 for item in defaults:
    #                     info[item] = defaults[item]
    #
    #         else:
    #             try:
    #                 f = open(canonical_path, "rb")
    #                 info = cPickle.load(f)
    #                 for item in defaults:
    #                     if item not in info:
    #                         info[item] = defaults[item]
    #
    #             except:
    #                 info = {}
    #                 if defaults:
    #                     for item in defaults:
    #                         info[item] = defaults[item]
    #
    #         self.settings[area] = settings_obj = Settings(canonical_path, info)
    #
    #     return settings_obj
    def getSettings(self, area, defaults=None):
        # type: (basestring, dict) -> service.Settings
        # NOTE: needed to change for tests
        # TODO: Write to memory with mmap -> https://docs.python.org/2/library/mmap.html
        settings_obj = self.settings.get(area)
        if settings_obj is None:  # and hasattr(self, 'BASE_PATH'):
            canonical_path = os.path.join(self.BASE_PATH, area) if hasattr(self, 'BASE_PATH') else ""
            if not os.path.exists(canonical_path):  # path string or empty string.
                info = {}
                if defaults:
                    info.update(defaults)
            else:
                try:
                    with open(canonical_path, "rb") as f:
                        info = pickle.load(f)
                    for item in defaults:
                        if item not in info:
                            info[item] = defaults[item]
                except:
                    info = {}
                    info.update(defaults)

            self.settings[area] = settings_obj = Settings(canonical_path, info)
        return settings_obj

    def saveAll(self):
        for settings in self.settings.values():
            settings.save()


class Settings(object):
    def __init__(self, location, info):
        # type: (basestring, dict) -> None
        # path string or empty string.
        self.location = location
        self.info = info

    # def save(self):
    #     f = open(self.location, "wb")
    #     cPickle.dump(self.info, f, cPickle.HIGHEST_PROTOCOL)

    def save(self):
        # NOTE: needed to change for tests
        if self.location is None or not self.location:
            return
        # NOTE: with + open -> file handle auto close
        with open(self.location, "wb") as f:
            pickle.dump(self.info, f, pickle.HIGHEST_PROTOCOL)

    def __getitem__(self, k):
        try:
            return self.info[k]
        except KeyError as e:
            pyfalog.warning("Failed to get setting for '{0}'. Exception: {1}", k, e)
            return None

    def __setitem__(self, k, v):
        self.info[k] = v

    def __iter__(self):
        return self.info.__iter__()

    def iterkeys(self):
        return iter(self.info.keys())

    def itervalues(self):
        return iter(self.info.values())

    def iteritems(self):
        return iter(self.info.items())

    def keys(self):
        return list(self.info.keys())

    def values(self):
        return list(self.info.values())

    def items(self):
        return list(self.info.items())


class NetworkSettings(object):
    _instance = None

    # constants for serviceNetworkDefaultSettings["mode"] parameter
    PROXY_MODE_NONE = 0  # 0 - No proxy
    PROXY_MODE_AUTODETECT = 1  # 1 - Auto-detected proxy settings
    PROXY_MODE_MANUAL = 2  # 2 - Manual proxy settings

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = NetworkSettings()

        return cls._instance

    def __init__(self):

        serviceNetworkDefaultSettings = {
            "mode"    : self.PROXY_MODE_AUTODETECT,
            "type"    : "https",
            "address" : "",
            "port"    : "",
            "access"  : 15,
            "login"   : None,
            "password": None
        }

        self.serviceNetworkSettings = SettingsProvider.getInstance().getSettings(
                "pyfaServiceNetworkSettings", serviceNetworkDefaultSettings)

    def isEnabled(self, type):
        if type & self.serviceNetworkSettings["access"]:
            return True
        return False

    def toggleAccess(self, type, toggle=True):
        bitfield = self.serviceNetworkSettings["access"]

        if toggle:  # Turn bit on
            self.serviceNetworkSettings["access"] = type | bitfield
        else:  # Turn bit off
            self.serviceNetworkSettings["access"] = ~type & bitfield

    def getMode(self):
        return self.serviceNetworkSettings["mode"]

    def getAddress(self):
        return self.serviceNetworkSettings["address"]

    def getPort(self):
        return self.serviceNetworkSettings["port"]

    def getType(self):
        return self.serviceNetworkSettings["type"]

    def getAccess(self):
        return self.serviceNetworkSettings["access"]

    def setMode(self, mode):
        self.serviceNetworkSettings["mode"] = mode

    def setAddress(self, addr):
        self.serviceNetworkSettings["address"] = addr

    def setPort(self, port):
        self.serviceNetworkSettings["port"] = port

    def setType(self, type):
        self.serviceNetworkSettings["type"] = type

    def setAccess(self, access):
        self.serviceNetworkSettings["access"] = access

    @staticmethod
    def autodetect():

        proxy = None
        proxydict = urllib.request.ProxyHandler().proxies

        validPrefixes = ("http", "https")

        for prefix in validPrefixes:
            if prefix not in proxydict:
                continue
            proxyline = proxydict[prefix]
            proto = "{0}://".format(prefix)
            if proxyline[:len(proto)] == proto:
                proxyline = proxyline[len(proto):]
            proxAddr, proxPort = proxyline.split(":")
            proxPort = int(proxPort.rstrip("/"))
            proxy = (proxAddr, proxPort)
            break

        return proxy

    def getProxySettings(self):

        if self.getMode() == self.PROXY_MODE_NONE:
            return None
        if self.getMode() == self.PROXY_MODE_AUTODETECT:
            return self.autodetect()
        if self.getMode() == self.PROXY_MODE_MANUAL:
            return self.getAddress(), int(self.getPort())

    def getProxyAuthDetails(self):
        if self.getMode() == self.PROXY_MODE_NONE:
            return None
        if (self.serviceNetworkSettings["login"] is None) or (self.serviceNetworkSettings["password"] is None):
            return None
        # in all other cases, return tuple of (login, password)
        return self.serviceNetworkSettings["login"], self.serviceNetworkSettings["password"]

    def setProxyAuthDetails(self, login, password):
        if (login is None) or (password is None):
            self.serviceNetworkSettings["login"] = None
            self.serviceNetworkSettings["password"] = None
            return
        if login == "":  # empty login unsets proxy auth info
            self.serviceNetworkSettings["login"] = None
            self.serviceNetworkSettings["password"] = None
            return
        self.serviceNetworkSettings["login"] = login
        self.serviceNetworkSettings["password"] = password


class HTMLExportSettings(object):
    """
    Settings used by the HTML export feature.
    """
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = HTMLExportSettings()

        return cls._instance

    def __init__(self):
        serviceHTMLExportDefaultSettings = {
            "path"   : config.savePath + os.sep + 'pyfaFits.html',
            "minimal": False
        }
        self.serviceHTMLExportSettings = SettingsProvider.getInstance().getSettings(
                "pyfaServiceHTMLExportSettings",
                serviceHTMLExportDefaultSettings
        )

    def getMinimalEnabled(self):
        return self.serviceHTMLExportSettings["minimal"]

    def setMinimalEnabled(self, minimal):
        self.serviceHTMLExportSettings["minimal"] = minimal

    def getPath(self):
        return self.serviceHTMLExportSettings["path"]

    def setPath(self, path):
        self.serviceHTMLExportSettings["path"] = path


class UpdateSettings(object):
    """
    Settings used by update notification
    """
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = UpdateSettings()

        return cls._instance

    def __init__(self):
        # Settings
        # Updates are completely suppressed via network settings
        # prerelease - If True, suppress prerelease notifications
        # version    - Set to release tag that user does not want notifications for
        serviceUpdateDefaultSettings = {"prerelease": True, 'version': None}
        self.serviceUpdateSettings = SettingsProvider.getInstance().getSettings(
                "pyfaServiceUpdateSettings",
                serviceUpdateDefaultSettings
        )

    def get(self, type):
        return self.serviceUpdateSettings[type]

    def set(self, type, value):
        self.serviceUpdateSettings[type] = value


class EsiSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = EsiSettings()

        return cls._instance

    def __init__(self):
        # LoginMode:
        # 0 - Server Start Up
        # 1 - User copy and paste data from website to pyfa
        defaults = {"loginMode": 0, "clientID": "", "clientSecret": "", "timeout": 60}

        self.settings = SettingsProvider.getInstance().getSettings(
                "pyfaServiceEsiSettings",
                defaults
        )

    def get(self, type):
        return self.settings[type]

    def set(self, type, value):
        self.settings[type] = value


class StatViewSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = StatViewSettings()

        return cls._instance

    def __init__(self):
        # mode
        # 0 - Do not show
        # 1 - Minimal/Text Only View
        # 2 - Full View
        serviceStatViewDefaultSettings = {
            "resources"    : 2,
            "resistances"  : 2,
            "recharge"     : 2,
            "firepower"    : 2,
            "capacitor"    : 2,
            "targetingMisc": 1,
            "price"        : 2,
            "miningyield"  : 2,
            "drones"       : 2,
            "outgoing"     : 2,
        }

        # We don't have these....yet
        '''
        "miningyield": 2,
        "drones": 2
        '''

        self.serviceStatViewDefaultSettings = SettingsProvider.getInstance().getSettings("pyfaServiceStatViewSettings", serviceStatViewDefaultSettings)

    def get(self, type):
        return self.serviceStatViewDefaultSettings[type]

    def set(self, type, value):
        self.serviceStatViewDefaultSettings[type] = value


class PriceMenuSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = PriceMenuSettings()

        return cls._instance

    def __init__(self):
        # mode
        # 0 - Do not add to total
        # 1 - Add to total
        PriceMenuDefaultSettings = {
            "ship" : 1,
            "modules" : 1,
            "drones" : 0,
            "cargo" : 0,
            "character" : 0
        }

        self.PriceMenuDefaultSettings = SettingsProvider.getInstance().getSettings("pyfaPriceMenuSettings",
                                                                                     PriceMenuDefaultSettings)

    def get(self, type):
        return self.PriceMenuDefaultSettings[type]

    def set(self, type, value):
        self.PriceMenuDefaultSettings[type] = value


class ContextMenuSettings(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = ContextMenuSettings()

        return cls._instance

    def __init__(self):
        # mode
        # 0 - Do not show
        # 1 - Show
        ContextMenuDefaultSettings = {
            "ammoPattern"           : 1,
            "amount"                : 1,
            "cargo"                 : 1,
            "cargoAmmo"             : 1,
            "changeAffectingSkills" : 1,
            "damagePattern"         : 1,
            "droneRemoveStack"      : 1,
            "droneSplit"            : 1,
            "droneStack"            : 1,
            "factorReload"          : 1,
            "fighterAbilities"      : 1,
            "implantSets"           : 1,
            "itemStats"             : 1,
            "itemRemove"            : 1,
            "marketJump"            : 1,
            "metaSwap"              : 1,
            "moduleAmmoPicker"      : 1,
            "moduleGlobalAmmoPicker": 1,
            "openFit"               : 1,
            "priceClear"            : 1,
            "project"               : 1,
            "shipJump"              : 1,
            "tacticalMode"          : 1,
            "targetResists"         : 1,
            "whProjector"           : 1,
        }

        self.ContextMenuDefaultSettings = SettingsProvider.getInstance().getSettings("pyfaContextMenuSettings", ContextMenuDefaultSettings)

    def get(self, type):
        return self.ContextMenuDefaultSettings[type]

    def set(self, type, value):
        self.ContextMenuDefaultSettings[type] = value


class EOSSettings(object):
        _instance = None

        @classmethod
        def getInstance(cls):
            if cls._instance is None:
                cls._instance = EOSSettings()

            return cls._instance

        def __init__(self):
            self.EOSSettings = SettingsProvider.getInstance().getSettings("pyfaEOSSettings", eos.config.settings)

        def get(self, type):
            return self.EOSSettings[type]

        def set(self, type, value):
            self.EOSSettings[type] = value

# @todo: migrate fit settings (from fit service) here?
