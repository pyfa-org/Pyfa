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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.    If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

# noinspection PyPackageRequirements
import wx
from logbook import Logger
import gc

pyfalog = Logger(__name__)


class DevTools(wx.Dialog):
    DAMAGE_TYPES = ("em", "thermal", "kinetic", "explosive")

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Damage Pattern Editor", size=wx.Size(400, 240))

        self.block = False
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.id_get = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition)
        mainSizer.Add(self.id_get, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        self.idBtn = wx.Button(self, wx.ID_ANY, "Print object", wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.idBtn, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.idBtn.Bind(wx.EVT_BUTTON, self.objects_by_id)

        self.SetSizer(mainSizer)

        self.Layout()
        self.CenterOnParent()
        self.Show()



    def objects_by_id(self, evt):
        input = self.id_get.GetValue()
        if input.startswith("0x"):
            input = int(input, 16)

        print("Finding {} ({})".format(str(input), hex(input)))

        for obj in gc.get_objects():
            if id(obj) == input:
                print(obj)
                print(bool(obj))
                break
        else:
            print(None)
