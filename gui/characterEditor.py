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
import traceback

import roman
# noinspection PyPackageRequirements
import wx
import wx.dataview
import wx.lib.agw.hyperlink
# noinspection PyPackageRequirements
import wx.lib.newevent
from logbook import Logger
# noinspection PyPackageRequirements
from wx.dataview import TreeListCtrl
from wx.lib.agw.floatspin import FloatSpin

import config
import gui.globalEvents as GE
from gui.auxWindow import AuxiliaryFrame
from gui.bitmap_loader import BitmapLoader
from gui.builtinViews.entityEditor import BaseValidator, EntityEditor, TextEntryValidatedDialog
from gui.builtinViews.implantEditor import BaseImplantEditorView
from gui.contextMenu import ContextMenu
from gui.utils.clipboard import fromClipboard, toClipboard
from service.character import Character
from service.esi import Esi
from service.esiAccess import APIException
from service.fit import Fit
from service.market import Market

_t = wx.GetTranslation

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
                raise ValueError(_t("You must supply a name for the Character!"))
            elif text in [x.name for x in sChar.getCharacterList()]:
                raise ValueError(_t("Character name already in use, please choose another."))

            return True
        except ValueError as e:
            pyfalog.error(e)
            wx.MessageBox("{}".format(e), _t("Error"))
            textCtrl.SetFocus()
            return False


class CharacterEntityEditor(EntityEditor):
    def __init__(self, parent):
        EntityEditor.__init__(self, parent, _t("Character"))
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

        if entity.alphaCloneID:
            trimmed_name = re.sub('[ \(\u03B1\)]+$', '', name)
            sChar.rename(entity, trimmed_name)
        else:
            sChar.rename(entity, name)

    def DoCopy(self, entity, name):
        sChar = Character.getInstance()
        copy = sChar.copy(entity)
        sChar.rename(copy, name)
        return copy

    def DoDelete(self, entity):
        sChar = Character.getInstance()
        sChar.delete(entity)


