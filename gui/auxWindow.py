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


class AuxiliaryMixin:

    _instance = None

    def __init__(self, parent, id=None, title=None, pos=None, size=None, style=None, name=None, resizeable=False):
        baseStyle = wx.FRAME_NO_TASKBAR | wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU
        if parent is not None:
            baseStyle = baseStyle | wx.FRAME_FLOAT_ON_PARENT
        if resizeable:
            baseStyle = baseStyle | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
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
        # Intercept copy-paste actions and do nothing in secondary windows,
        # otherwise on Mac OS X Cmd-C brings up copy fit dialog
        if 'wxMac' in wx.PlatformInfo:
            self.Bind(wx.EVT_MENU, self.OnSuppressedAction, id=wx.ID_COPY)
            self.Bind(wx.EVT_MENU, self.OnSuppressedAction, id=wx.ID_PASTE)
        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

    @classmethod
    def openOne(cls, parent, *args, forceReopen=False, **kwargs):
        """If window is open and alive - raise it, open otherwise"""
        if not cls._instance or forceReopen:
            if cls._instance:
                cls._instance.Close()
            frame = cls(parent, *args, **kwargs)
            cls._instance = frame
            frame.Show()
        else:
            cls._instance.Raise()
        return cls._instance


    def OnSuppressedAction(self, event):
        return


class AuxiliaryFrame(AuxiliaryMixin, wx.Frame):
    pass


class AuxiliaryDialog(AuxiliaryMixin, wx.Dialog):
    pass
