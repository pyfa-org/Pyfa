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

import wx


def valToStr(val):
    if val is None:
        return ''
    if int(val) == val:
        val = int(val)
    return str(val)


def strToFloat(val):
    try:
        return float(val)
    except ValueError:
        return None


class ConstantBox(wx.TextCtrl):

    def __init__(self, parent, initial):
        super().__init__(parent, wx.ID_ANY, style=0)
        self.Bind(wx.EVT_TEXT, self.OnText)
        self._storedValue = ''
        self.ChangeValue(valToStr(initial))


    def ChangeValue(self, value):
        self._storedValue = value
        super().ChangeValue(value)

    def OnText(self, event):
        currentValue = self.GetValue()
        if currentValue == self._storedValue:
            event.Skip()
            return
        if currentValue == '' or re.match('^\d*\.?\d*$', currentValue):
            self._storedValue = currentValue
            event.Skip()
        else:
            self.ChangeValue(self._storedValue)

    def GetValueFloat(self):
        return strToFloat(self.GetValue())


class RangeBox(wx.TextCtrl):

    def __init__(self, parent, initialLow, initialHigh):
        super().__init__(parent, wx.ID_ANY, style=0)
        self.Bind(wx.EVT_TEXT, self.OnText)
        self._storedValue = ''
        self.ChangeValue('{}-{}'.format(valToStr(initialLow), valToStr(initialHigh)))

    def ChangeValue(self, value):
        self._storedValue = value
        super().ChangeValue(value)

    def OnText(self, event):
        currentValue = self.GetValue()
        if currentValue == self._storedValue:
            event.Skip()
            return
        if currentValue == '' or re.match('^\d*\.?\d*-?\d*\.?\d*$', currentValue):
            self._storedValue = currentValue
            event.Skip()
        else:
            self.ChangeValue(self._storedValue)

    def GetValueRange(self):
        parts = self.GetValue().split('-')
        if len(parts) == 1:
            val = strToFloat(parts)
            return (val, val)
        else:
            return (strToFloat(parts[0]), strToFloat(parts[1]))
