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

import io
import os.path
import zipfile
from collections import OrderedDict

# noinspection PyPackageRequirements
import wx

import config

import gui.mainFrame as mainFrame

from logbook import Logger
logging = Logger(__name__)


class BitmapLoader(object):
    # try:
    #     archive = zipfile.ZipFile(os.path.join(config.pyfaPath, 'imgs.zip'), 'r')
    #     logging.info("Using zipped image files.")
    # except (IOError, TypeError):
    #     logging.info("Using local image files.")
    #     archive = None

    logging.info("Using local image files.")
    archive = None

    cached_bitmaps = OrderedDict()
    dont_use_cached_bitmaps = False
    max_cached_bitmaps = 500

    @classmethod
    def getStaticBitmap(cls, name, parent, location):
        static = wx.StaticBitmap(parent)
        static.SetBitmap(cls.getBitmap(name or 0, location))
        return static

    @classmethod
    def getBitmap(cls, name, location):
        if cls.dont_use_cached_bitmaps:
            return cls.loadBitmap(name, location)

        path = "%s%s" % (name, location)

        if len(cls.cached_bitmaps) == cls.max_cached_bitmaps:
            cls.cached_bitmaps.popitem(False)

        if path not in cls.cached_bitmaps:
            bmp = cls.loadBitmap(name, location)
            cls.cached_bitmaps[path] = bmp
        else:
            bmp = cls.cached_bitmaps[path]

        return bmp

    @classmethod
    def getImage(cls, name, location):
        return cls.getBitmap(name, location).ConvertToImage()

    @classmethod
    def loadBitmap(cls, name, location):
        filename = "{0}.png".format(name)
        scale = int(mainFrame.MainFrame.getInstance().GetContentScaleFactor())
        if scale == 1:
            img = cls.loadImage(filename, location)
        else:
            filenameScaled = "{0}@{1}x.png".format(name, scale)
            img = cls.loadImage(filenameScaled, location)
            if img is None:
                img = cls.loadImage(filename, location)
                scale = 1
        if img is None:
            return None
        bmp: wx.Bitmap = img.ConvertToBitmap()
        if scale > 1:
            bmp.SetSize((int(bmp.GetWidth()/scale), int(bmp.GetHeight()/scale)))
        return bmp

    @classmethod
    def loadImage(cls, filename, location):
        if cls.archive:
            path = os.path.join(location, filename)
            if os.sep != "/" and os.sep in path:
                path = path.replace(os.sep, "/")

            try:
                img_data = cls.archive.read(path)
                sbuf = io.StringIO(img_data)
                return wx.ImageFromStream(sbuf)
            except KeyError:
                print(("Missing icon file from zip: {0}".format(path)))
        else:
            path = os.path.join(config.pyfaPath, 'imgs' + os.sep + location + os.sep + filename)

            if os.path.exists(path):
                return wx.Image(path)
            else:
                print(("Missing icon file: {0}".format(path)))
