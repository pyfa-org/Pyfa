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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.    If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
import bitmapLoader
from wx.lib.intctrl import IntCtrl
import service
###########################################################################
## Class DmgPatternEditorDlg
###########################################################################

class DmgPatternEditorDlg (wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id = wx.ID_ANY, title = u"Damage Pattern Editor", size = wx.Size( 350,240 ))

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.headerSizer = headerSizer = wx.BoxSizer(wx.HORIZONTAL)

        cDP = service.DamagePattern.getInstance()

        self.choices = cDP.getDamagePatternList()
        self.choices.sort(key=lambda p: p.name)
        self.ccDmgPattern = wx.Choice(self, choices=map(lambda p: p.name, self.choices))
        self.ccDmgPattern.SetSelection(0)

        self.namePicker = wx.TextCtrl(self)
        self.namePicker.Hide()

        size = None
        headerSizer.Add(self.ccDmgPattern, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT|wx.LEFT, 3)
        buttons = (("new", wx.ART_NEW),
                   ("copy", wx.ART_COPY),
                   ("rename", bitmapLoader.getBitmap("rename", "icons")),
                   ("delete", wx.ART_DELETE))
        for name, art in buttons:
                bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON) if name != "rename" else art
                btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)
                if size is None:
                        size = btn.GetSize()

                btn.SetMinSize(size)
                btn.SetMaxSize(size)

                btn.Layout()
                setattr(self, name, btn)
                btn.Enable(True)
                btn.SetToolTipString("%s fit" % name.capitalize())
                headerSizer.Add(btn, 0, wx.ALIGN_CENTER_VERTICAL)


        mainSizer.Add(headerSizer, 0, wx.EXPAND | wx.ALL, 2)

        self.sl = wx.StaticLine(self)
        mainSizer.Add(self.sl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        contentSizer = wx.BoxSizer(wx.VERTICAL)
        self.embitmap = bitmapLoader.getBitmap("em_big", "icons")
        self.thermbitmap = bitmapLoader.getBitmap("thermal_big", "icons")
        self.kinbitmap = bitmapLoader.getBitmap("kinetic_big", "icons")
        self.expbitmap = bitmapLoader.getBitmap("explosive_big", "icons")

        dmgeditSizer = wx.FlexGridSizer(2, 4, 0, 2)
        dmgeditSizer.AddGrowableCol(1)
        dmgeditSizer.AddGrowableCol(2)
        dmgeditSizer.SetFlexibleDirection(wx.BOTH)
        dmgeditSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        width = -1
        defSize = wx.Size(width,-1)

        self.editEM = IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, wx.TE_RIGHT)
        dmgeditSizer.Add(self.editEM, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bmpEM = wx.StaticBitmap(self, wx.ID_ANY, self.embitmap)
        dmgeditSizer.Add(self.bmpEM, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bmpTHERM = wx.StaticBitmap(self, wx.ID_ANY, self.thermbitmap)
        dmgeditSizer.Add(self.bmpTHERM, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.editTHERM = IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, 0)
        dmgeditSizer.Add(self.editTHERM, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.editKIN = IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, wx.TE_RIGHT)
        dmgeditSizer.Add(self.editKIN, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bmpKIN = wx.StaticBitmap(self, wx.ID_ANY, self.kinbitmap)
        dmgeditSizer.Add(self.bmpKIN, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bmpEXP = wx.StaticBitmap(self, wx.ID_ANY, self.expbitmap)
        dmgeditSizer.Add(self.bmpEXP, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.editEXP = IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, 0)
        dmgeditSizer.Add(self.editEXP, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        contentSizer.Add(dmgeditSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.slfooter = wx.StaticLine(self)
        contentSizer.Add(self.slfooter, 0, wx.EXPAND | wx.TOP, 5)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)

        perSizer = wx.BoxSizer(wx.VERTICAL)

        self.stPercentages = wx.StaticText(self, wx.ID_ANY, u"")
        self.stPercentages.Wrap(-1)
        perSizer.Add(self.stPercentages, 0, wx.BOTTOM | wx.LEFT, 5)

        footerSizer.Add(perSizer, 0, 0, 5)

        self.totSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTotal = wx.StaticText(self, wx.ID_ANY, u"")
        self.stTotal.Wrap(-1)
        self.totSizer.Add(self.stTotal, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 5)

        footerSizer.Add(self.totSizer, 1, 0, 5)

        contentSizer.Add(footerSizer, 0, wx.EXPAND, 5)

        mainSizer.Add(contentSizer, 1, wx.EXPAND, 0)

        self.SetSizer(mainSizer)


        self.Layout()
        self.ValuesUpdated()
        bsize = self.GetBestSize()
        self.SetSize((-1,bsize.height))

        self.editEM.SetLimited(True)
        self.editTHERM.SetLimited(True)
        self.editKIN.SetLimited(True)
        self.editEXP.SetLimited(True)


        self.editEM.SetMin(0)
        self.editTHERM.SetMin(0)
        self.editKIN.setMin(0)
        self.editEXP.SetMin(0)

        self.editEM.SetMax(99999)
        self.editTHERM.SetMax(99999)
        self.editKIN.SetMax(99999)
        self.editEXP.SetMax(99999)


        self.new.Bind(wx.EVT_BUTTON, self.newPattern)
        self.rename.Bind(wx.EVT_BUTTON, self.renamePattern)
        self.delete.Bind(wx.EVT_BUTTON, self.deletePattern)
        self.copy.Bind(wx.EVT_BUTTON, self.copyPattern)

        self.editEM.Bind(wx.EVT_TEXT, self.ValuesUpdated)
        self.editTHERM.Bind(wx.EVT_TEXT, self.ValuesUpdated)
        self.editKIN.Bind(wx.EVT_TEXT, self.ValuesUpdated)
        self.editEXP.Bind(wx.EVT_TEXT, self.ValuesUpdated)

        if self.choices[0].name == "Uniform":
            self.restrict()

    def ValuesUpdated(self, event=None):
        self._EM = self.editEM.GetValue()
        self._THERM = self.editTHERM.GetValue()
        self._KIN = self.editKIN.GetValue()
        self._EXP = self.editEXP.GetValue()
        total = self._EM + self._THERM + self._KIN + self._EXP
        format = "EM: % 3d%% THERM: % 3d%% KIN: % 3d%% EXP: % 3d%%"
        if total > 0:
            ltext = format %(self._EM*100/total, self._THERM*100/total, self._KIN*100/total, self._EXP*100/total)
        else:
            ltext = format %(0, 0, 0, 0)

        ttext = "Total: % 6d" % (total)
        self.stPercentages.SetLabel(ltext)
        self.stTotal.SetLabel(ttext)
        self.totSizer.Layout()

        if event is not None:
            event.Skip()

    def restrict(self):
        self.editEM.Enable(False)
        self.editEXP.Enable(False)
        self.editKIN.Enable(False)
        self.editTHERM.Enable(False)
        self.rename.Enable(False)
        self.delete.Enable(False)

    def unrestrict(self):
        self.editEM.Enable()
        self.editEXP.Enable()
        self.editKIN.Enable()
        self.editTHERM.Enable()
        self.rename.Enable()
        self.delete.Enable()


    def newPattern(self,event):
        cDP = service.DamagePattern.getInstance()
        p = cDP.newPattern()
        self.choices.append(p)
        id = self.ccDmgPattern.Append(p.name)
        self.ccDmgPattern.SetSelection(id)
        self.renamePattern(event)

    def renamePattern(self,event):
        event.Skip()

    def copyPattern(self,event):
        event.Skip()

    def deletePattern(self,event):
        event.Skip()


    def __del__( self ):
                pass
