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
import wx.dataview
import wx.lib.agw.hyperlink

# noinspection PyPackageRequirements
import wx.lib.newevent
# noinspection PyPackageRequirements
from wx.dataview import TreeListCtrl
from gui.bitmap_loader import BitmapLoader
from gui.contextMenu import ContextMenu
import gui.globalEvents as GE
from gui.builtinViews.implantEditor import BaseImplantEditorView
from gui.builtinViews.entityEditor import EntityEditor, BaseValidator, TextEntryValidatedDialog
from service.fit import Fit
from service.character import Character
from service.esi import Esi
from service.network import AuthenticationError, TimeoutError
from service.market import Market
from logbook import Logger

from wx.lib.agw.floatspin import FloatSpin


from gui.utils.clipboard import toClipboard, fromClipboard

import roman
import re
import webbrowser

pyfalog = Logger(__name__)


def arabicOrRomanToInt(s):
    m = re.match(r'\d+$', s)
    if m:
        i = int(s)
    else:
        i = roman.fromRoman(s)
    return i


class CharacterTextValidor(BaseValidator):
    def __init__(self):
        BaseValidator.__init__(self)

    def Clone(self):
        return CharacterTextValidor()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()
        sChar = Character.getInstance()

        try:
            if len(text) == 0:
                raise ValueError("You must supply a name for the Character!")
            elif text in [x.name for x in sChar.getCharacterList()]:
                raise ValueError("Character name already in use, please choose another.")

            return True
        except ValueError as e:
            pyfalog.error(e)
            wx.MessageBox("{}".format(e), "Error")
            textCtrl.SetFocus()
            return False


class PlaceholderTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        self.default_text = kwargs.pop("placeholder", "")
        kwargs["value"] = self.default_text
        wx.TextCtrl.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def OnFocus(self, evt):
        if self.GetValue() == self.default_text:
            self.SetValue("")
        evt.Skip()

    def OnKillFocus(self, evt):
        if self.GetValue().strip() == "":
            self.SetValue(self.default_text)
        evt.Skip()

    def Reset(self):
        self.SetValue(self.default_text)


class CharacterEntityEditor(EntityEditor):
    def __init__(self, parent):
        EntityEditor.__init__(self, parent, "Character")
        self.SetEditorValidator(CharacterTextValidor)

    def getEntitiesFromContext(self):
        sChar = Character.getInstance()
        charList = sorted(sChar.getCharacterList(), key=lambda c: (not c.ro, c.name))

        # Do some processing to ensure that we have All 0 and All 5 at the top
        all5 = sChar.all5()
        all0 = sChar.all0()

        charList.remove(all5)
        charList.remove(all0)

        charList.insert(0, all5)
        charList.insert(0, all0)

        return charList

    def DoNew(self, name):
        sChar = Character.getInstance()
        return sChar.new(name)

    def DoRename(self, entity, name):
        sChar = Character.getInstance()
        sChar.rename(entity, name)

    def DoCopy(self, entity, name):
        sChar = Character.getInstance()
        copy = sChar.copy(entity)
        sChar.rename(copy, name)
        return copy

    def DoDelete(self, entity):
        sChar = Character.getInstance()
        sChar.delete(entity)


