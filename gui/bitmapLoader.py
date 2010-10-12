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

import os.path
import config
import wx

def getStaticBitmap(name, parent, location):
    static = wx.StaticBitmap(parent)
    static.SetBitmap(getBitmap(name,location))
    return static

locationMap = {"pack": os.path.join(config.staticPath, "icons"),
               "ships": os.path.join(config.staticPath, "icons", "ships")}

def getBitmap(name,location):
    icon = getImage(name, location)
    if icon is not None:
        return icon.ConvertToBitmap()

def getImage(name, location):
    if location in locationMap:
        location = locationMap[location]
        path = os.path.join(location, "icon%s.png" % name)
    else:
        location = os.path.join(config.path, location)
        path = os.path.join(location, name + ".png")

    if os.path.exists(path):
        return wx.Image(path)
