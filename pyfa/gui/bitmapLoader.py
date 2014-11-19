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
import time

try:
    from collections import OrderedDict
except ImportError:
    from gui.utils.compat import OrderedDict

cachedBitmapsCount = 0
cachedBitmaps = OrderedDict()
dontUseCachedBitmaps = False

def getStaticBitmap(name, parent, location):
    static = wx.StaticBitmap(parent)
    static.SetBitmap(getBitmap(name,location))
    return static

locationMap = {"pack": os.path.join(config.staticPath, "icons"),
               "ships": os.path.join(config.staticPath, "icons/ships")}

def getBitmap(name,location):

    global cachedBitmaps
    global cachedBitmapsCount
    global dontUseCachedBitmaps

    if dontUseCachedBitmaps:
        img = getImage(name, location)
        if img is not None:
            return img.ConvertToBitmap()

    path = "%s%s" % (name,location)
    MAX_BMPS = 500
#    start = time.clock()
    if cachedBitmapsCount == MAX_BMPS:
        cachedBitmaps.popitem(False)
        cachedBitmapsCount -=1

    if path not in cachedBitmaps:
        img = getImage(name, location)
        if img is not None:
            bmp = img.ConvertToBitmap()
        else:
            bmp = None
        cachedBitmaps[path] = bmp
        cachedBitmapsCount += 1
    else:
        bmp = cachedBitmaps[path]

#    print "#BMPs:%d - Current took: %.8f" % (cachedBitmapsCount,time.clock() - start)
    return bmp

def getImage(name, location):
    if location in locationMap:
        if location == "pack":
            location = locationMap[location]
            filename = "icon{0}.png".format(name)
            path = os.path.join(location, filename)
        else:
            location = locationMap[location]
            filename = "{0}.png".format(name)
            path = os.path.join(location, filename)

    else:
        location = os.path.join(config.pyfaPath, location)
        filename = "{0}.png".format(name)
        path = os.path.join(location, filename)

    if os.path.exists(path):
        return wx.Image(path)
    else:
        print "Missing icon file: {0}".format(filename)
