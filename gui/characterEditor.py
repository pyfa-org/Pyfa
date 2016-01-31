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
from gui.bitmapLoader import BitmapLoader
import service
import gui.display as d
from gui.contextMenu import ContextMenu
from wx.lib.buttons import GenBitmapButton
import gui.globalEvents as GE

class CharacterEditor(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"pyfa: Character Editor", pos=wx.DefaultPosition,
                            size=wx.Size(640, 600), style=wx.DEFAULT_DIALOG_STYLE)

        i = wx.IconFromBitmap(BitmapLoader.getBitmap("character_small", "gui"))
        self.SetIcon(i)

        self.mainFrame = parent

        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.navSizer = wx.BoxSizer(wx.HORIZONTAL)

        sChar = service.Character.getInstance()

        self.btnSave = wx.Button(self, wx.ID_SAVE)
        self.btnSave.Hide()
        self.btnSave.Bind(wx.EVT_BUTTON, self.processRename)

        self.characterRename = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.characterRename.Hide()
        self.characterRename.Bind(wx.EVT_TEXT_ENTER, self.processRename)

        self.charChoice = wx.Choice(self, wx.ID_ANY, style=0)
        self.navSizer.Add(self.charChoice, 1, wx.ALL | wx.EXPAND, 5)

        charList = sChar.getCharacterList()

        for id, name, active in charList:
            i = self.charChoice.Append(name, id)
            if active:
                self.charChoice.SetSelection(i)

        self.navSizer.Add(self.btnSave, 0, wx.ALL , 5)


        buttons = (("new", wx.ART_NEW),
                   ("rename", BitmapLoader.getBitmap("rename", "gui")),
                   ("copy", wx.ART_COPY),
                   ("delete", wx.ART_DELETE))

        size = None
        for name, art in buttons:
            bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON) if name != "rename" else art
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
        #self.iview = ImplantsTreeView(self.viewsNBContainer)
        #=======================================================================
        # RC2
        #self.iview.Show(False)
        #=======================================================================
        self.aview = APIView(self.viewsNBContainer)

        self.viewsNBContainer.AddPage(self.sview, "Skills")

        #=======================================================================
        # Disabled for RC2
        # self.viewsNBContainer.AddPage(self.iview, "Implants")
        #=======================================================================
        self.viewsNBContainer.AddPage(self.aview, "API")

        mainSizer.Add(self.viewsNBContainer, 1, wx.EXPAND | wx.ALL, 5)

        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.btnSaveChar = wx.Button(self, wx.ID_ANY, "Save")
        self.btnSaveAs = wx.Button(self, wx.ID_ANY, "Save As...")
        self.btnRevert = wx.Button(self, wx.ID_ANY, "Revert")
        self.btnOK = wx.Button(self, wx.ID_OK)

        bSizerButtons.Add(self.btnSaveChar, 0, wx.ALL, 5)
        bSizerButtons.Add(self.btnSaveAs, 0, wx.ALL, 5)
        bSizerButtons.Add(self.btnRevert, 0, wx.ALL, 5)
        bSizerButtons.AddStretchSpacer()
        bSizerButtons.Add(self.btnOK, 0, wx.ALL, 5)


        self.btnSaveChar.Bind(wx.EVT_BUTTON, self.saveChar)
        self.btnSaveAs.Bind(wx.EVT_BUTTON, self.saveCharAs)
        self.btnRevert.Bind(wx.EVT_BUTTON, self.revertChar)
        self.btnOK.Bind(wx.EVT_BUTTON, self.editingFinished)

        mainSizer.Add(bSizerButtons, 0, wx.EXPAND, 5)

        self.btnRestrict()

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        charID = self.getActiveCharacter()
        if sChar.getCharName(charID) in ("All 0", "All 5"):
            self.restrict()

        self.registerEvents()

    def btnRestrict(self):
        sChar = service.Character.getInstance()
        charID = self.getActiveCharacter()
        char = sChar.getCharacter(charID)

        # enable/disable character saving stuff
        self.btnSaveChar.Enable(not char.ro and char.isDirty)
        self.btnSaveAs.Enable(char.isDirty)
        self.btnRevert.Enable(char.isDirty)

    def refreshCharacterList(self, event=None):
        sChar = service.Character.getInstance()
        charList = sChar.getCharacterList()
        active = self.getActiveCharacter()
        self.charChoice.Clear()

        for id, name, _ in charList:
            i = self.charChoice.Append(name, id)
            if active == id:
                self.charChoice.SetSelection(i)

        self.btnRestrict()

    def editingFinished(self, event):
        wx.PostEvent(self.mainFrame, GE.CharListUpdated())
        self.Close()

    def registerEvents(self):
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(GE.CHAR_LIST_UPDATED, self.refreshCharacterList)
        self.charChoice.Bind(wx.EVT_CHOICE, self.charChanged)

    def saveChar(self, event):
        sChr = service.Character.getInstance()
        charID = self.getActiveCharacter()
        sChr.saveCharacter(charID)
        self.sview.populateSkillTree()
        wx.PostEvent(self, GE.CharListUpdated())

    def saveCharAs(self, event):
        charID = self.getActiveCharacter()
        dlg = SaveCharacterAs(self, charID)
        dlg.ShowModal()
        self.sview.populateSkillTree()

    def revertChar(self, event):
        sChr = service.Character.getInstance()
        charID = self.getActiveCharacter()
        sChr.revertCharacter(charID)
        self.sview.populateSkillTree()
        wx.PostEvent(self, GE.CharListUpdated())

    def restrict(self):
        self.btnRename.Enable(False)
        self.btnDelete.Enable(False)
        self.aview.stDisabledTip.Show()
        self.aview.inputID.Enable(False)
        self.aview.inputKey.Enable(False)
        self.aview.charChoice.Enable(False)
        self.aview.btnFetchCharList.Enable(False)
        self.aview.btnFetchSkills.Enable(False)
        self.aview.stStatus.SetLabel("")
        self.aview.Layout()

    def unrestrict(self):
        self.btnRename.Enable(True)
        self.btnDelete.Enable(True)
        self.aview.stDisabledTip.Hide()
        self.aview.inputID.Enable(True)
        self.aview.inputKey.Enable(True)
        self.aview.btnFetchCharList.Enable(True)
        self.aview.btnFetchSkills.Enable(True)
        self.aview.stStatus.SetLabel("")
        self.aview.Layout()

    def charChanged(self, event):
        self.sview.populateSkillTree()
        sChar = service.Character.getInstance()
        charID = self.getActiveCharacter()
        if sChar.getCharName(charID) in ("All 0", "All 5"):
            self.restrict()
        else:
            self.unrestrict()

        wx.PostEvent(self, GE.CharChanged())
        if event is not None:
            event.Skip()

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not None else None

    def new(self, event):
        sChar = service.Character.getInstance()
        charID = sChar.new()
        id = self.charChoice.Append(sChar.getCharName(charID), charID)
        self.charChoice.SetSelection(id)
        self.unrestrict()
        self.btnSave.SetLabel("Create")
        self.rename(None)
        self.charChanged(None)

    def rename(self, event):
        if event is not None:
            self.btnSave.SetLabel("Rename")
        self.charChoice.Hide()
        self.characterRename.Show()
        self.navSizer.Replace(self.charChoice, self.characterRename)
        self.characterRename.SetFocus()
        for btn in (self.btnNew, self.btnCopy, self.btnRename, self.btnDelete):
            btn.Hide()

        self.btnSave.Show()
        self.navSizer.Layout()

        sChar = service.Character.getInstance()
        currName = sChar.getCharName(self.getActiveCharacter())
        self.characterRename.SetValue(currName)
        self.characterRename.SetSelection(0, len(currName))

    def processRename(self, event):
        sChar = service.Character.getInstance()
        newName = self.characterRename.GetLineText(0)

        if newName == "All 0" or newName == "All 5":
            newName = newName + " bases are belong to us"

        charID = self.getActiveCharacter()
        sChar.rename(charID, newName)

        self.charChoice.Show()
        self.characterRename.Hide()
        self.navSizer.Replace(self.characterRename, self.charChoice)
        for btn in (self.btnNew, self.btnCopy, self.btnRename, self.btnDelete):
            btn.Show()

        self.btnSave.Hide()
        self.navSizer.Layout()
        self.refreshCharacterList()

    def copy(self, event):
        sChar = service.Character.getInstance()
        charID = sChar.copy(self.getActiveCharacter())
        id = self.charChoice.Append(sChar.getCharName(charID), charID)
        self.charChoice.SetSelection(id)
        self.unrestrict()
        self.btnSave.SetLabel("Copy")
        self.rename(None)
        wx.PostEvent(self, GE.CharChanged())

    def delete(self, event):
        dlg = wx.MessageDialog(self,
                 "Do you really want to delete this character?",
                 "Confirm Delete", wx.YES | wx.NO | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            sChar = service.Character.getInstance()
            sChar.delete(self.getActiveCharacter())
            sel = self.charChoice.GetSelection()
            self.charChoice.Delete(sel)
            self.charChoice.SetSelection(sel - 1)
            newSelection = self.getActiveCharacter()
            if sChar.getCharName(newSelection) in ("All 0", "All 5"):
                self.restrict()

            wx.PostEvent(self, GE.CharChanged())

    def OnClose(self, event):
        wx.PostEvent(self.mainFrame, GE.CharListUpdated())
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        if fitID is not None:
            sFit.clearFit(fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

        self.Destroy()

class SkillTreeView (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        tree = self.skillTreeListCtrl = wx.gizmos.TreeListCtrl(self, wx.ID_ANY, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        pmainSizer.Add(tree, 1, wx.EXPAND | wx.ALL, 5)


        self.imageList = wx.ImageList(16, 16)
        tree.SetImageList(self.imageList)
        self.skillBookImageId = self.imageList.Add(BitmapLoader.getBitmap("skill_small", "gui"))

        tree.AddColumn("Skill")
        tree.AddColumn("Level")
        tree.SetMainColumn(0)

        self.root = tree.AddRoot("Skills")
        tree.SetItemText(self.root, "Levels", 1)

        tree.SetColumnWidth(0, 500)

        self.populateSkillTree()

        tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)
        tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.scheduleMenu)

        srcContext = "skillItem"
        itemContext = "Skill"
        context = (srcContext, itemContext)
        self.statsMenu = ContextMenu.getMenu(None, context)
        self.levelChangeMenu = ContextMenu.getMenu(None, context) or wx.Menu()
        self.levelChangeMenu.AppendSeparator()
        self.levelIds = {}

        idUnlearned = wx.NewId()
        self.levelIds[idUnlearned] = "Not learned"
        self.levelChangeMenu.Append(idUnlearned, "Unlearn")

        for level in xrange(6):
            id = wx.NewId()
            self.levelIds[id] = level
            self.levelChangeMenu.Append(id, "Level %d" % level)

        self.levelChangeMenu.AppendSeparator()
        self.revertID = wx.NewId()
        self.levelChangeMenu.Append(self.revertID, "Revert")


        self.saveID = wx.NewId()
        self.levelChangeMenu.Append(self.saveID, "Save")

        self.levelChangeMenu.Bind(wx.EVT_MENU, self.changeLevel)
        self.SetSizer(pmainSizer)

        self.Layout()

    def populateSkillTree(self):
        sChar = service.Character.getInstance()
        charID = self.Parent.Parent.getActiveCharacter()
        dirtySkills = sChar.getDirtySkills(charID)
        dirtyGroups = set([skill.item.group.ID for skill in dirtySkills])

        groups = sChar.getSkillGroups()
        imageId = self.skillBookImageId
        root = self.root
        tree = self.skillTreeListCtrl
        tree.DeleteChildren(root)

        for id, name in groups:
            childId = tree.AppendItem(root, name, imageId)
            tree.SetPyData(childId, id)
            tree.AppendItem(childId, "dummy")
            if id in dirtyGroups:
                tree.SetItemTextColour(childId, wx.BLUE)

        tree.SortChildren(root)

    def expandLookup(self, event):
        root = event.Item
        tree = self.skillTreeListCtrl
        child, cookie = tree.GetFirstChild(root)
        if tree.GetItemText(child) == "dummy":
            tree.Delete(child)

            #Get the real intrestin' stuff
            sChar = service.Character.getInstance()
            char = self.Parent.Parent.getActiveCharacter()
            for id, name in sChar.getSkills(tree.GetPyData(root)):
                iconId = self.skillBookImageId
                childId = tree.AppendItem(root, name, iconId, data=wx.TreeItemData(id))
                level, dirty = sChar.getSkillLevel(char, id)
                tree.SetItemText(childId, "Level %d" % level if isinstance(level, int) else level, 1)
                if dirty:
                    tree.SetItemTextColour(childId, wx.BLUE)

            tree.SortChildren(root)

    def scheduleMenu(self, event):
        event.Skip()
        wx.CallAfter(self.spawnMenu, event.Item)

    def spawnMenu(self, item):
        self.skillTreeListCtrl.SelectItem(item)
        if self.skillTreeListCtrl.GetChildrenCount(item) > 0:
            return

        sChar = service.Character.getInstance()
        charID = self.Parent.Parent.getActiveCharacter()
        sMkt = service.Market.getInstance()
        if sChar.getCharName(charID) not in ("All 0", "All 5"):
            self.levelChangeMenu.selection = sMkt.getItem(self.skillTreeListCtrl.GetPyData(item))
            self.PopupMenu(self.levelChangeMenu)
        else:
            self.statsMenu.selection = sMkt.getItem(self.skillTreeListCtrl.GetPyData(item))
            self.PopupMenu(self.statsMenu)

    def changeLevel(self, event):
        level = self.levelIds.get(event.Id)

        sChar = service.Character.getInstance()
        charID = self.Parent.Parent.getActiveCharacter()
        selection = self.skillTreeListCtrl.GetSelection()
        skillID = self.skillTreeListCtrl.GetPyData(selection)

        if level is not None:
            self.skillTreeListCtrl.SetItemText(selection, "Level %d" % level if isinstance(level, int) else level, 1)
            sChar.changeLevel(charID, skillID, level, persist=True)
        elif event.Id == self.revertID:
            sChar.revertLevel(charID, skillID)
        elif event.Id == self.saveID:
            sChar.saveSkill(charID, skillID)

        self.skillTreeListCtrl.SetItemTextColour(selection, None)

        dirtySkills = sChar.getDirtySkills(charID)
        dirtyGroups = set([skill.item.group.ID for skill in dirtySkills])

        parentID = self.skillTreeListCtrl.GetItemParent(selection)
        groupID = self.skillTreeListCtrl.GetPyData(parentID)

        if groupID not in dirtyGroups:
            self.skillTreeListCtrl.SetItemTextColour(parentID, None)

        wx.PostEvent(self.Parent.Parent, GE.CharListUpdated())
        event.Skip()

class ImplantsTreeView (wx.Panel):
    def addMarketViewImage(self, iconFile):
        if iconFile is None:
            return -1
        bitmap = BitmapLoader.getBitmap(iconFile, "icons")
        if bitmap is None:
            return -1
        else:
            return self.availableImplantsImageList.Add(bitmap)

    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL)

        pmainSizer = wx.BoxSizer(wx.HORIZONTAL)

        availableSizer = wx.BoxSizer(wx.VERTICAL)
        pmainSizer.Add(availableSizer, 1, wx.ALL | wx.EXPAND, 5)

        self.availableImplantsSearch = wx.SearchCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.availableImplantsSearch.ShowCancelButton(True)
        availableSizer.Add(self.availableImplantsSearch, 0, wx.BOTTOM | wx.EXPAND, 2)

        self.availableImplantsTree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        root = self.availableRoot = self.availableImplantsTree.AddRoot("Available")
        self.availableImplantsImageList = wx.ImageList(16, 16)
        self.availableImplantsTree.SetImageList(self.availableImplantsImageList)

        availableSizer.Add(self.availableImplantsTree, 1, wx.EXPAND)

        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        pmainSizer.Add(buttonSizer, 0, wx.TOP, 5)

        self.btnAdd = GenBitmapButton(self, wx.ID_ADD, BitmapLoader.getBitmap("fit_add_small", "gui"), style = wx.BORDER_NONE)
        buttonSizer.Add(self.btnAdd, 0)
        self.btnRemove = GenBitmapButton(self, wx.ID_REMOVE, BitmapLoader.getBitmap("fit_delete_small", "gui"), style = wx.BORDER_NONE)
        buttonSizer.Add(self.btnRemove, 0)

        self.pluggedImplantsTree = AvailableImplantsView(self, style=wx.LC_SINGLE_SEL)

        pmainSizer.Add(self.pluggedImplantsTree, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(pmainSizer)

        # Populate the market tree
        sMkt = service.Market.getInstance()
        for mktGrp in sMkt.getImplantTree():
            iconId = self.addMarketViewImage(sMkt.getIconByMarketGroup(mktGrp))
            childId = self.availableImplantsTree.AppendItem(root, mktGrp.name, iconId, data=wx.TreeItemData(mktGrp.ID))
            if sMkt.marketGroupHasTypesCheck(mktGrp) is False:
                self.availableImplantsTree.AppendItem(childId, "dummy")

        self.availableImplantsTree.SortChildren(self.availableRoot)

        #Bind the event to replace dummies by real data
        self.availableImplantsTree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)

        #Bind add & remove buttons
        self.btnAdd.Bind(wx.EVT_BUTTON, self.addImplant)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.removeImplant)

        #Bind the change of a character*
        self.Parent.Parent.Bind(GE.CHAR_CHANGED, self.charChanged)
        self.Enable(False)
        self.Layout()

    def update(self, implants):
        self.implants = implants[:]
        self.implants.sort(key=lambda i: int(i.getModifiedItemAttr("implantness")))
        self.pluggedImplantsTree.update(self.implants)

    def charChanged(self, event):
        sChar = service.Character.getInstance()
        charID = self.Parent.Parent.getActiveCharacter()
        name = sChar.getCharName(charID)
        if name == "All 0" or name == "All 5":
            self.Enable(False)
        else:
            self.Enable(True)

        self.update(sChar.getImplants(charID))
        event.Skip()

    def expandLookup(self, event):
        tree = self.availableImplantsTree
        root = event.Item
        child, cookie = tree.GetFirstChild(root)
        text = tree.GetItemText(child)
        if text == "dummy" or text == "itemdummy":
            sMkt = service.Market.getInstance()
            #A DUMMY! Keeeel!!! EBUL DUMMY MUST DIAF!
            tree.Delete(child)

        if text == "dummy":
            #Add 'real stoof!' instead
            for id, name, iconFile, more in sMkt.getChildren(tree.GetPyData(root)):
                iconId = self.addMarketViewImage(iconFile)
                childId = tree.AppendItem(root, name, iconId, data=wx.TreeItemData(id))
                if more:
                    tree.AppendItem(childId, "dummy")
                else:
                    tree.AppendItem(childId, "itemdummy")

        if text == "itemdummy":
            sMkt = service.Market.getInstance()
            data, usedMetas = sMkt.getVariations(tree.GetPyData(root))
            for item in data:
                id = item.ID
                name = item.name
                iconFile = item.icon.iconFile
                iconId = self.addMarketViewImage(iconFile)
                tree.AppendItem(root, name, iconId, data=wx.TreeItemData(id))

        tree.SortChildren(root)

    def addImplant(self, event):
        root = self.availableImplantsTree.GetSelection()

        if not root.IsOk():
            return

        nchilds = self.availableImplantsTree.GetChildrenCount(root)
        sChar = service.Character.getInstance()
        charID = self.Parent.Parent.getActiveCharacter()
        if nchilds == 0:
            itemID = self.availableImplantsTree.GetPyData(root)
            sChar.addImplant(charID, itemID)
            self.update(sChar.getImplants(charID))

    def removeImplant(self, event):
        pos = self.pluggedImplantsTree.GetFirstSelected()
        if pos != -1:
            sChar = service.Character.getInstance()
            charID = self.Parent.Parent.getActiveCharacter()
            sChar.removeImplant(charID, self.implants[pos].slot)
            self.update(sChar.getImplants(charID))