class CharacterEditor(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="pyfa: Character Editor", pos=wx.DefaultPosition,
                          size=wx.Size(640, 600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        i = wx.Icon(BitmapLoader.getBitmap("character_small", "gui"))
        self.SetIcon(i)

        self.mainFrame = parent
        # self.disableWin = wx.WindowDisabler(self)
        sFit = Fit.getInstance()

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.entityEditor = CharacterEntityEditor(self)
        mainSizer.Add(self.entityEditor, 0, wx.ALL | wx.EXPAND, 2)
        # Default drop down to current fit's character
        self.entityEditor.setActiveEntity(sFit.character)

        self.viewsNBContainer = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        self.sview = SkillTreeView(self.viewsNBContainer)
        self.iview = ImplantEditorView(self.viewsNBContainer, self)
        self.aview = APIView(self.viewsNBContainer)

        self.viewsNBContainer.AddPage(self.sview, "Skills")
        self.viewsNBContainer.AddPage(self.iview, "Implants")
        self.viewsNBContainer.AddPage(self.aview, "EVE SSO")

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

        self.Bind(wx.EVT_CLOSE, self.closeEvent)
        self.Bind(GE.CHAR_LIST_UPDATED, self.refreshCharacterList)
        self.entityEditor.Bind(wx.EVT_CHOICE, self.charChanged)

        self.charChanged(None)

    def btnRestrict(self):
        char = self.entityEditor.getActiveEntity()

        # enable/disable character saving stuff
        self.btnSaveChar.Enable(not char.ro and char.isDirty)
        self.btnSaveAs.Enable(char.isDirty)
        self.btnRevert.Enable(char.isDirty)
        self.sview.importBtn.Enable(not char.ro)

    def refreshCharacterList(self, event=None):
        """This is only called when we save a modified character"""
        active = self.entityEditor.getActiveEntity()
        self.entityEditor.refreshEntityList(active)
        self.btnRestrict()

        if event:
            event.Skip()

    def editingFinished(self, event):
        # del self.disableWin
        wx.PostEvent(self.mainFrame, GE.CharListUpdated())
        self.Destroy()

    def saveChar(self, event):
        sChr = Character.getInstance()
        char = self.entityEditor.getActiveEntity()
        sChr.saveCharacter(char.ID)
        wx.PostEvent(self, GE.CharListUpdated())

    def saveCharAs(self, event):
        char = self.entityEditor.getActiveEntity()
        self.SaveCharacterAs(self, char.ID)
        wx.PostEvent(self, GE.CharListUpdated())

    def revertChar(self, event):
        sChr = Character.getInstance()
        char = self.entityEditor.getActiveEntity()
        sChr.revertCharacter(char.ID)
        wx.PostEvent(self, GE.CharListUpdated())

    def closeEvent(self, event):
        # del self.disableWin
        wx.PostEvent(self.mainFrame, GE.CharListUpdated())
        self.Destroy()

    def restrict(self):
        self.entityEditor.btnRename.Enable(False)
        self.entityEditor.btnDelete.Enable(False)

    def unrestrict(self):
        self.entityEditor.btnRename.Enable()
        self.entityEditor.btnDelete.Enable()

    def charChanged(self, event):
        char = self.entityEditor.getActiveEntity()
        if char.name in ("All 0", "All 5"):
            self.restrict()
        else:
            self.unrestrict()

        self.btnRestrict()

        if event is not None:
            event.Skip()

    def Destroy(self):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        if fitID is not None:
            sFit.clearFit(fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

        wx.Frame.Destroy(self)

    @staticmethod
    def SaveCharacterAs(parent, charID):
        sChar = Character.getInstance()
        name = sChar.getCharName(charID)

        dlg = TextEntryValidatedDialog(parent, CharacterTextValidor,
                                       "Enter a name for your new Character:",
                                       "Save Character As...")
        dlg.SetValue("{} Copy".format(name))
        dlg.txtctrl.SetInsertionPointEnd()
        dlg.CenterOnParent()

        if dlg.ShowModal() == wx.ID_OK:
            sChar = Character.getInstance()
            return sChar.saveCharacterAs(charID, dlg.txtctrl.GetValue().strip())


class SkillTreeView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        self.charEditor = self.Parent.Parent  # first parent is Notebook, second is Character Editor
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.clonesChoice = wx.Choice(self, wx.ID_ANY, style=0)
        i = self.clonesChoice.Append("Omega Clone", None)
        self.clonesChoice.SetSelection(i)
        hSizer.Add(self.clonesChoice, 5, wx.ALL | wx.EXPAND, 5)

        self.searchInput = PlaceholderTextCtrl(self, wx.ID_ANY, placeholder="Search...")
        hSizer.Add(self.searchInput, 1, wx.ALL | wx.EXPAND, 5)
        self.searchInput.Bind(wx.EVT_TEXT, self.delaySearch)

        sChar = Character.getInstance()
        self.alphaClones = sChar.getAlphaCloneList()
        char = self.charEditor.entityEditor.getActiveEntity()

        for clone in self.alphaClones:
            i = self.clonesChoice.Append(clone.alphaCloneName, clone.ID)
            if clone.ID == char.alphaCloneID:
                self.clonesChoice.SetSelection(i)

        self.clonesChoice.Bind(wx.EVT_CHOICE, self.cloneChanged)

        self.clonesChoice.SetToolTip(
            wx.ToolTip("Setting an Alpha clone does not replace the character's skills, but rather caps them to Alpha levels."))

        pmainSizer.Add(hSizer, 0, wx.EXPAND | wx.ALL, 5)

        # Set up timer for skill search
        self.searchTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.populateSkillTreeSkillSearch, self.searchTimer)

        tree = self.skillTreeListCtrl = TreeListCtrl(self, wx.ID_ANY, style=wx.dataview.TL_DEFAULT_STYLE)
        pmainSizer.Add(tree, 1, wx.EXPAND | wx.ALL, 5)

        self.imageList = wx.ImageList(16, 16)
        tree.SetImageList(self.imageList)
        self.skillBookImageId = self.imageList.Add(wx.Icon(BitmapLoader.getBitmap("skill_small", "gui")))
        self.skillBookDirtyImageId = self.imageList.Add(wx.Icon(BitmapLoader.getBitmap("skill_small_red", "gui")))

        tree.AppendColumn("Skill")
        tree.AppendColumn("Level")
        # tree.SetMainColumn(0)

        self.root = tree.GetRootItem()
        # self.root = tree.AppendItem(root, "Skills")
        #
        # tree.SetItemText(self.root, 1, "Levels")

        # tree.SetColumnWidth(0, 300)

        self.btnSecStatus = wx.Button(self, wx.ID_ANY, "Sec Status: {0:.2f}".format(char.secStatus or 0.0))
        self.btnSecStatus.Bind(wx.EVT_BUTTON, self.onSecStatus)

        self.populateSkillTree()

        tree.Bind(wx.dataview.EVT_TREELIST_ITEM_EXPANDING, self.expandLookup)
        tree.Bind(wx.dataview.EVT_TREELIST_ITEM_CONTEXT_MENU, self.scheduleMenu)

        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        bSizerButtons.Add(self.btnSecStatus, 0, wx.ALL, 5)

        bSizerButtons.AddStretchSpacer()

        importExport = (("Import", wx.ART_FILE_OPEN, "from"),
                        ("Export", wx.ART_FILE_SAVE_AS, "to"))

        for name, art, direction in importExport:
            bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON)
            btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)

            btn.SetMinSize(btn.GetSize())
            btn.SetMaxSize(btn.GetSize())

            btn.Layout()
            setattr(self, "{}Btn".format(name.lower()), btn)
            btn.Enable(True)
            btn.SetToolTip("%s skills %s clipboard" % (name, direction))
            bSizerButtons.Add(btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_RIGHT | wx.ALL, 5)
            btn.Bind(wx.EVT_BUTTON, getattr(self, "{}Skills".format(name.lower())))

        pmainSizer.Add(bSizerButtons, 0, wx.EXPAND, 5)

        # bind the Character selection event
        self.charEditor.entityEditor.Bind(wx.EVT_CHOICE, self.charChanged)
        self.charEditor.Bind(GE.CHAR_LIST_UPDATED, self.populateSkillTree)

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

        for level in range(6):
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

    def importSkills(self, evt):

        dlg = wx.MessageDialog(self, "Importing skills into this character will set the skill levels as pending. " +
                                     "To save the skills permanently, please click the Save button at the bottom of the window after importing"
                                     , "Import Skills", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

        text = fromClipboard().strip()
        if text:
            char = self.charEditor.entityEditor.getActiveEntity()
            try:
                lines = text.splitlines()

                for l in lines:
                    s = l.strip()
                    skill, level = s.rsplit(None, 1)[0], arabicOrRomanToInt(s.rsplit(None, 1)[1])
                    skill = char.getSkill(skill)
                    if skill:
                        skill.setLevel(level, ignoreRestrict=True)

            except Exception as e:
                dlg = wx.MessageDialog(self, "There was an error importing skills, please see log file", "Error", wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
                pyfalog.error(e)

            finally:
                self.charEditor.btnRestrict()
                self.populateSkillTree()
                self.charEditor.entityEditor.refreshEntityList(char)

    def exportSkills(self, evt):
        char = self.charEditor.entityEditor.getActiveEntity()

        skills = sorted(char.__class__.getSkillNameMap().keys())
        list = ""
        for s in skills:
            skill = char.getSkill(s)
            list += "{} {}\n".format(skill.item.name, skill.level)

        toClipboard(list)

    def onSecStatus(self, event):
        sChar = Character.getInstance()
        char = self.charEditor.entityEditor.getActiveEntity()
        myDlg = SecStatusDialog(self, char.secStatus or 0.0)
        res = myDlg.ShowModal()
        if res == wx.ID_OK:
            value = myDlg.floatSpin.GetValue()
            sChar.setSecStatus(char, value)
            self.btnSecStatus.SetLabel("Sec Status: {0:.2f}".format(value))
        myDlg.Destroy()

    def delaySearch(self, evt):
        if self.searchInput.GetValue() == "" or self.searchInput.GetValue() == self.searchInput.default_text:
            self.populateSkillTree()
        else:
            self.searchTimer.Stop()
            self.searchTimer.Start(150, True)  # 150ms

    def cloneChanged(self, event):
        sChar = Character.getInstance()
        sChar.setAlphaClone(self.charEditor.entityEditor.getActiveEntity(), event.ClientData)
        self.populateSkillTree()

    def charChanged(self, event=None):
        self.searchInput.Reset()
        char = self.charEditor.entityEditor.getActiveEntity()
        for i in range(self.clonesChoice.GetCount()):
            cloneID = self.clonesChoice.GetClientData(i)
            if char.alphaCloneID == cloneID:
                self.clonesChoice.SetSelection(i)

        self.btnSecStatus.SetLabel("Sec Status: {0:.2f}".format(char.secStatus or 0.0))

        self.populateSkillTree(event)

    def populateSkillTreeSkillSearch(self, event=None):
        sChar = Character.getInstance()
        char = self.charEditor.entityEditor.getActiveEntity()
        search = self.searchInput.GetLineText(0)

        root = self.root
        tree = self.skillTreeListCtrl
        tree.DeleteAllItems()

        for id, name in sChar.getSkillsByName(search):
            iconId = self.skillBookImageId
            level, dirty = sChar.getSkillLevel(char.ID, id)

            if dirty:
                iconId = self.skillBookDirtyImageId

            childId = tree.AppendItem(root, name, iconId, data=('skill', id))
            tree.SetItemText(childId, 1, "Level %d" % int(level) if isinstance(level, float) else level)

    def populateSkillTree(self, event=None):
        sChar = Character.getInstance()
        char = self.charEditor.entityEditor.getActiveEntity()
        dirtyGroups = set([skill.item.group.ID for skill in char.dirtySkills])

        if char.name in ("All 0", "All 5"):
            self.clonesChoice.Disable()
            self.btnSecStatus.Disable()
        else:
            self.clonesChoice.Enable()
            self.btnSecStatus.Enable()

        groups = sChar.getSkillGroups()
        root = self.root
        tree = self.skillTreeListCtrl
        tree.DeleteAllItems()

        for id, name in groups:
            imageId = self.skillBookImageId
            if id in dirtyGroups:
                imageId = self.skillBookDirtyImageId

            childId = tree.AppendItem(root, name, imageId, data=('group', id))
            tree.AppendItem(childId, "dummy")

        if event:
            event.Skip()

    def expandLookup(self, event):
        root = event.GetItem()
        tree = self.skillTreeListCtrl
        child = tree.GetFirstChild(root)
        if tree.GetItemText(child) == "dummy":
            tree.DeleteItem(child)

            # Get the real intrestin' stuff
            sChar = Character.getInstance()
            char = self.charEditor.entityEditor.getActiveEntity()
            data = tree.GetItemData(root)
            for id, name in sChar.getSkills(data[1]):
                iconId = self.skillBookImageId
                level, dirty = sChar.getSkillLevel(char.ID, id)

                if dirty:
                    iconId = self.skillBookDirtyImageId

                childId = tree.AppendItem(root, name, iconId, data=('skill', id))

                tree.SetItemText(childId, 1, "Level %d" % int(level) if isinstance(level, float) else level)

    def scheduleMenu(self, event):
        event.Skip()
        wx.CallAfter(self.spawnMenu, event.GetItem())

    def spawnMenu(self, item):
        self.skillTreeListCtrl.Select(item)
        thing = self.skillTreeListCtrl.GetFirstChild(item).IsOk()
        if thing:
            return

        char = self.charEditor.entityEditor.getActiveEntity()
        sMkt = Market.getInstance()
        id = self.skillTreeListCtrl.GetItemData(item)[1]
        if char.name not in ("All 0", "All 5"):
            self.levelChangeMenu.selection = sMkt.getItem(id)
            self.PopupMenu(self.levelChangeMenu)
        else:
            self.statsMenu.selection = sMkt.getItem(id)
            self.PopupMenu(self.statsMenu)

    def changeLevel(self, event):
        level = self.levelIds.get(event.Id)

        sChar = Character.getInstance()
        char = self.charEditor.entityEditor.getActiveEntity()
        selection = self.skillTreeListCtrl.GetSelection()
        dataType, skillID = self.skillTreeListCtrl.GetItemData(selection)

        if level is not None:
            sChar.changeLevel(char.ID, skillID, level, persist=True)
        elif event.Id == self.revertID:
            sChar.revertLevel(char.ID, skillID)
        elif event.Id == self.saveID:
            sChar.saveSkill(char.ID, skillID)

        # After saving the skill, we need to update not just the selected skill, but all open skills due to strict skill
        # level setting. We don't want to refresh tree, as that will lose all expanded categories and users location
        # within the tree. Thus, we loop through the tree and refresh the info.
        # @todo: when collapsing branch, remove the data. This will make this loop more performant

        child = self.skillTreeListCtrl.GetFirstChild(self.root)

        def _setTreeSkillLevel(treeItem, skillID):
            lvl, dirty = sChar.getSkillLevel(char.ID, skillID)
            self.skillTreeListCtrl.SetItemText(treeItem,
                                               1,
                                               "Level {}".format(int(lvl)) if not isinstance(lvl, str) else lvl)

            if not dirty:
                self.skillTreeListCtrl.SetItemImage(treeItem, self.skillBookImageId)

        while child.IsOk():
            # child = Skill category
            dataType, id = self.skillTreeListCtrl.GetItemData(child)

            if dataType == 'skill':
                _setTreeSkillLevel(child, id)
            else:
                grand = self.skillTreeListCtrl.GetFirstChild(child)
                while grand.IsOk():
                    if self.skillTreeListCtrl.GetItemText(grand) != "dummy":
                        _, skillID = self.skillTreeListCtrl.GetItemData(grand)
                        _setTreeSkillLevel(grand, skillID)
                    grand = self.skillTreeListCtrl.GetNextSibling(grand)

            child = self.skillTreeListCtrl.GetNextSibling(child)

        dirtySkills = sChar.getDirtySkills(char.ID)
        dirtyGroups = set([skill.item.group.ID for skill in dirtySkills])

        parentID = self.skillTreeListCtrl.GetItemParent(selection)
        parent = self.skillTreeListCtrl.GetItemData(parentID)

        if parent:
            if parent[1] in dirtyGroups:
                self.skillTreeListCtrl.SetItemImage(parentID, self.skillBookImageId)

        event.Skip()


class ImplantEditorView(BaseImplantEditorView):
    def __init__(self, parent, charEditor):
        BaseImplantEditorView.__init__(self, parent)

        self.determineEnabled()
        charEditor.Bind(GE.CHAR_CHANGED, self.contextChanged)

        if "__WXGTK__" in wx.PlatformInfo:
            self.pluggedImplantsTree.Bind(wx.EVT_RIGHT_UP, self.scheduleMenu)
        else:
            self.pluggedImplantsTree.Bind(wx.EVT_RIGHT_DOWN, self.scheduleMenu)

    def bindContext(self):
        self.Parent.Parent.entityEditor.Bind(wx.EVT_CHOICE, self.contextChanged)

    def contextChanged(self, event):
        BaseImplantEditorView.contextChanged(self, event)
        self.determineEnabled()

    def getImplantsFromContext(self):
        sChar = Character.getInstance()
        char = self.Parent.Parent.entityEditor.getActiveEntity()

        return sChar.getImplants(char.ID)

    def addImplantToContext(self, item):
        sChar = Character.getInstance()
        char = self.Parent.Parent.entityEditor.getActiveEntity()

        sChar.addImplant(char.ID, item.ID)

    def removeImplantFromContext(self, implant):
        sChar = Character.getInstance()
        char = self.Parent.Parent.entityEditor.getActiveEntity()

        sChar.removeImplant(char.ID, implant)

    def scheduleMenu(self, event):
        event.Skip()
        wx.CallAfter(self.spawnMenu)

    def spawnMenu(self):
        context = (("implantEditor",),)
        # fuck good coding practices, passing a pointer to the character editor here for [reasons] =D
        # (see implantSets context class for info)
        menu = ContextMenu.getMenu((self.Parent.Parent,), *context)

        if menu:
            self.PopupMenu(menu)
        else:
            pyfalog.debug("ContextMenu.getMenu returned false do not attempt PopupMenu")

    def determineEnabled(self):
        char = self.Parent.Parent.entityEditor.getActiveEntity()

        if char.name in ("All 0", "All 5"):
            self.Enable(False)
        else:
            self.Enable()


class APIView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)
        self.charEditor = self.Parent.Parent  # first parent is Notebook, second is Character Editor
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        hintSizer = wx.BoxSizer(wx.HORIZONTAL)
        hintSizer.AddStretchSpacer()
        self.stDisabledTip = wx.StaticText(self, wx.ID_ANY,
                                           "You cannot link All 0 or All 5 characters to an EVE character.\n"
                                           "Please select another character or make a new one.", style=wx.ALIGN_CENTER)
        self.stDisabledTip.Wrap(-1)
        hintSizer.Add(self.stDisabledTip, 0, wx.TOP | wx.BOTTOM, 10)

        self.stDisabledTip.Hide()
        hintSizer.AddStretchSpacer()
        pmainSizer.Add(hintSizer, 0, wx.EXPAND, 5)

        fgSizerInput = wx.FlexGridSizer(1, 3, 0, 0)
        fgSizerInput.AddGrowableCol(1)
        fgSizerInput.SetFlexibleDirection(wx.BOTH)
        fgSizerInput.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticCharText = wx.StaticText(self, wx.ID_ANY, "Character:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticCharText.Wrap(-1)
        fgSizerInput.Add(self.m_staticCharText, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)

        self.charChoice = wx.Choice(self, wx.ID_ANY, style=0)
        fgSizerInput.Add(self.charChoice, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)

        self.fetchButton = wx.Button(self, wx.ID_ANY, "Get Skills", wx.DefaultPosition, wx.DefaultSize, 0)
        self.fetchButton.Bind(wx.EVT_BUTTON, self.fetchSkills)
        fgSizerInput.Add(self.fetchButton, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)

        pmainSizer.Add(fgSizerInput, 0, wx.EXPAND, 5)

        pmainSizer.AddStretchSpacer()

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        pmainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 10)

        self.noCharactersTip = wx.StaticText(self, wx.ID_ANY, "Don't see your EVE character in the list?", style=wx.ALIGN_CENTER)

        self.noCharactersTip.Wrap(-1)
        pmainSizer.Add(self.noCharactersTip, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 0)

        self.addButton = wx.Button(self, wx.ID_ANY, "Log In with EVE SSO", wx.DefaultPosition, wx.DefaultSize, 0)
        self.addButton.Bind(wx.EVT_BUTTON, self.addCharacter)
        pmainSizer.Add(self.addButton, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        self.charEditor.mainFrame.Bind(GE.EVT_SSO_LOGOUT, self.ssoListChanged)
        self.charEditor.mainFrame.Bind(GE.EVT_SSO_LOGIN, self.ssoListChanged)
        self.charEditor.entityEditor.Bind(wx.EVT_CHOICE, self.charChanged)

        self.charChoice.Bind(wx.EVT_CHOICE, self.ssoCharChanged)

        self.SetSizer(pmainSizer)
        self.Layout()
        self.ssoListChanged(None)

    def ssoCharChanged(self, event):
        sChar = Character.getInstance()
        activeChar = self.charEditor.entityEditor.getActiveEntity()
        ssoChar = self.getActiveCharacter()
        sChar.setSsoCharacter(activeChar.ID, ssoChar)

        self.fetchButton.Enable(ssoChar is not None)

        event.Skip()

    def fetchSkills(self, evt):
        sChar = Character.getInstance()
        char = self.charEditor.entityEditor.getActiveEntity()
        sChar.apiFetch(char.ID, self.__fetchCallback)

    def addCharacter(self, event):
        sEsi = Esi.getInstance()
        sEsi.login()

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not -1 else None

    def ssoListChanged(self, event):
        if not self:  # todo: fix event not unbinding properly
            return

        self.charChanged(event)

    def charChanged(self, event):
        sChar = Character.getInstance()
        sEsi = Esi.getInstance()

        activeChar = self.charEditor.entityEditor.getActiveEntity()

        if event and event.EventType == GE.EVT_SSO_LOGIN.typeId and hasattr(event, 'character'):
            # Automatically assign the character that was just logged into
            sChar.setSsoCharacter(activeChar.ID, event.character.ID)

        sso = sChar.getSsoCharacter(activeChar.ID)

        self.fetchButton.Enable(sso is not None)

        ssoChars = sEsi.getSsoCharacters()

        self.charChoice.Clear()

        noneID = self.charChoice.Append("None", None)

        for char in ssoChars:
            currId = self.charChoice.Append(char.characterName, char.ID)

            if sso is not None and char.ID == sso.ID:
                self.charChoice.SetSelection(currId)

        if sso is None:
            self.charChoice.SetSelection(noneID)

        #
        # if chars:
        #     for charName in chars:
        #         self.charChoice.Append(charName)
        #     self.charChoice.SetStringSelection(char)
        # else:
        #     self.charChoice.Append("No characters...", 0)
        #     self.charChoice.SetSelection(0)
        #
        if activeChar.name in ("All 0", "All 5"):
            self.Enable(False)
            self.stDisabledTip.Show()
            self.Layout()
        else:
            self.Enable()
            self.stDisabledTip.Hide()
            self.Layout()

        if event is not None:
            event.Skip()

    def __fetchCallback(self, e=None):
        if e:
            exc_type, exc_obj, exc_trace = e
            pyfalog.warn("Error fetching skill information for character")
            pyfalog.warn(exc_obj)

            wx.MessageBox(
                "Error fetching skill information",
                "Error", wx.ICON_ERROR | wx.STAY_ON_TOP)
        else:
            wx.MessageBox(
                "Successfully fetched skills", "Success", wx.ICON_INFORMATION | wx.STAY_ON_TOP)


class SecStatusDialog(wx.Dialog):

    def __init__(self, parent, sec):
        wx.Dialog.__init__(self, parent, title="Set Security Status", size=(275, 175))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY,
                                        "Security Status is used in some CONCORD hull calculations; you can set the characters security status here",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 1, wx.ALL | wx.EXPAND, 5)

        self.floatSpin = FloatSpin(self, value=sec, min_val=-5.0, max_val=5.0, increment=0.1, digits=2, size=(100, -1))
        bSizer1.Add(self.floatSpin, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        btnOk = wx.Button(self, wx.ID_OK)
        bSizer1.Add(btnOk, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
