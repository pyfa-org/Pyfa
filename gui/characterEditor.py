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

from utils.floatspin import FloatSpin
# noinspection PyPackageRequirements
import wx.lib.newevent
# noinspection PyPackageRequirements
import wx.gizmos
from gui.bitmapLoader import BitmapLoader
from gui.contextMenu import ContextMenu
import gui.globalEvents as GE
from gui.builtinViews.implantEditor import BaseImplantEditorView
from gui.builtinViews.entityEditor import EntityEditor, BaseValidator, TextEntryValidatedDialog
from service.fit import Fit
from service.character import Character
from service.network import AuthenticationError, TimeoutError
from service.market import Market
from logbook import Logger

from gui.utils.clipboard import toClipboard, fromClipboard

import utils.roman as roman
import re

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
        except ValueError, e:
            pyfalog.error(e)
            wx.MessageBox(u"{}".format(e), "Error")
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
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"pyfa: Character Editor", pos=wx.DefaultPosition,
                          size=wx.Size(640, 600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        i = wx.IconFromBitmap(BitmapLoader.getBitmap("character_small", "gui"))
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
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

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

        self.btnSecStatus = wx.Button(self, wx.ID_ANY, "Sec Status: {0:.2f}".format(char.secStatus or 0.0))
        self.btnSecStatus.Bind(wx.EVT_BUTTON, self.onSecStatus)

        self.populateSkillTree()

        tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)
        tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.scheduleMenu)

        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        bSizerButtons.Add(self.btnSecStatus, 0, wx.ALL, 5)

        bSizerButtons.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
            btn.SetToolTipString("%s skills %s clipboard" % (name, direction))
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
        tree.DeleteChildren(root)

        for id, name in sChar.getSkillsByName(search):
            iconId = self.skillBookImageId
            childId = tree.AppendItem(root, name, iconId, data=wx.TreeItemData(('skill', id)))
            level, dirty = sChar.getSkillLevel(char.ID, id)
            tree.SetItemText(childId, "Level %d" % int(level) if isinstance(level, float) else level, 1)
            if dirty:
                tree.SetItemTextColour(childId, wx.BLUE)

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
        imageId = self.skillBookImageId
        root = self.root
        tree = self.skillTreeListCtrl
        tree.DeleteChildren(root)

        for id, name in groups:
            childId = tree.AppendItem(root, name, imageId)
            tree.SetPyData(childId, ('group', id))
            tree.AppendItem(childId, "dummy")
            if id in dirtyGroups:
                tree.SetItemTextColour(childId, wx.BLUE)

        tree.SortChildren(root)

        if event:
            event.Skip()

    def expandLookup(self, event):
        root = event.Item
        tree = self.skillTreeListCtrl
        child, cookie = tree.GetFirstChild(root)
        if tree.GetItemText(child) == "dummy":
            tree.Delete(child)

            # Get the real intrestin' stuff
            sChar = Character.getInstance()
            char = self.charEditor.entityEditor.getActiveEntity()
            data = tree.GetPyData(root)
            for id, name in sChar.getSkills(data[1]):
                iconId = self.skillBookImageId
                childId = tree.AppendItem(root, name, iconId, data=wx.TreeItemData(('skill', id)))
                level, dirty = sChar.getSkillLevel(char.ID, id)
                tree.SetItemText(childId, "Level %d" % int(level) if isinstance(level, float) else level, 1)
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

        char = self.charEditor.entityEditor.getActiveEntity()
        sMkt = Market.getInstance()
        id = self.skillTreeListCtrl.GetPyData(item)[1]
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
        dataType, skillID = self.skillTreeListCtrl.GetPyData(selection)

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
        child, cookie = self.skillTreeListCtrl.GetFirstChild(self.root)

        def _setTreeSkillLevel(treeItem, skillID):
            lvl, dirty = sChar.getSkillLevel(char.ID, skillID)
            self.skillTreeListCtrl.SetItemText(treeItem,
                                               "Level {}".format(int(lvl)) if not isinstance(lvl, basestring) else lvl,
                                               1)
            if not dirty:
                self.skillTreeListCtrl.SetItemTextColour(treeItem, None)

        while child.IsOk():
            # child = Skill category
            dataType, id = self.skillTreeListCtrl.GetPyData(child)
            if dataType == 'skill':
                _setTreeSkillLevel(child, id)
            else:
                grand, cookie2 = self.skillTreeListCtrl.GetFirstChild(child)

                while grand.IsOk():
                    if self.skillTreeListCtrl.GetItemText(grand) != "dummy":
                        _, skillID = self.skillTreeListCtrl.GetPyData(grand)
                        _setTreeSkillLevel(grand, skillID)
                    grand, cookie2 = self.skillTreeListCtrl.GetNextChild(child, cookie2)

            child, cookie = self.skillTreeListCtrl.GetNextChild(self.root, cookie)

        dirtySkills = sChar.getDirtySkills(char.ID)
        dirtyGroups = set([skill.item.group.ID for skill in dirtySkills])

        parentID = self.skillTreeListCtrl.GetItemParent(selection)
        parent = self.skillTreeListCtrl.GetPyData(parentID)

        if parent:
            if parent[1] in dirtyGroups:
                self.skillTreeListCtrl.SetItemTextColour(parentID, None)

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
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

        self.apiUrlCreatePredefined = u"https://community.eveonline.com/support/api-key/CreatePredefined?accessMask=8"
        self.apiUrlKeyList = u"https://community.eveonline.com/support/api-key/"

        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        hintSizer = wx.BoxSizer(wx.HORIZONTAL)
        hintSizer.AddStretchSpacer()
        self.stDisabledTip = wx.StaticText(self, wx.ID_ANY,
                                           u"You cannot add API Details for All 0 and All 5 characters.\n"
                                           u"Please select another character or make a new one.", style=wx.ALIGN_CENTER)
        self.stDisabledTip.Wrap(-1)
        hintSizer.Add(self.stDisabledTip, 0, wx.TOP | wx.BOTTOM, 10)
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

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddStretchSpacer()

        self.btnFetchCharList = wx.Button(self, wx.ID_ANY, u"Get Characters")
        btnSizer.Add(self.btnFetchCharList, 0, wx.ALL, 2)
        self.btnFetchCharList.Bind(wx.EVT_BUTTON, self.fetchCharList)

        self.btnFetchSkills = wx.Button(self, wx.ID_ANY, u"Fetch Skills")
        btnSizer.Add(self.btnFetchSkills, 0, wx.ALL, 2)
        self.btnFetchSkills.Bind(wx.EVT_BUTTON, self.fetchSkills)
        self.btnFetchSkills.Enable(False)

        btnSizer.AddStretchSpacer()
        pmainSizer.Add(btnSizer, 0, wx.EXPAND, 5)

        self.stStatus = wx.StaticText(self, wx.ID_ANY, wx.EmptyString)
        pmainSizer.Add(self.stStatus, 0, wx.ALL, 5)

        pmainSizer.AddStretchSpacer()
        self.stAPITip = wx.StaticText(self, wx.ID_ANY,
                                      u"You can create a pre-defined key here (only CharacterSheet is required):",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.stAPITip.Wrap(-1)

        pmainSizer.Add(self.stAPITip, 0, wx.ALL, 2)

        self.hlEveAPI = wx.HyperlinkCtrl(self, wx.ID_ANY, self.apiUrlCreatePredefined, self.apiUrlCreatePredefined,
                                         wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE)
        pmainSizer.Add(self.hlEveAPI, 0, wx.ALL, 2)

        self.stAPITip2 = wx.StaticText(self, wx.ID_ANY, u"Or, you can choose an existing key from:", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.stAPITip2.Wrap(-1)
        pmainSizer.Add(self.stAPITip2, 0, wx.ALL, 2)

        self.hlEveAPI2 = wx.HyperlinkCtrl(self, wx.ID_ANY, self.apiUrlKeyList, self.apiUrlKeyList, wx.DefaultPosition,
                                          wx.DefaultSize, wx.HL_DEFAULT_STYLE)
        pmainSizer.Add(self.hlEveAPI2, 0, wx.ALL, 2)

        self.charEditor.entityEditor.Bind(wx.EVT_CHOICE, self.charChanged)

        self.SetSizer(pmainSizer)
        self.Layout()
        self.charChanged(None)

    def charChanged(self, event):
        sChar = Character.getInstance()
        activeChar = self.charEditor.entityEditor.getActiveEntity()

        ID, key, char, chars = sChar.getApiDetails(activeChar.ID)
        self.inputID.SetValue(str(ID))
        self.inputKey.SetValue(key)

        self.charChoice.Clear()

        if chars:
            for charName in chars:
                self.charChoice.Append(charName)
            self.charChoice.SetStringSelection(char)
            self.charChoice.Enable(True)
            self.btnFetchSkills.Enable(True)
        else:
            self.charChoice.Append("No characters...", 0)
            self.charChoice.SetSelection(0)
            self.charChoice.Enable(False)
            self.btnFetchSkills.Enable(False)

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

    def fetchCharList(self, event):
        self.stStatus.SetLabel("")
        if self.inputID.GetLineText(0) == "" or self.inputKey.GetLineText(0) == "":
            self.stStatus.SetLabel("Invalid keyID or vCode!")
            return

        sChar = Character.getInstance()
        try:
            activeChar = self.charEditor.entityEditor.getActiveEntity()
            list = sChar.apiCharList(activeChar.ID, self.inputID.GetLineText(0), self.inputKey.GetLineText(0))
        except AuthenticationError, e:
            msg = "Authentication failure. Please check keyID and vCode combination."
            pyfalog.info(msg)
            self.stStatus.SetLabel(msg)
        except TimeoutError, e:
            msg = "Request timed out. Please check network connectivity and/or proxy settings."
            pyfalog.info(msg)
            self.stStatus.SetLabel(msg)
        except Exception, e:
            pyfalog.error(e)
            self.stStatus.SetLabel("Error:\n%s" % e.message)
        else:
            self.charChoice.Clear()
            for charName in list:
                self.charChoice.Append(charName)

            self.btnFetchSkills.Enable(True)
            self.charChoice.Enable(True)

            self.Layout()

            self.charChoice.SetSelection(0)

    def fetchSkills(self, event):
        charName = self.charChoice.GetString(self.charChoice.GetSelection())
        if charName:
            sChar = Character.getInstance()
            activeChar = self.charEditor.entityEditor.getActiveEntity()
            sChar.apiFetch(activeChar.ID, charName, self.__fetchCallback)
            self.stStatus.SetLabel("Getting skills for {}".format(charName))

    def __fetchCallback(self, e=None):
        charName = self.charChoice.GetString(self.charChoice.GetSelection())
        if e is None:
            self.stStatus.SetLabel("Successfully fetched {}\'s skills from EVE API.".format(charName))
        else:
            exc_type, exc_obj, exc_trace = e
            pyfalog.error("Unable to retrieve {0}\'s skills. Error message:\n{1}".format(charName, exc_obj))
            self.stStatus.SetLabel("Unable to retrieve {}\'s skills. Error message:\n{}".format(charName, exc_obj))


class SecStatusDialog(wx.Dialog):

    def __init__(self, parent, sec):
        wx.Dialog.__init__(self, parent, title="Set Security Status", size=(275, 175))

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY,
                                        u"Security Status is used in some CONCORD hull calculations; you can set the characters security status here",
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