class AvailableImplantsView(d.Display):
    DEFAULT_COLS = ["Base Name",
                    "attr:implantness"]

    def __init__(self, parent, style):
        d.Display.__init__(self, parent, style=style)

class APIView (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL)
        self.Parent.Parent.Bind(GE.CHAR_CHANGED, self.charChanged)
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

        self.apiUrlCreatePredefined = u"https://community.eveonline.com/support/api-key/CreatePredefined?accessMask=8"
        self.apiUrlKeyList = u"https://community.eveonline.com/support/api-key/"

        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        hintSizer = wx.BoxSizer( wx.HORIZONTAL )
        hintSizer.AddStretchSpacer()
        self.stDisabledTip = wx.StaticText( self, wx.ID_ANY, u"You cannot add API Details for All 0 and All 5 characters.\n"
                                                             u"Please select another character or make a new one.", style=wx.ALIGN_CENTER )
        self.stDisabledTip.Wrap( -1 )
        hintSizer.Add( self.stDisabledTip, 0, wx.TOP | wx.BOTTOM, 10 )
        self.stDisabledTip.Hide()
        hintSizer.AddStretchSpacer()
        pmainSizer.Add(hintSizer, 0, wx.EXPAND, 5)


        fgSizerInput = wx.FlexGridSizer(3, 2, 0, 0)
        fgSizerInput.AddGrowableCol(1)
        fgSizerInput.SetFlexibleDirection(wx.BOTH)
        fgSizerInput.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticIDText = wx.StaticText(self, wx.ID_ANY, u"keyID:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticIDText.Wrap(-1)
        fgSizerInput.Add(self.m_staticIDText, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.inputID = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerInput.Add(self.inputID, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticKeyText = wx.StaticText(self, wx.ID_ANY, u"vCode:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticKeyText.Wrap(-1)
        fgSizerInput.Add(self.m_staticKeyText, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.inputKey = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerInput.Add(self.inputKey, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticCharText = wx.StaticText(self, wx.ID_ANY, u"Character:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticCharText.Wrap(-1)
        fgSizerInput.Add(self.m_staticCharText, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.charChoice = wx.Choice(self, wx.ID_ANY, style=0)
        self.charChoice.Append("No Selection", 0)
        fgSizerInput.Add(self.charChoice, 1, wx.ALL | wx.EXPAND, 5)

        self.charChoice.Enable(False)

        pmainSizer.Add(fgSizerInput, 0, wx.EXPAND, 5)

        btnSizer = wx.BoxSizer( wx.HORIZONTAL )
        btnSizer.AddStretchSpacer()

        self.btnFetchCharList = wx.Button(self, wx.ID_ANY, u"Get Characters")
        btnSizer.Add(self.btnFetchCharList, 0, wx.ALL, 2)
        self.btnFetchCharList.Bind(wx.EVT_BUTTON, self.fetchCharList)

        self.btnFetchSkills =  wx.Button(self, wx.ID_ANY, u"Fetch Skills")
        btnSizer.Add(self.btnFetchSkills,  0, wx.ALL, 2)
        self.btnFetchSkills.Bind(wx.EVT_BUTTON, self.fetchSkills)
        self.btnFetchSkills.Enable(False)

        btnSizer.AddStretchSpacer()
        pmainSizer.Add(btnSizer, 0, wx.EXPAND, 5)

        self.stStatus = wx.StaticText(self,  wx.ID_ANY, wx.EmptyString)
        pmainSizer.Add(self.stStatus, 0, wx.ALL, 5)

        pmainSizer.AddStretchSpacer()
        self.stAPITip = wx.StaticText( self, wx.ID_ANY, u"You can create a pre-defined key here (only CharacterSheet is required):", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stAPITip.Wrap( -1 )

        pmainSizer.Add( self.stAPITip, 0, wx.ALL, 2 )

        self.hlEveAPI = wx.HyperlinkCtrl( self, wx.ID_ANY, self.apiUrlCreatePredefined, self.apiUrlCreatePredefined, wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
        pmainSizer.Add( self.hlEveAPI, 0, wx.ALL, 2 )

        self.stAPITip2 = wx.StaticText( self, wx.ID_ANY, u"Or, you can choose an existing key from:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stAPITip2.Wrap( -1 )
        pmainSizer.Add( self.stAPITip2, 0, wx.ALL, 2 )

        self.hlEveAPI2 = wx.HyperlinkCtrl( self, wx.ID_ANY, self.apiUrlKeyList, self.apiUrlKeyList, wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
        pmainSizer.Add( self.hlEveAPI2, 0, wx.ALL, 2 )

        self.SetSizer(pmainSizer)
        self.Layout()
        self.charChanged(None)

    def charChanged(self, event):
        sChar = service.Character.getInstance()
        ID, key, char, chars = sChar.getApiDetails(self.Parent.Parent.getActiveCharacter())
        self.inputID.SetValue(str(ID))
        self.inputKey.SetValue(key)

        self.charChoice.Clear()

        if chars:
            for charName in chars:
                i = self.charChoice.Append(charName)
            self.charChoice.SetStringSelection(char)
            self.charChoice.Enable(True)
            self.btnFetchSkills.Enable(True)
        else:
            self.charChoice.Append("No characters...", 0)
            self.charChoice.SetSelection(0)
            self.charChoice.Enable(False)
            self.btnFetchSkills.Enable(False)


        if event is not None:
            event.Skip()

    def fetchCharList(self, event):
        self.stStatus.SetLabel("")
        if self.inputID.GetLineText(0) == "" or self.inputKey.GetLineText(0) == "":
            self.stStatus.SetLabel("Invalid keyID or vCode!")
            return

        sChar = service.Character.getInstance()
        try:
            list = sChar.apiCharList(self.Parent.Parent.getActiveCharacter(), self.inputID.GetLineText(0), self.inputKey.GetLineText(0))
        except service.network.AuthenticationError, e:
            self.stStatus.SetLabel("Authentication failure. Please check keyID and vCode combination.")
        except service.network.TimeoutError, e:
            self.stStatus.SetLabel("Request timed out. Please check network connectivity and/or proxy settings.")
        except Exception, e:
            self.stStatus.SetLabel("Error:\n%s"%e.message)
        else:
            self.charChoice.Clear()
            for charName in list:
                i = self.charChoice.Append(charName)

            self.btnFetchSkills.Enable(True)
            self.charChoice.Enable(True)

            self.Layout()

            self.charChoice.SetSelection(0)

    def fetchSkills(self, event):
        charName = self.charChoice.GetString(self.charChoice.GetSelection())
        if charName:
            try:
                sChar = service.Character.getInstance()
                sChar.apiFetch(self.Parent.Parent.getActiveCharacter(), charName)
                self.stStatus.SetLabel("Successfully fetched %s\'s skills from EVE API." % charName)
            except Exception, e:
                self.stStatus.SetLabel("Unable to retrieve %s\'s skills. Error message:\n%s" % (charName, e))

class SaveCharacterAs(wx.Dialog):

    def __init__(self, parent, charID):
        wx.Dialog.__init__(self, parent, title="Save Character As...", size=wx.Size(300, 60))
        self.charID = charID
        self.parent = parent
        sChar = service.Character.getInstance()
        name = sChar.getCharName(charID)
        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.input = wx.TextCtrl(self, wx.ID_ANY, name, style=wx.TE_PROCESS_ENTER)

        bSizer1.Add(self.input, 1, wx.ALL, 5)
        self.input.Bind(wx.EVT_TEXT_ENTER, self.change)
        self.button = wx.Button(self, wx.ID_OK, u"Save")
        bSizer1.Add(self.button, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.button.Bind(wx.EVT_BUTTON, self.change)

    def change(self, event):
        sChar = service.Character.getInstance()
        sChar.saveCharacterAs(self.charID, self.input.GetLineText(0))
        wx.PostEvent(self.parent, GE.CharListUpdated())

        event.Skip()
        self.Close()

