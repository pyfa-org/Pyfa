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

import threading
import wx
import urllib2
import json
import config
import service

class CheckUpdateThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.settings = service.settings.UpdateSettings.getInstance()

    def run(self):
        # Suppress all
        if (self.settings.get('all')):
            return

        try:
            # @todo: use proxy settings?
            response = urllib2.urlopen('https://api.github.com/repos/DarkFenX/Pyfa/releases')
            jsonResponse = json.loads(response.read());

            for release in jsonResponse:
                # Suppress pre releases
                if (release['prerelease'] and self.settings.get('prerelease')):
                    continue

                # Handle use-case of updating to suppressed version
                if self.settings.get('version') == 'v'+config.version:
                    self.settings.set('version', None)

                # Suppress version
                if (release['tag_name'] == self.settings.get('version')):
                    break

                # Set the release version that we will be comparing with.
                if release['prerelease']:
                    rVersion = release['tag_name'].replace('singularity-', '', 1)
                else:
                    rVersion = release['tag_name'].replace('v', '', 1)

                if config.tag is 'git' and not release['prerelease'] and self.versiontuple(rVersion) >= self.versiontuple(config.version):
                    print "git (dev/Singularity) -> Stable"
                    wx.CallAfter(self.callback, release)
                elif config.expansionName is not "Singularity": # Current version is a stable release
                    if release['prerelease']:
                        print "Stable -> Singularity"
                        wx.CallAfter(self.callback, release)
                    elif self.versiontuple(rVersion) > self.versiontuple(config.version):
                            print "Stable -> Stable"
                            wx.CallAfter(self.callback, release)
                else: #Current version is pre-release
                    if release['prerelease'] and rVersion > config.expansionVersion:
                            print "Singularity -> Singularity"
                            wx.CallAfter(self.callback, release)
                    else:
                        print "no new release"
                break;
        except: # for when there is no internet connection
            pass

    def versiontuple(self, v):
        return tuple(map(int, (v.split("."))))

class Update():
    instance = None
    def __init__(self):
       pass

    def CheckUpdate(self, callback):
        thread = CheckUpdateThread(callback)
        thread.start()

    @classmethod
    def getInstance(cls):
        if cls.instance == None:
            cls.instance = Update()
        return cls.instance


