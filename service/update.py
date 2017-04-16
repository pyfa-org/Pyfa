# =============================================================================
# Copyright (C) 2014 Ryan Holmes
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

import threading
import json
import calendar

# noinspection PyPackageRequirements
import wx
# noinspection PyPackageRequirements
import dateutil.parser

import config
from service.network import Network
from service.settings import UpdateSettings
from logbook import Logger

pyfalog = Logger(__name__)


class CheckUpdateThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.name = "CheckUpdate"
        self.callback = callback
        self.settings = UpdateSettings.getInstance()
        self.network = Network.getInstance()

    def run(self):
        network = Network.getInstance()

        try:
            response = network.request('https://api.github.com/repos/pyfa-org/Pyfa/releases', network.UPDATE)
            jsonResponse = json.loads(response.read())
            jsonResponse.sort(
                key=lambda x: calendar.timegm(dateutil.parser.parse(x['published_at']).utctimetuple()),
                reverse=True
            )

            for release in jsonResponse:
                # Suppress pre releases
                if release['prerelease'] and self.settings.get('prerelease'):
                    continue

                # Handle use-case of updating to suppressed version
                if self.settings.get('version') == 'v' + config.version:
                    self.settings.set('version', None)

                # Suppress version
                if release['tag_name'] == self.settings.get('version'):
                    break

                # Set the release version that we will be comparing with.
                if release['prerelease']:
                    rVersion = release['tag_name'].replace('singularity-', '', 1)
                else:
                    rVersion = release['tag_name'].replace('v', '', 1)

                if config.tag is 'git' and \
                        not release['prerelease'] and \
                        self.versiontuple(rVersion) >= self.versiontuple(config.version):
                    wx.CallAfter(self.callback, release)  # git (dev/Singularity) -> Stable
                elif config.expansionName is not "Singularity":
                    if release['prerelease']:
                        wx.CallAfter(self.callback, release)  # Stable -> Singularity
                    elif self.versiontuple(rVersion) > self.versiontuple(config.version):
                        wx.CallAfter(self.callback, release)  # Stable -> Stable
                else:
                    if release['prerelease'] and rVersion > config.expansionVersion:
                        wx.CallAfter(self.callback, release)  # Singularity -> Singularity
                break
        except Exception as e:
            pyfalog.error("Caught exception in run")
            pyfalog.error(e)
            pass

    @staticmethod
    def versiontuple(v):
        return tuple(map(int, (v.split("."))))


class Update(object):
    instance = None

    @staticmethod
    def CheckUpdate(callback):
        thread = CheckUpdateThread(callback)
        pyfalog.debug("Starting Check Update Thread.")
        thread.start()

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Update()
        return cls.instance
