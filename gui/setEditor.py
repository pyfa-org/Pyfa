#===============================================================================
# Copyright (C) 2016 Ryan Holmes
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
from gui.bitmapLoader import BitmapLoader
from gui.builtinViews.implantEditor import BaseImplantEditorView
import service
from gui.utils.clipboard import toClipboard, fromClipboard
from service.targetResists import ImportError

class ImplantSetEditor(BaseImplantEditorView):
    def __init__(self, parent):
        BaseImplantEditorView.__init__(self, parent)

    def bindContext(self):
        self.Parent.ccSets.Bind(wx.EVT_CHOICE, self.contextChanged)

    def getImplantsFromContext(self):
        sIS = service.ImplantSets.getInstance()
        setID = self.Parent.getActiveSet()

        return sIS.getImplants(setID)

    def addImplantToContext(self, item):
        sIS = service.ImplantSets.getInstance()
        setID = self.Parent.getActiveSet()

        sIS.addImplant(setID, item.ID)

    def removeImplantFromContext(self, pos):
        sIS = service.ImplantSets.getInstance()
        setID = self.Parent.getActiveSet()

        sIS.removeImplant(setID, self.implants[pos])


class ImplantSetEditorDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = u"Implant Set Editor", size = wx.Size(640, 600))

        self.block = False
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.headerSizer = headerSizer = wx.BoxSizer(wx.HORIZONTAL)

        sIS = service.ImplantSets.getInstance()

        self.choices = sIS.getImplantSetList()

        # Sort the remaining list and continue on
        self.choices.sort(key=lambda s: s.name)
        self.ccSets = wx.Choice(self, wx.ID_ANY, style=0)

        for set in self.choices:
            i = self.ccSets.Append(set.name, set.ID)

        self.ccSets.Bind(wx.EVT_CHOICE, self.setChanged)
        self.ccSets.SetSelection(0)

        self.namePicker = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.namePicker.Bind(wx.EVT_TEXT_ENTER, self.processRename)
        self.namePicker.Hide()

        size = None
        headerSizer.Add(self.ccSets, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT, 3)

        buttons = (("new", wx.ART_NEW),
                   ("rename", BitmapLoader.getBitmap("rename", "gui")),
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
                #btn.SetToolTipString("%s resist profile" % name.capitalize())
                headerSizer.Add(btn, 0, wx.ALIGN_CENTER_VERTICAL)


        self.btnSave = wx.Button(self, wx.ID_SAVE)
        self.btnSave.Hide()
        self.btnSave.Bind(wx.EVT_BUTTON, self.processRename)
        headerSizer.Add(self.btnSave, 0, wx.ALIGN_CENTER)

        mainSizer.Add(headerSizer, 0, wx.EXPAND | wx.ALL, 2)

        self.sl = wx.StaticLine(self)
        mainSizer.Add(self.sl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.iview = ImplantSetEditor(self)
        mainSizer.Add(self.iview, 0, wx.EXPAND)

        contentSizer = wx.BoxSizer(wx.VERTICAL)

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

    def closeEvent(self, event):
        self.Destroy()

    def getActiveSet(self):
        selection = self.ccSets.GetCurrentSelection()
        return self.ccSets.GetClientData(selection) if selection is not None else None

    def ValuesUpdated(self, event=None):
        '''
        Event that is fired when resists values change. Iterates through all
        resist edit fields. If blank, sets it to 0.0. If it is not a proper
        decimal value, sets text color to red and refuses to save changes until
        issue is resolved
        '''
        if self.block:
            return

        try:
            p = self.getActivePattern()

            for type in self.DAMAGE_TYPES:
                editObj = getattr(self, "%sEdit"%type)

                if editObj.GetValue() == "":
                    # if we are blank, overwrite with 0
                    editObj.ChangeValue("0.0")
                    editObj.SetInsertionPointEnd()

                value = float(editObj.GetValue())

                # assertion, because they're easy
                assert 0 <= value <= 100

                # if everything checks out, set resist attribute
                setattr(p, "%sAmount"%type, value/100)
                editObj.SetForegroundColour(self.colorReset)

            self.stNotice.SetLabel("")
            self.totSizer.Layout()

            if event is not None:
                event.Skip()

            service.TargetResists.getInstance().saveChanges(p)

        except ValueError:
            editObj.SetForegroundColour(wx.RED)
            self.stNotice.SetLabel("Incorrect Formatting (decimals only)")
        except AssertionError:
            editObj.SetForegroundColour(wx.RED)
            self.stNotice.SetLabel("Incorrect Range (must be 0-100)")
        finally:  # Refresh for color changes to take effect immediately
            self.Refresh()

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

        return self.choices[self.ccSets.GetSelection()]

    def setChanged(self, event=None):
        "Event fired when user selects pattern. Can also be called from script"
        p = self.getActivePattern()
        if p is None:
            # This happens when there are no patterns in the DB. As such, force
            # user to create one first or exit dlg.
            self.newPattern(None)
            return

        #ValuesUpdated()

    def newPattern(self, event):
        '''
        Simply does new-pattern specifics: replaces label on button, restricts,
        and resets values to default. Hands off to the rename function for
        further handling.
        '''
        self.btnSave.SetLabel("Create")
        self.restrict()
        # reset values
        for type in self.DAMAGE_TYPES:
            editObj = getattr(self, "%sEdit"%type)
            editObj.ChangeValue("0.0")
            editObj.SetForegroundColour(self.colorReset)

        self.Refresh()
        self.renamePattern()

    def renamePattern(self, event=None):
        "Changes layout to facilitate naming a pattern"

        self.showInput(True)

        if event is not None:  # Rename mode
            self.btnSave.SetLabel("Rename")
            self.namePicker.SetValue(self.getActivePattern().name)
        else:  # Create mode
            self.namePicker.SetValue("")

        if event is not None:
            event.Skip()

    def processRename(self, event):
        '''
        Processes rename event (which can be new or old patterns). If new
        pattern, creates it; if old, selects it. if checks are valid, rename
        saves pattern to DB.

        Also resets to default layout and unrestricts.
        '''
        newName = self.namePicker.GetLineText(0)
        self.stNotice.SetLabel("")

        if newName == "":
            self.stNotice.SetLabel("Invalid name")
            return

        sTR = service.TargetResists.getInstance()
        if self.btnSave.Label == "Create":
            p = sTR.newPattern()
        else:
            # we are renaming, so get the current selection
            p = self.getActivePattern()

        # test for patterns of the same name
        for pattern in self.choices:
            if pattern.name == newName and p != pattern:
                self.stNotice.SetLabel("Name already used, please choose another")
                return

        # rename regardless of new or rename
        sTR.renamePattern(p, newName)

        self.updateChoices(newName)
        self.showInput(False)
        sel = self.ccSets.GetSelection()
        self.ValuesUpdated()
        self.unrestrict()

    def copyPattern(self,event):
        sTR = service.TargetResists.getInstance()
        p = sTR.copyPattern(self.getActivePattern())
        self.choices.append(p)
        id = self.ccSets.Append(p.name)
        self.ccSets.SetSelection(id)
        self.btnSave.SetLabel("Copy")
        self.renamePattern()
        self.setChanged()

    def deletePattern(self,event):
        sTR = service.TargetResists.getInstance()
        sel = self.ccSets.GetSelection()
        sTR.deletePattern(self.getActivePattern())
        self.ccSets.Delete(sel)
        self.ccSets.SetSelection(max(0, sel - 1))
        del self.choices[sel]
        self.setChanged()

    def showInput(self, bool):
        if bool and not self.namePicker.IsShown():
            self.ccSets.Hide()
            self.namePicker.Show()
            self.headerSizer.Replace(self.ccSets, self.namePicker)
            self.namePicker.SetFocus()
            for btn in (self.new, self.rename, self.delete, self.copy):
                btn.Hide()
            self.btnSave.Show()
            self.restrict()
            self.headerSizer.Layout()
        elif not bool and self.namePicker.IsShown():
            self.headerSizer.Replace(self.namePicker, self.ccSets)
            self.ccSets.Show()
            self.namePicker.Hide()
            self.btnSave.Hide()
            for btn in (self.new, self.rename, self.delete, self.copy):
                btn.Show()
            self.unrestrict()
            self.headerSizer.Layout()


    def __del__( self ):
        pass

    def updateChoices(self, select=None):
        "Gathers list of patterns and updates choice selections"
        sTR = service.TargetResists.getInstance()
        self.choices = sTR.getTargetResistsList()

        if len(self.choices) == 0:
            #self.newPattern(None)
            return

        # Sort the remaining list and continue on
        self.choices.sort(key=lambda p: p.name)
        self.ccSets.Clear()

        for i, choice in enumerate(map(lambda p: p.name, self.choices)):
            self.ccSets.Append(choice)

            if select is not None and choice == select:
                self.ccSets.SetSelection(i)

        if select is None:
            self.ccSets.SetSelection(0)

        self.setChanged()

    def importPatterns(self, event):
        "Event fired when import from clipboard button is clicked"

        text = fromClipboard()
        if text:
            sTR = service.TargetResists.getInstance()
            try:
                sTR.importPatterns(text)
                self.stNotice.SetLabel("Patterns successfully imported from clipboard")
                self.showInput(False)
            except service.targetResists.ImportError, e:
                self.stNotice.SetLabel(str(e))
            except Exception, e:
                self.stNotice.SetLabel("Could not import from clipboard: unknown errors")
            finally:
                self.updateChoices()
        else:
            self.stNotice.SetLabel("Could not import from clipboard")

    def exportPatterns(self, event):
        "Event fired when export to clipboard button is clicked"

        sTR = service.TargetResists.getInstance()
        toClipboard( sTR.exportPatterns() )
        self.stNotice.SetLabel("Patterns exported to clipboard")
