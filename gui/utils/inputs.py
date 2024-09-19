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


import re
from abc import ABCMeta, abstractmethod

import wx

from eos.utils.float import floatUnerr


def valToStr(val):
    if val is None:
        return ''
    val = floatUnerr(val)
    if int(val) == val:
        val = int(val)
    return str(val)


def strToFloat(val):
    try:
        return float(val)
    except ValueError:
        return None


class InputValidator(metaclass=ABCMeta):

    def validate(self, value):
        return self._validateWithReason(value)[0]

    def getReason(self, value):
        return self._validateWithReason(value)[1]

    @abstractmethod
    def _validateWithReason(self, value):
        raise NotImplementedError


class FloatBox(wx.TextCtrl):

    def __init__(self, parent, value, id=wx.ID_ANY, style=0, validator=None, **kwargs):
        # Workaround for #2591
        if 'wxMac' in wx.PlatformInfo and 'size' not in kwargs:
            kwargs['size'] = wx.Size(97, 26)
        super().__init__(parent=parent, id=id, style=style, **kwargs)
        self.Bind(wx.EVT_TEXT, self.OnText)
        self._storedValue = ''
        self._validator = validator
        self.ChangeValue(valToStr(value))

    def ChangeValue(self, value):
        self._storedValue = value
        super().ChangeValue(value)
        self.updateColor()

    def ChangeValueFloat(self, value):
        self.ChangeValue(valToStr(value))

    def updateColor(self):
        if self.isValid():
            self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        else:
            self.SetForegroundColour(wx.RED)

    def isValid(self):
        if self._validator is None:
            return True
        return self._validator.validate(self.GetValue())

    def getInvalidationReason(self):
        if self._validator is None:
            return None
        return self._validator.getReason(self.GetValue())

    def OnText(self, event):
        currentValue = self.GetValue()
        if currentValue == self._storedValue:
            event.Skip()
            return
        if currentValue == '' or re.match(r'^\d*\.?\d*$', currentValue):
            self._storedValue = currentValue
            self.updateColor()
            event.Skip()
        else:
            self.ChangeValue(self._storedValue)

    def GetValueFloat(self):
        return strToFloat(self.GetValue())


class FloatRangeBox(wx.TextCtrl):

    def __init__(self, parent, value, id=wx.ID_ANY, style=0, **kwargs):
        # Workaround for #2591
        if 'wxMac' in wx.PlatformInfo and 'size' not in kwargs:
            kwargs['size'] = wx.Size(97, 26)
        super().__init__(parent=parent, id=id, style=style, **kwargs)
        self.Bind(wx.EVT_TEXT, self.OnText)
        self._storedValue = ''
        value = [v for v in value if v is not None]
        if not value:
            self.ChangeValue('')
        else:
            self.ChangeValue('{}-{}'.format(valToStr(min(value)), valToStr(max(value))))

    def ChangeValue(self, value):
        self._storedValue = value
        super().ChangeValue(value)

    def OnText(self, event):
        currentValue = self.GetValue()
        if currentValue == self._storedValue:
            event.Skip()
            return
        if currentValue == '' or re.match(r'^\d*\.?\d*-?\d*\.?\d*$', currentValue):
            self._storedValue = currentValue
            event.Skip()
        else:
            self.ChangeValue(self._storedValue)

    def GetValueRange(self):
        parts = self.GetValue().split('-')
        if len(parts) == 1:
            val = strToFloat(parts[0])
            return (val, val)
        else:
            return (strToFloat(parts[0]), strToFloat(parts[1]))
