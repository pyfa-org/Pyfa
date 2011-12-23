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
import service
from wx.lib.intctrl import IntCtrl
from gui.utils.clipboard import toClipboard, fromClipboard

###########################################################################
## Class DmgPatternEditorDlg
###########################################################################

class DmgPatternEditorDlg (wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id = wx.ID_ANY, title = u"Damage Pattern Editor", size = wx.Size( 400,240 ))

        self.block = False
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.headerSizer = headerSizer = wx.BoxSizer(wx.HORIZONTAL)

        cDP = service.DamagePattern.getInstance()

        self.choices = cDP.getDamagePatternList()
        # Remove "Selected Ammo" Damage Pattern
        for dp in self.choices:
            if dp.name == "Selected Ammo":
                self.choices.remove(dp)
        # Sort the remaining list and continue on
        self.choices.sort(key=lambda p: p.name)
        self.ccDmgPattern = wx.Choice(self, choices=map(lambda p: p.name, self.choices))
        self.ccDmgPattern.Bind(wx.EVT_CHOICE, self.patternChanged)
        self.ccDmgPattern.SetSelection(0)

        self.namePicker = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.namePicker.Bind(wx.EVT_TEXT_ENTER, self.processRename)
        self.namePicker.Hide()

        self.btnSave = wx.Button(self, wx.ID_SAVE)
        self.btnSave.Hide()
        self.btnSave.Bind(wx.EVT_BUTTON, self.processRename)

        size = None
        headerSizer.Add(self.ccDmgPattern, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT|wx.LEFT, 3)
        buttons = (("new", wx.ART_NEW),
                   ("rename", bitmapLoader.getBitmap("rename", "icons")),
                   ("copy", wx.ART_COPY),
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
                btn.SetToolTipString("%s pattern" % name.capitalize())
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
        dmgeditSizer.AddGrowableCol(0)
        dmgeditSizer.AddGrowableCol(3)
        dmgeditSizer.SetFlexibleDirection(wx.BOTH)
        dmgeditSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        width = -1
        defSize = wx.Size(width,-1)

        self.bmpEM = wx.StaticBitmap(self, wx.ID_ANY, self.embitmap)
        dmgeditSizer.Add(self.bmpEM, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        self.editEm = IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize)
        dmgeditSizer.Add(self.editEm, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bmpTHERM = wx.StaticBitmap(self, wx.ID_ANY, self.thermbitmap)
        dmgeditSizer.Add(self.bmpTHERM, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT, 25)
        self.editThermal = IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, 0)
        dmgeditSizer.Add(self.editThermal, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bmpKIN = wx.StaticBitmap(self, wx.ID_ANY, self.kinbitmap)
        dmgeditSizer.Add(self.bmpKIN, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        self.editKinetic = IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize)
        dmgeditSizer.Add(self.editKinetic, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bmpEXP = wx.StaticBitmap(self, wx.ID_ANY, self.expbitmap)
        dmgeditSizer.Add(self.bmpEXP, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT, 25)
        self.editExplosive = IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize, 0)
        dmgeditSizer.Add(self.editExplosive, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)

        contentSizer.Add(dmgeditSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.slfooter = wx.StaticLine(self)
        contentSizer.Add(self.slfooter, 0, wx.EXPAND | wx.TOP, 5)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        perSizer = wx.BoxSizer(wx.VERTICAL)

        self.stPercentages = wx.StaticText(self, wx.ID_ANY, u"")
        self.stPercentages.Wrap(-1)
        perSizer.Add(self.stPercentages, 0, wx.BOTTOM | wx.TOP | wx.LEFT, 5)

        footerSizer.Add(perSizer, 1,  wx.ALIGN_CENTER_VERTICAL, 5)

        self.totSizer = wx.BoxSizer(wx.VERTICAL)

        contentSizer.Add(footerSizer, 0, wx.EXPAND, 5)

        mainSizer.Add(contentSizer, 1, wx.EXPAND, 0)

        if "wxGTK" in wx.PlatformInfo:
            self.closeBtn = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
            mainSizer.Add( self.closeBtn, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
            self.closeBtn.Bind(wx.EVT_BUTTON, self.closeEvent)

        self.SetSizer(mainSizer)

        importExport = (("Import", wx.ART_FILE_OPEN, "from"),
                        ("Export", wx.ART_FILE_SAVE_AS, "to"))
        for name, art, direction in importExport:
                bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON)
                btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)

                btn.SetMinSize( btn.GetSize() )
                btn.SetMaxSize( btn.GetSize() )

                btn.Layout()
                setattr(self, name, btn)
                btn.Enable(True)
                btn.SetToolTipString("%s patterns %s clipboard" % (name, direction) )
                footerSizer.Add(btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_RIGHT)

        self.Layout()
        bsize = self.GetBestSize()
        self.SetSize((-1,bsize.height))

        self.editEm.SetLimited(True)
        self.editThermal.SetLimited(True)
        self.editKinetic.SetLimited(True)
        self.editExplosive.SetLimited(True)

        self.editEm.SetMin(0)
        self.editThermal.SetMin(0)
        self.editKinetic.SetMin(0)
        self.editExplosive.SetMin(0)

        self.editEm.SetMax(99999)
        self.editThermal.SetMax(99999)
        self.editKinetic.SetMax(99999)
        self.editExplosive.SetMax(99999)


        self.new.Bind(wx.EVT_BUTTON, self.newPattern)
        self.rename.Bind(wx.EVT_BUTTON, self.renamePattern)
        self.copy.Bind(wx.EVT_BUTTON, self.copyPattern)
        self.delete.Bind(wx.EVT_BUTTON, self.deletePattern)
        self.Import.Bind(wx.EVT_BUTTON, self.importPatterns)
        self.Export.Bind(wx.EVT_BUTTON, self.exportPatterns)

        self.editEm.Bind(wx.EVT_TEXT, self.ValuesUpdated)
        self.editThermal.Bind(wx.EVT_TEXT, self.ValuesUpdated)
        self.editKinetic.Bind(wx.EVT_TEXT, self.ValuesUpdated)
        self.editExplosive.Bind(wx.EVT_TEXT, self.ValuesUpdated)

        self.patternChanged()

    def closeEvent(self, event):
        self.Destroy()

    def ValuesUpdated(self, event=None):
        if self.block:
            return

        p = self.getActivePattern()
        p.emAmount = self._EM = self.editEm.GetValue()
        p.thermalAmount = self._THERM = self.editThermal.GetValue()
        p.kineticAmount = self._KIN = self.editKinetic.GetValue()
        p.explosiveAmount = self._EXP = self.editExplosive.GetValue()
        total = self._EM + self._THERM + self._KIN + self._EXP
        format = "EM: %d%%,    THERM: %d%%,    KIN: %d%%,    EXP: %d%%"
        if total > 0:
            ltext = format %(self._EM*100/total, self._THERM*100/total, self._KIN*100/total, self._EXP*100/total)
        else:
            ltext = format %(0, 0, 0, 0)

        self.stPercentages.SetLabel(ltext)
        self.totSizer.Layout()

        if event is not None:
            event.Skip()

        service.DamagePattern.getInstance().saveChanges(p)

    def restrict(self):
        self.editEm.Enable(False)
        self.editExplosive.Enable(False)
        self.editKinetic.Enable(False)
        self.editThermal.Enable(False)
        self.rename.Enable(False)
        self.delete.Enable(False)

    def unrestrict(self):
        self.editEm.Enable()
        self.editExplosive.Enable()
        self.editKinetic.Enable()
        self.editThermal.Enable()
        self.rename.Enable()
        self.delete.Enable()

    def getActivePattern(self):
        if len(self.choices) == 0:
            return None

        return self.choices[self.ccDmgPattern.GetSelection()]

    def patternChanged(self, event=None):
        p = self.getActivePattern()
        if p is None:
            return

        if p.name == "Uniform" or p.name == "Selected Ammo":
            self.restrict()
        else:
            self.unrestrict()

        self.block = True
        for field in ("em", "thermal", "kinetic", "explosive"):
            edit = getattr(self, "edit%s" % field.capitalize())
            amount = getattr(p, "%sAmount" % field)
            edit.SetValue(amount)

        self.block = False
        self.ValuesUpdated()

    def newPattern(self,event):
        cDP = service.DamagePattern.getInstance()
        p = cDP.newPattern()
        self.choices.append(p)
        id = self.ccDmgPattern.Append(p.name)
        self.ccDmgPattern.SetSelection(id)
        self.btnSave.SetLabel("Create")
        self.renamePattern()

    def renamePattern(self,event=None):
        if event is not None:
            self.btnSave.SetLabel("Rename")

        self.ccDmgPattern.Hide()
        self.namePicker.Show()
        self.headerSizer.Replace(self.ccDmgPattern, self.namePicker)
        self.namePicker.SetFocus()
        self.namePicker.SetValue(self.getActivePattern().name)

        for btn in (self.new, self.rename, self.delete, self.copy):
            btn.Hide()
            self.headerSizer.Remove(btn)

        self.headerSizer.Add(self.btnSave, 0, wx.ALIGN_CENTER)
        self.btnSave.Show()
        self.headerSizer.Layout()
        if event is not None:
            event.Skip()

    def processRename(self, event):
        newName = self.namePicker.GetLineText(0)
        self.stPercentages.SetLabel("")

        p = self.getActivePattern()
        for pattern in self.choices:
            if pattern.name == newName and p != pattern:
                self.stPercentages.SetLabel("Name already used, please pick another")
                return

        if newName == "":
            self.stPercentages.SetLabel("Invalid name.")
            return

        cDP = service.DamagePattern.getInstance()
        cDP.renamePattern(p, newName)

        self.headerSizer.Replace(self.namePicker, self.ccDmgPattern)
        self.ccDmgPattern.Show()
        self.namePicker.Hide()
        self.btnSave.Hide()
        self.headerSizer.Remove(self.btnSave)
        for btn in (self.new, self.rename, self.delete, self.copy):
            self.headerSizer.Add(btn, 0, wx.ALIGN_CENTER_VERTICAL)
            btn.Show()

        sel = self.ccDmgPattern.GetSelection()
        self.ccDmgPattern.Delete(sel)
        self.ccDmgPattern.Insert(newName, sel)
        self.ccDmgPattern.SetSelection(sel)
        self.ValuesUpdated()
        self.unrestrict()

    def copyPattern(self,event):
        cDP = service.DamagePattern.getInstance()
        p = cDP.copyPattern(self.getActivePattern())
        self.choices.append(p)
        id = self.ccDmgPattern.Append(p.name)
        self.ccDmgPattern.SetSelection(id)
        self.btnSave.SetLabel("Copy")
        self.renamePattern()
        self.patternChanged()

    def deletePattern(self,event):
        cDP = service.DamagePattern.getInstance()
        sel = self.ccDmgPattern.GetSelection()
        cDP.deletePattern(self.getActivePattern())
        self.ccDmgPattern.Delete(sel)
        self.ccDmgPattern.SetSelection(max(0, sel - 1))
        del self.choices[sel]
        self.patternChanged()

    def __del__( self ):
        pass

    def importPatterns(self, event):
        text = fromClipboard()
        if text:
            sDP = service.DamagePattern.getInstance()
            sDP.importPatterns(text)
            self.stPercentages.SetLabel("Patterns imported from clipboard")
        else:
            self.stPercentages.SetLabel("Could not import from clipboard")

    def exportPatterns(self, event):
        sDP = service.DamagePattern.getInstance()
        toClipboard( sDP.exportPatterns() )
        self.stPercentages.SetLabel("Patterns exported to clipboard")
