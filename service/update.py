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

from service.settings import SettingsProvider

class CheckUpdateThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback

    def run(self):
        print "In the thread"
        try:
            response = urllib2.urlopen('https://api.github.com/repos/DarkFenX/Pyfa/releases')
            jsonResponse = json.loads(response.read());
            responseVersion = jsonResponse[0]['tag_name'].replace('v', '', 1)
            if responseVersion != config.version:
                print "New version!"
                wx.CallAfter(self.callback, jsonResponse[0])
        except:
            pass

class Update():
    instance = None
    def __init__(self):
       pass
       
    def CheckUpdate(self, callback):
        print "Checking for Updates"
        thread = CheckUpdateThread(callback)
        thread.start()

    @classmethod
    def getInstance(cls):
        if cls.instance == None:
            cls.instance = Update()
        return cls.instance

    
