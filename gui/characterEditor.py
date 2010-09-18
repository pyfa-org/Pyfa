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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
import gui.mainFrame
import wx.lib.newevent
import wx.gizmos
from gui import bitmapLoader
import service
import sys

CharListUpdated, CHAR_LIST_UPDATED = wx.lib.newevent.NewEvent()

class CharacterEditor(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"pyfa: Character Editor", pos=wx.DefaultPosition,
                            size=wx.Size(641, 600), style=wx.CAPTION | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetSizeHintsSz(wx.Size(640, 600), wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.navSizer = wx.BoxSizer(wx.HORIZONTAL)

        cChar = service.Character.getInstance()
        charList = cChar.getCharacterList()

        self.btnSave = wx.Button(self, wx.ID_SAVE)
        self.btnSave.Hide()
        self.btnSave.Bind(wx.EVT_BUTTON, self.processRename)

        self.characterRename = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.characterRename.Hide()
        self.characterRename.Bind(wx.EVT_TEXT_ENTER, self.processRename)

        self.skillTreeChoice = wx.Choice(self, wx.ID_ANY, style=0)

        for id, name in charList:
            self.skillTreeChoice.Append(name, id)

        self.skillTreeChoice.SetSelection(0)

        self.navSizer.Add(self.skillTreeChoice, 1, wx.ALL | wx.EXPAND, 5)

        buttons = (("new", wx.ART_NEW),
                   ("copy", wx.ART_COPY),
                   ("rename", bitmapLoader.getBitmap("rename", "icons")),
                   ("delete", wx.ART_DELETE))

        size = None
        for name, art in buttons:
            bitmap = wx.ArtProvider.GetBitmap(art) if isinstance(art, unicode) else art
            btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)
            if size is None:
                size = btn.GetSize()

            btn.SetMinSize(size)
            btn.SetMaxSize(size)

            btn.SetToolTipString("%s character" % name.capitalize())
            btn.Bind(wx.EVT_BUTTON, getattr(self, name))
            setattr(self, "btn%s" % name.capitalize(), btn)
            self.navSizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)


        mainSizer.Add(self.navSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.viewsNBContainer = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        self.sview = SkillTreeView(self.viewsNBContainer)
        self.iview = ImplantsTreeView(self.viewsNBContainer)
        self.aview = APIView(self.viewsNBContainer)

        self.viewsNBContainer.AddPage(self.sview, "Skills")
        self.viewsNBContainer.AddPage(self.iview, "Implants")
        self.viewsNBContainer.AddPage(self.aview, "API")

        mainSizer.Add(self.viewsNBContainer, 1, wx.EXPAND | wx.ALL, 5)

        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.btnOK = wx.Button(self, wx.ID_OK)
        bSizerButtons.Add(self.btnOK, 0, wx.ALL, 5)
        self.btnOK.Bind(wx.EVT_BUTTON, self.editingFinished)

        mainSizer.Add(bSizerButtons, 0, wx.ALIGN_RIGHT, 5)


        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        charID = self.getActiveCharacter()
        if cChar.getCharName(charID) == "All 0":
            self.restrict()

        self.registerEvents()

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def editingFinished(self, event):
        wx.PostEvent(self.mainFrame, CharListUpdated())
        event.Skip()

    def registerEvents(self):
        self.Bind(wx.EVT_CLOSE, self.closeEvent)
        self.skillTreeChoice.Bind(wx.EVT_CHOICE, self.charChanged)

    def closeEvent(self, event):
        pass

    def restrict(self):
        self.btnRename.Enable(False)
        self.btnDelete.Enable(False)
        self.aview.inputID.Enable(False)
        self.aview.inputKey.Enable(False)
        self.aview.btnFetchCharList.Enable(False)

    def unrestrict(self):
        self.btnRename.Enable(True)
        self.btnDelete.Enable(True)
        self.aview.inputID.Enable(True)
        self.aview.inputKey.Enable(True)
        self.aview.btnFetchCharList.Enable(True)

    def charChanged(self, event):
        self.sview.skillTreeListCtrl.DeleteChildren(self.sview.root)
        self.sview.populateSkillTree()
        cChar = service.Character.getInstance()
        charID = self.getActiveCharacter()
        if cChar.getCharName(charID) in ("All 0", "All 5"):
            self.restrict()
        else:
            self.unrestrict()

    def getActiveCharacter(self):
        selection = self.skillTreeChoice.GetCurrentSelection()
        return self.skillTreeChoice.GetClientData(selection) if selection is not None else None

    def new(self, event):
        cChar = service.Character.getInstance()
        charID = cChar.new()
        id = self.skillTreeChoice.Append(cChar.getCharName(charID), charID)
        self.skillTreeChoice.SetSelection(id)
        self.unrestrict()
        self.btnSave.SetLabel("Create")
        self.rename(None)
        self.charChanged(None)

    def rename(self, event):
        if event is not None:
            self.btnSave.SetLabel("Rename")
        self.skillTreeChoice.Hide()
        self.characterRename.Show()
        self.navSizer.Replace(self.skillTreeChoice, self.characterRename)
        self.characterRename.SetFocus()
        for btn in (self.btnNew, self.btnCopy, self.btnRename, self.btnDelete):
            btn.Hide()
            self.navSizer.Remove(btn)

        self.btnSave.Show()
        self.navSizer.Add(self.btnSave, 0, wx.ALIGN_CENTER)
        self.navSizer.Layout()

        cChar = service.Character.getInstance()
        currName = cChar.getCharName(self.getActiveCharacter())
        self.characterRename.SetValue(currName)
        self.characterRename.SetSelection(0, len(currName))

    def processRename(self, event):
        cChar = service.Character.getInstance()
        newName = self.characterRename.GetLineText(0)
        charID = self.getActiveCharacter()
        cChar.rename(charID, newName)

        self.skillTreeChoice.Show()
        self.characterRename.Hide()
        self.navSizer.Replace(self.characterRename, self.skillTreeChoice)
        for btn in (self.btnNew, self.btnCopy, self.btnRename, self.btnDelete):
            btn.Show()
            self.navSizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)

        self.navSizer.Remove(self.btnSave)
        self.btnSave.Hide()
        self.navSizer.Layout()
        selection = self.skillTreeChoice.GetCurrentSelection()
        self.skillTreeChoice.Delete(selection)
        self.skillTreeChoice.Insert(newName, selection, charID)
        self.skillTreeChoice.SetSelection(selection)

    def copy(self, event):
        cChar = service.Character.getInstance()
        charID = cChar.copy(self.getActiveCharacter())
        id = self.skillTreeChoice.Append(cChar.getCharName(charID), charID)
        self.skillTreeChoice.SetSelection(id)
        self.unrestrict()
        self.btnSave.SetLabel("Copy")
        self.rename(None)

    def delete(self, event):
        cChar = service.Character.getInstance()
        cChar.delete(self.getActiveCharacter())
        sel = self.skillTreeChoice.GetSelection()
        self.skillTreeChoice.Delete(sel)
        self.skillTreeChoice.SetSelection(sel - 1)
        newSelection = self.getActiveCharacter()
        if cChar.getCharName(newSelection) in ("All 0", "All 5"):
            self.restrict()

