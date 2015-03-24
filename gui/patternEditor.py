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
from service.damagePattern import ImportError

###########################################################################
## Class DmgPatternEditorDlg
###########################################################################

class DmgPatternEditorDlg(wx.Dialog):
    DAMAGE_TYPES = ("em", "thermal", "kinetic", "explosive")

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = u"Damage Pattern Editor", size = wx.Size( 400,240 ))

        self.block = False
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.headerSizer = headerSizer = wx.BoxSizer(wx.HORIZONTAL)

        sDP = service.DamagePattern.getInstance()

        self.choices = sDP.getDamagePatternList()
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

        dmgeditSizer = wx.FlexGridSizer(2, 6, 0, 2)
        dmgeditSizer.AddGrowableCol(0)
        dmgeditSizer.AddGrowableCol(5)
        dmgeditSizer.SetFlexibleDirection(wx.BOTH)
        dmgeditSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        width = -1
        defSize = wx.Size(width,-1)

        for i, type in enumerate(self.DAMAGE_TYPES):
            bmp = wx.StaticBitmap(self, wx.ID_ANY, bitmapLoader.getBitmap("%s_big"%type, "icons"))
            if i%2:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT
                border = 10
            else:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
                border = 5

            # set text edit
            setattr(self, "%sEdit"%type, IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize))
            setattr(self, "%sPerc"%type, wx.StaticText(self, wx.ID_ANY, u"0%"))
            editObj = getattr(self, "%sEdit"%type)

            dmgeditSizer.Add(bmp, 0, style, border)
            dmgeditSizer.Add(editObj, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)
            dmgeditSizer.Add(getattr(self, "%sPerc"%type), 0,  wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

            editObj.Bind(wx.EVT_TEXT, self.ValuesUpdated)
            editObj.SetLimited(True)
            editObj.SetMin(0)
            editObj.SetMax(2000000)

        contentSizer.Add(dmgeditSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.slfooter = wx.StaticLine(self)
        contentSizer.Add(self.slfooter, 0, wx.EXPAND | wx.TOP, 5)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        perSizer = wx.BoxSizer(wx.VERTICAL)

        self.stNotice = wx.StaticText(self, wx.ID_ANY, u"")
        self.stNotice.Wrap(-1)
        perSizer.Add(self.stNotice, 0, wx.BOTTOM | wx.TOP | wx.LEFT, 5)

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

        self.new.Bind(wx.EVT_BUTTON, self.newPattern)
        self.rename.Bind(wx.EVT_BUTTON, self.renamePattern)
        self.copy.Bind(wx.EVT_BUTTON, self.copyPattern)
        self.delete.Bind(wx.EVT_BUTTON, self.deletePattern)
        self.Import.Bind(wx.EVT_BUTTON, self.importPatterns)
        self.Export.Bind(wx.EVT_BUTTON, self.exportPatterns)

        self.patternChanged()

    def closeEvent(self, event):
        self.Destroy()

    def ValuesUpdated(self, event=None):
        if self.block:
            return

        p = self.getActivePattern()
        total = sum(map(lambda attr: getattr(self, "%sEdit"%attr).GetValue(), self.DAMAGE_TYPES))
        for type in self.DAMAGE_TYPES:
                editObj = getattr(self, "%sEdit"%type)
                percObj = getattr(self, "%sPerc"%type)
                setattr(p, "%sAmount"%type, editObj.GetValue())
                percObj.SetLabel("%.1f%%"%(float(editObj.GetValue())*100/total if total > 0 else 0))

        self.totSizer.Layout()

        if event is not None:
            event.Skip()

        service.DamagePattern.getInstance().saveChanges(p)

    def restrict(self):
        for type in self.DAMAGE_TYPES:
            editObj = getattr(self, "%sEdit"%type)
            editObj.Enable(False)
        self.rename.Enable(False)
        self.delete.Enable(False)

    def unrestrict(self):
        for type in self.DAMAGE_TYPES:
            editObj = getattr(self, "%sEdit"%type)
            editObj.Enable()
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

        for field in self.DAMAGE_TYPES:
            edit = getattr(self, "%sEdit" % field)
            amount = getattr(p, "%sAmount" % field)
            edit.SetValue(amount)

        self.block = False
        self.ValuesUpdated()

    def newPattern(self, event):
        self.restrict()
        # reset values
        for type in self.DAMAGE_TYPES:
            editObj = getattr(self, "%sEdit"%type)
            editObj.SetValue(0)

        self.btnSave.SetLabel("Create")
        self.Refresh()
        self.renamePattern()

    def renamePattern(self, event=None):
        if event is not None:
            self.btnSave.SetLabel("Rename")

        self.ccDmgPattern.Hide()
        self.namePicker.Show()
        self.headerSizer.Replace(self.ccDmgPattern, self.namePicker)
        self.namePicker.SetFocus()

        if event is not None:  # Rename mode
            self.btnSave.SetLabel("Rename")
            self.namePicker.SetValue(self.getActivePattern().name)
        else:  # Create mode
            self.namePicker.SetValue("")

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
        self.stNotice.SetLabel("")

        if newName == "":
            self.stNotice.SetLabel("Invalid name.")
            return

        sDP = service.DamagePattern.getInstance()
        if self.btnSave.Label == "Create":
            p = sDP.newPattern()
        else:
            # we are renaming, so get the current selection
            p = self.getActivePattern()

        for pattern in self.choices:
            if pattern.name == newName and p != pattern:
                self.stNotice.SetLabel("Name already used, please choose another")
                return

        sDP.renamePattern(p, newName)

        self.updateChoices(newName)
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
        sDP = service.DamagePattern.getInstance()
        p = sDP.copyPattern(self.getActivePattern())
        self.choices.append(p)
        id = self.ccDmgPattern.Append(p.name)
        self.ccDmgPattern.SetSelection(id)
        self.btnSave.SetLabel("Copy")
        self.renamePattern()
        self.patternChanged()

    def deletePattern(self,event):
        sDP = service.DamagePattern.getInstance()
        sel = self.ccDmgPattern.GetSelection()
        sDP.deletePattern(self.getActivePattern())
        self.ccDmgPattern.Delete(sel)
        self.ccDmgPattern.SetSelection(max(0, sel - 1))
        del self.choices[sel]
        self.patternChanged()

    def __del__( self ):
        pass

    def updateChoices(self, select=None):
        "Gathers list of patterns and updates choice selections"
        sDP = service.DamagePattern.getInstance()
        self.choices = sDP.getDamagePatternList()

        for dp in self.choices:
            if dp.name == "Selected Ammo":  # don't include this special butterfly
                self.choices.remove(dp)

        # Sort the remaining list and continue on
        self.choices.sort(key=lambda p: p.name)
        self.ccDmgPattern.Clear()

        for i, choice in enumerate(map(lambda p: p.name, self.choices)):
            self.ccDmgPattern.Append(choice)

            if select is not None and choice == select:
                self.ccDmgPattern.SetSelection(i)

        if select is None:
            self.ccDmgPattern.SetSelection(0)
        self.patternChanged()

    def importPatterns(self, event):
        text = fromClipboard()
        if text:
            sDP = service.DamagePattern.getInstance()
            try:
                sDP.importPatterns(text)
                self.stNotice.SetLabel("Patterns successfully imported from clipboard")
            except service.damagePattern.ImportError, e:
                self.stNotice.SetLabel(str(e))
            except Exception, e:
                self.stNotice.SetLabel("Could not import from clipboard: unknown errors")
            finally:
                self.updateChoices()
        else:
            self.stNotice.SetLabel("Could not import from clipboard")

    def exportPatterns(self, event):
        sDP = service.DamagePattern.getInstance()
        toClipboard( sDP.exportPatterns() )
        self.stNotice.SetLabel("Patterns exported to clipboard")
