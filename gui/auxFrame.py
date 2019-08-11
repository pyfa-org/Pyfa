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


# noinspection PyPackageRequirements
import wx


class AuxiliaryFrame(wx.Frame):

    _instance = None

    def __init__(self, parent, id=None, title=None, pos=None, size=None, style=None, name=None):
        baseStyle = wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT | wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU
        kwargs = {
            'parent': parent,
            'style': baseStyle if style is None else baseStyle | style}
        if id is not None:
            kwargs['id'] = id
        if title is not None:
            kwargs['title'] = title
        if pos is not None:
            kwargs['pos'] = pos
        if size is not None:
            kwargs['size'] = size
        if name is not None:
            kwargs['name'] = name
        super().__init__(**kwargs)

    @classmethod
    def openOne(cls, parent):
        if not cls._instance:
            frame = cls(parent)
            cls._instance = frame
            frame.Show()
        else:
            cls._instance.Raise()