class SkillTreeView (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL)

        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        tree = self.skillTreeListCtrl = wx.gizmos.TreeListCtrl(self, wx.ID_ANY, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        pmainSizer.Add(tree, 1, wx.EXPAND | wx.ALL, 5)


        self.imageList = wx.ImageList(16, 16)
        tree.SetImageList(self.imageList)
        self.skillBookImageId = self.imageList.Add(bitmapLoader.getBitmap("skill_small", "icons"))

        tree.AddColumn("Skill")
        tree.AddColumn("Level")
        tree.SetMainColumn(0)

        self.root = tree.AddRoot("Skills")
        tree.SetItemText(self.root, "Levels", 1)

        tree.SetColumnWidth(0, 500)

        self.populateSkillTree()

        tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)
        tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.spawnMenu)

        self.levelChangeMenu = wx.Menu()
        self.levelIds = {}

        idUnlearned = wx.NewId()
        self.levelIds[idUnlearned] = "Not Learned"
        self.levelChangeMenu.Append(idUnlearned, "Unlearn")

        for level in xrange(6):
            id = wx.NewId()
            self.levelIds[id] = level
            self.levelChangeMenu.Append(id, "Level %d" % level)

        self.levelChangeMenu.Bind(wx.EVT_MENU, self.changeLevel)
        self.SetSizer(pmainSizer)

        self.Layout()

    def populateSkillTree(self):
        cChar = service.Character.getInstance()
        groups = cChar.getSkillGroups()
        imageId = self.skillBookImageId
        root = self.root
        tree = self.skillTreeListCtrl

        for id, name in groups:
            childId = tree.AppendItem(root, name, imageId)
            tree.SetPyData(childId, id)
            tree.AppendItem(childId, "dummy")

        tree.SortChildren(root)

    def expandLookup(self, event):
        root = event.Item
        tree = self.skillTreeListCtrl
        child, cookie = tree.GetFirstChild(root)
        if tree.GetItemText(child) == "dummy":
            tree.Delete(child)

            #Get the real intrestin' stuff
            cChar = service.Character.getInstance()
            char = self.Parent.Parent.getActiveCharacter()
            for id, name in cChar.getSkills(tree.GetPyData(root)):
                iconId = self.skillBookImageId
                childId = tree.AppendItem(root, name, iconId, data=wx.TreeItemData(id))
                level = cChar.getSkillLevel(char, id)
                tree.SetItemText(childId, "Level %d" % level if isinstance(level, int) else level, 1)

            tree.SortChildren(root)

    def spawnMenu(self, event):
        item = event.Item
        self.skillTreeListCtrl.SelectItem(item)
        if self.skillTreeListCtrl.GetChildrenCount(item) > 0:
            return

        cChar = service.Character.getInstance()
        charID = self.Parent.Parent.getActiveCharacter()
        if cChar.getCharName(charID) not in ("All 0", "All 5"):
            self.PopupMenu(self.levelChangeMenu)

    def changeLevel(self, event):
        cChar = service.Character.getInstance()
        charID = self.Parent.Parent.getActiveCharacter()
        selection = self.skillTreeListCtrl.GetSelection()
        skillID = self.skillTreeListCtrl.GetPyData(selection)
        level = self.levelIds[event.Id]

        self.skillTreeListCtrl.SetItemText(selection, "Level %d" % level if isinstance(level, int) else level, 1)
        cChar.changeLevel(charID, skillID, level)