class CharacterEditor(AuxiliaryFrame):

    def __init__(self, parent):
        super().__init__(
            parent, id=wx.ID_ANY, title=_t("Character Editor"), resizeable=True, pos=wx.DefaultPosition,
            size=wx.Size(950, 650) if "wxGTK" in wx.PlatformInfo else wx.Size(850, 600))

        i = wx.Icon(BitmapLoader.getBitmap("character_small", "gui"))
        self.SetIcon(i)

        self.mainFrame = parent
        # self.disableWin = wx.WindowDisabler(self)
        sFit = Fit.getInstance()

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.entityEditor = CharacterEntityEditor(self)
        mainSizer.Add(self.entityEditor, 0, wx.ALL | wx.EXPAND, 2)
        # Default drop down to current fit's character
        self.entityEditor.setActiveEntity(sFit.character)

        self.viewsNBContainer = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        self.sview = SkillTreeView(self.viewsNBContainer)
        self.iview = ImplantEditorView(self.viewsNBContainer, self)
        self.aview = APIView(self.viewsNBContainer)

        self.viewsNBContainer.AddPage(self.sview, _t("Skills"))
        self.viewsNBContainer.AddPage(self.iview, _t("Implants"))
        self.viewsNBContainer.AddPage(self.aview, _t("EVE SSO"))

        mainSizer.Add(self.viewsNBContainer, 1, wx.EXPAND | wx.ALL, 5)

        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.btnSaveChar = wx.Button(self, wx.ID_SAVE)
        self.btnSaveAs = wx.Button(self, wx.ID_SAVEAS)
        self.btnRevert = wx.Button(self, wx.ID_REVERT_TO_SAVED)
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

        self.SetMinSize(self.GetSize())
        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)
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
        self.Close()

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

    def kbEvent(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE and event.GetModifiers() == wx.MOD_NONE:
            self.Close()
            return
        event.Skip()

    def OnClose(self, event):
        wx.PostEvent(self.mainFrame, GE.CharListUpdated())
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        if fitID is not None:
            sFit.clearFit(fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))
        event.Skip()

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

    @staticmethod
    def SaveCharacterAs(parent, charID):
        sChar = Character.getInstance()
        name = sChar.getCharName(charID)

        with TextEntryValidatedDialog(
            parent, CharacterTextValidor,
            _t("Enter a name for your new Character:"),
            _t("Save Character As...")
        ) as dlg:
            dlg.SetValue(_t("{} Copy").format(name))
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

        self.searchInput = wx.SearchCtrl(self, wx.ID_ANY)
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
            wx.ToolTip(_t("Setting an Alpha clone does not replace the character's skills, but rather caps them to Alpha levels.")))

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

        tree.AppendColumn(_t("Skill"))
        tree.AppendColumn(_t("Level"))
        # tree.SetMainColumn(0)

        self.root = tree.GetRootItem()
        # self.root = tree.AppendItem(root, "Skills")
        #
        # tree.SetItemText(self.root, 1, "Levels")

        # first one doesn't work right in Windows. Second one doesn't work right in GTK. Together, we make sure it works.
        # Gotta love wx
        tree.SetColumnWidth(0, 525)
        tree.SetColumnWidth(1, 100)

        self.secStatusLabel = _t("Sec Status: {0:.2f}")
        self.btnSecStatus = wx.Button(self, wx.ID_ANY, self.secStatusLabel.format(char.secStatus or 0.0))
        self.btnSecStatus.Bind(wx.EVT_BUTTON, self.onSecStatus)

        self.populateSkillTree()

        tree.Bind(wx.dataview.EVT_TREELIST_ITEM_ACTIVATED, self.expand)
        tree.Bind(wx.dataview.EVT_TREELIST_ITEM_EXPANDING, self.expandLookup)
        tree.Bind(wx.dataview.EVT_TREELIST_ITEM_CONTEXT_MENU, self.spawnMenu)

        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        bSizerButtons.Add(self.btnSecStatus, 0, wx.ALL, 5)

        bSizerButtons.AddStretchSpacer()

        importExport = ((_t("Import skills from clipboard"), wx.ART_FILE_OPEN, "import"),
                        (_t("Export skills from clipboard"), wx.ART_FILE_SAVE_AS, "export"))

        for tooltip, art, attr in importExport:
            bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON)
            btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)

            btn.SetMinSize(btn.GetSize())
            btn.SetMaxSize(btn.GetSize())

            btn.Layout()
            setattr(self, "{}Btn".format(attr), btn)
            btn.Enable(True)
            btn.SetToolTip(tooltip)
            bSizerButtons.Add(btn, 0, wx.ALL, 5)
            btn.Bind(wx.EVT_BUTTON, getattr(self, "{}Skills".format(attr)))

        pmainSizer.Add(bSizerButtons, 0, wx.EXPAND, 5)

        # bind the Character selection event
        self.charEditor.entityEditor.Bind(wx.EVT_CHOICE, self.charChanged)
        self.charEditor.Bind(GE.CHAR_LIST_UPDATED, self.populateSkillTree)

        # Context menu stuff
        self.idUnlearned = wx.NewId()
        self.levelIds = {}
        self.idLevels = {}
        self.levelIds[self.idUnlearned] = _t("Not learned")
        for level in range(6):
            id = wx.NewId()
            self.levelIds[id] = level
            self.idLevels[level] = id
        self.revertID = wx.NewId()
        self.saveID = wx.NewId()

        self.SetSizer(pmainSizer)

        # This cuases issues with GTK, see #1866
        # self.Layout()

        # For level keyboard shortcuts
        self.ChangeLevelEvent, CHANGE_LEVEL_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)
        self.Bind(CHANGE_LEVEL_EVENT, self.changeLevel)

    def kbEvent(self, event):
        keyLevelMap = {
            # Regular number keys
            48: 0, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5,
            # Numpad keys
            wx.WXK_NUMPAD0: 0, wx.WXK_NUMPAD1: 1, wx.WXK_NUMPAD2: 2,
            wx.WXK_NUMPAD3: 3, wx.WXK_NUMPAD4: 4, wx.WXK_NUMPAD5: 5}
        keycode = event.GetKeyCode()
        if keycode in keyLevelMap and event.GetModifiers() == wx.MOD_NONE:
            level = keyLevelMap[keycode]
            selection = self.skillTreeListCtrl.GetSelection()
            if selection:
                dataType, skillID = self.skillTreeListCtrl.GetItemData(selection)
                if dataType == 'skill':
                    event = self.ChangeLevelEvent()
                    event.SetId(self.idLevels[level])
                    wx.PostEvent(self, event)
                    return
        event.Skip()

    def importSkills(self, evt):

        with wx.MessageDialog(
            self, (_t("Importing skills into this character will set the skill levels as pending. To save the skills "
                   "permanently, please click the Save button at the bottom of the window after importing")),
            _t("Import Skills"), wx.OK
        ) as dlg:
            dlg.ShowModal()

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

            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                pyfalog.error(e)
                with wx.MessageDialog(self, _t("There was an error importing skills, please see log file"), _t("Error"), wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()

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
        with SecStatusDialog(self, char.secStatus or 0.0) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                value = dlg.floatSpin.GetValue()
                sChar.setSecStatus(char, value)
                self.btnSecStatus.SetLabel(self.secStatusLabel.format(value))

    def delaySearch(self, evt):
        if self.searchInput.GetValue() == "":
            self.populateSkillTree()
        else:
            self.searchTimer.Stop()
            self.searchTimer.Start(150, True)  # 150ms

    def cloneChanged(self, event):
        sChar = Character.getInstance()
        sChar.setAlphaClone(self.charEditor.entityEditor.getActiveEntity(), event.ClientData)
        self.populateSkillTree()

    def charChanged(self, event=None):
        self.searchInput.SetValue("")
        char = self.charEditor.entityEditor.getActiveEntity()
        for i in range(self.clonesChoice.GetCount()):
            cloneID = self.clonesChoice.GetClientData(i)
            if char.alphaCloneID == cloneID:
                self.clonesChoice.SetSelection(i)

        self.btnSecStatus.SetLabel(self.secStatusLabel.format(char.secStatus or 0.0))

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
            tree.SetItemText(childId, 1, _t("Level {}d").format(int(level)) if isinstance(level, float) else level)

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

    def expand(self, event):
        root = event.GetItem()
        tree = self.skillTreeListCtrl
        if tree.IsExpanded(root):
            tree.Collapse(root)
        else:
            tree.Expand(root)

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

                tree.SetItemText(childId, 1, _t("Level {}").format(int(level)) if isinstance(level, float) else level)

    def spawnMenu(self, event):
        item = event.GetItem()
        itemData = self.skillTreeListCtrl.GetItemData(item)
        if itemData is None:
            return

        self.skillTreeListCtrl.Select(item)
        thing = self.skillTreeListCtrl.GetFirstChild(item).IsOk()
        if thing:
            return

        id = itemData[1]
        eveItem = Market.getInstance().getItem(id)

        srcContext = "skillItem"
        itemContext = _t("Skill")
        context = (srcContext, itemContext)
        menu = ContextMenu.getMenu(self, eveItem, [eveItem], context)
        char = self.charEditor.entityEditor.getActiveEntity()
        if char.name not in ("All 0", "All 5"):
            menu.AppendSeparator()
            menu.Append(self.idUnlearned, _t("Unlearn"))
            for level in range(6):
                menu.Append(self.idLevels[level], _t("Level {}").format(level))
            menu.Bind(wx.EVT_MENU, self.changeLevel)

        self.PopupMenu(menu)

    def changeLevel(self, event):
        level = self.levelIds.get(event.Id)

        sChar = Character.getInstance()
        char = self.charEditor.entityEditor.getActiveEntity()
        if char.name in ("All 0", "All 5"):
            return
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
                                               _t("Level {}").format(int(lvl)) if not isinstance(lvl, str) else lvl)

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

        self.pluggedImplantsTree.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

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

    def addImplants(self, implants):
        charEditor = self.Parent.Parent
        char = charEditor.entityEditor.getActiveEntity()

        sChar = Character.getInstance()
        for implant in implants:
            sChar.addImplant(char.ID, implant.item.ID)

        wx.PostEvent(charEditor, GE.CharChanged())

    def spawnMenu(self, event):
        context = (("implantEditor",),)
        menu = ContextMenu.getMenu(self, None, None, *context)

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
                                           _t("You cannot link All 0 or All 5 characters to an EVE character.") + "\n" +
                                           _t("Please select another character or make a new one."), style=wx.ALIGN_CENTER)
        self.stDisabledTip.Wrap(-1)
        hintSizer.Add(self.stDisabledTip, 0, wx.TOP | wx.BOTTOM, 10)

        self.stDisabledTip.Hide()
        hintSizer.AddStretchSpacer()
        pmainSizer.Add(hintSizer, 0, wx.EXPAND, 5)

        fgSizerInput = wx.FlexGridSizer(1, 3, 0, 0)
        fgSizerInput.AddGrowableCol(1)
        fgSizerInput.SetFlexibleDirection(wx.BOTH)
        fgSizerInput.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticCharText = wx.StaticText(self, wx.ID_ANY, _t("Character:"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticCharText.Wrap(-1)
        fgSizerInput.Add(self.m_staticCharText, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)

        self.charChoice = wx.Choice(self, wx.ID_ANY, style=0)
        fgSizerInput.Add(self.charChoice, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)

        self.fetchButton = wx.Button(self, wx.ID_ANY, _t("Get Skills"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.fetchButton.Bind(wx.EVT_BUTTON, self.fetchSkills)
        fgSizerInput.Add(self.fetchButton, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)

        pmainSizer.Add(fgSizerInput, 0, wx.EXPAND, 5)

        pmainSizer.AddStretchSpacer()

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        pmainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 10)

        self.noCharactersTip = wx.StaticText(self, wx.ID_ANY, _t("Don't see your EVE character in the list?"), style=wx.ALIGN_CENTER)

        self.noCharactersTip.Wrap(-1)
        pmainSizer.Add(self.noCharactersTip, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 0)

        self.addButton = wx.Button(self, wx.ID_ANY, _t("Log In with EVE SSO"), wx.DefaultPosition, wx.DefaultSize, 0)
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
        sChar.apiFetch(char.ID, APIView.fetchCallback)

    def addCharacter(self, event):
        sEsi = Esi.getInstance()
        sEsi.login()

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection != -1 else None

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

        noneID = self.charChoice.Append(_t("None"), None)

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

    @staticmethod
    def fetchCallback(e=None):
        if e:
            pyfalog.warn("Error fetching skill information for character for __fetchCallback")
            SkillFetchExceptionHandler(e)
        else:
            wx.MessageBox(
                _t("Successfully fetched skills"), _t("Success"), wx.ICON_INFORMATION | wx.STAY_ON_TOP)


class SecStatusDialog(wx.Dialog):

    def __init__(self, parent, sec):
        super().__init__(parent, title=_t("Set Security Status"), size=(300, 175), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY,
                                           _t("Security Status is used in some CONCORD hull calculations"),
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 1, wx.ALL | wx.EXPAND, 5)

        self.floatSpin = FloatSpin(self, value=sec, min_val=-5.0, max_val=5.0, increment=0.1, digits=2, size=(-1, -1))
        bSizer1.Add(self.floatSpin, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        btnOk = wx.Button(self, wx.ID_OK)
        bSizer1.Add(btnOk, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Center(wx.BOTH)


class SkillFetchExceptionHandler:
    def __init__(self, e):
        from gui.esiFittings import ESIExceptionHandler
        exc_type, exc_value, exc_trace = e
        if config.debug:
            exc_value = ''.join(traceback.format_exception(exc_type, exc_value, exc_trace))
        pyfalog.warn(exc_value)

        try:
            try:
                raise exc_value
            except APIException as ex:
                pyfalog.error(ex)
                ESIExceptionHandler(ex)
        except Exception as ex:
            pyfalog.error(ex)
            wx.MessageBox(
                _t("Error fetching skill information"),
                _t("Error"), wx.ICON_ERROR | wx.STAY_ON_TOP)
