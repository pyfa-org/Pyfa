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
        self.settings =  service.settings.UpdateSettings.getInstance()

    def run(self):
        # Suppress all
        if (self.settings.get('all')):
            return

        try:
            response = urllib2.urlopen('https://api.github.com/repos/DarkFenX/Pyfa/releases')
            jsonResponse = json.loads(response.read());
            i = 0
            while (True):
                release = jsonResponse[i]

                # Suppress pre releases
                if (release['prerelease'] and self.settings.get('prerelease')):
                    i += 1
                    continue
                
                # Handle use-case of updating to suppressed version
                if self.settings.get('version') == 'v'+config.version:
                    self.settings.set('version', None)
                
                # Suppress version
                if (release['tag_name'] == self.settings.get('version')):
                    return                
                    
                version = release['tag_name'].replace('v', '', 1)
                if version != config.version:
                    wx.CallAfter(self.callback, jsonResponse[i])
                    break;
                
        except: # for when there is no internet connection
            pass
    
    def versiontuple(v):
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

    