class ImplantsTreeView (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL)

        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        self.ImplantsTreeCtrl = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE)
        pmainSizer.Add(self.ImplantsTreeCtrl, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(pmainSizer)
        self.Layout()

class APIView (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL)

        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        fgSizerInput = wx.FlexGridSizer(3, 2, 0, 0)
        fgSizerInput.AddGrowableCol(1)
        fgSizerInput.SetFlexibleDirection(wx.BOTH)
        fgSizerInput.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticIDText = wx.StaticText(self, wx.ID_ANY, u"User ID:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticIDText.Wrap(-1)
        fgSizerInput.Add(self.m_staticIDText, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.inputID = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerInput.Add(self.inputID, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticKeyText = wx.StaticText(self, wx.ID_ANY, u"API key:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticKeyText.Wrap(-1)
        fgSizerInput.Add(self.m_staticKeyText, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.inputKey = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerInput.Add(self.inputKey, 0, wx.ALL | wx.EXPAND, 5)

        pmainSizer.Add(fgSizerInput, 0, wx.EXPAND, 5)

        self.btnFetchCharList = wx.Button(self, wx.ID_ANY, u"Fetch Character List")
        pmainSizer.Add(self.btnFetchCharList, 0, wx.ALL, 5)

        self.btnFetchCharList.Bind(wx.EVT_BUTTON, self.fetchCharList)

        self.charList = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SINGLE_SEL)
        pmainSizer.Add(self.charList, 0, wx.EXPAND| wx.ALL, 5)

        info = wx.ListItem()
        info.m_text = "Character"
        info.m_mask = wx.LIST_MASK_TEXT

        self.charList.InsertColumnInfo(0, info)

        self.charList.SetMinSize(wx.Size(-1, 100))
        self.charList.Hide()

        self.btnFetchSkills =  wx.Button(self, wx.ID_ANY, u"Fetch Skills")
        pmainSizer.Add(self.btnFetchSkills, 0, wx.ALL, 5)
        self.btnFetchSkills.Hide()
        self.btnFetchSkills.Bind(wx.EVT_BUTTON, self.fetchSkills)

        self.SetSizer(pmainSizer)
        self.Layout()

    def fetchCharList(self, event):
        cChar = service.Character.getInstance()
        list = cChar.charList(self.Parent.Parent.getActiveCharacter(), self.inputID.GetLineText(0), self.inputKey.GetLineText(0))
        self.charList.DeleteAllItems()

        for charName in list:
            self.charList.InsertStringItem(sys.maxint, charName)

        self.charList.SetColumnWidth(0, 614)
        self.charList.Show()
        self.btnFetchCharList.Hide()
        self.btnFetchSkills.Show()
        self.Layout()

    def fetchSkills(self, event):
        item = self.charList.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        charName = self.charList.GetItemText(item)
        if charName:
            cChar = service.Character.getInstance()
            cChar.apiFetch(self.Parent.Parent.getActiveCharacter(), charName)
