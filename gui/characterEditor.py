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
from gui import bitmapLoader
import controller

class CharacterEditor (wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"pyfa: Character Editor", pos=wx.DefaultPosition,
                            size=wx.Size(641, 450), style=wx.CAPTION | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetSizeHintsSz(wx.Size(640, 450), wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        navSizer = wx.BoxSizer(wx.HORIZONTAL)

        cChar = controller.Character.getInstance()
        charList = cChar.getCharacterList()

        choices = []
        self.charIDs = []
        for ID, name in charList:
            choices.append(name)
            self.charIDs.append(ID)

        self.skillTreeChoice = wx.Choice(self, wx.ID_ANY, choices=choices)
        navSizer.Add(self.skillTreeChoice, 1, wx.ALL | wx.EXPAND, 5)

        buttons = (("new", wx.ART_NEW),
                   ("rename", bitmapLoader.getBitmap("rename", "icons")),
                   ("copy", wx.ART_COPY),
                   ("import", wx.ART_FILE_OPEN),
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
            setattr(self, "btn%s" % name.capitalize(), btn)
            navSizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)

        mainSizer.Add(navSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.viewsNBContainer = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        self.sview = SkillTreeView(self.viewsNBContainer)
        self.iview = ImplantsTreeView(self.viewsNBContainer)
        self.aview = APIView(self.viewsNBContainer)

        self.viewsNBContainer.AddPage(self.sview, "Skills")
        self.viewsNBContainer.AddPage(self.iview, "Implants")
        self.viewsNBContainer.AddPage(self.aview, "API")

        mainSizer.Add(self.viewsNBContainer, 1, wx.EXPAND | wx.ALL, 5)

        self.descriptionBox = wx.StaticBox(self, wx.ID_ANY, u"Description")
        sbSizerDescription = wx.StaticBoxSizer(self.descriptionBox, wx.HORIZONTAL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN)

        self.description = wx.StaticText(self, wx.ID_ANY, u"\n\n\n")
        self.description.Wrap(-1)
        sbSizerDescription.Add(self.description, 0, wx.ALL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 2)

        mainSizer.Add(sbSizerDescription, 0, wx.ALL | wx.EXPAND, 5)

        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.btnOK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerButtons.Add(self.btnOK, 0, wx.ALL, 5)

        self.btnCancel = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerButtons.Add(self.btnCancel, 0, wx.ALL, 5)

        mainSizer.Add(bSizerButtons, 0, wx.ALIGN_RIGHT, 5)


        self.SetSizer(mainSizer)
        self.Layout()

        self.description.Hide()

        self.Centre(wx.BOTH)

        self.registerEvents()

    def registerEvents(self):
        self.Bind(wx.EVT_CLOSE, self.closeEvent)
        self.skillTreeChoice.Bind(wx.EVT_CHOICE, self.charChanged)
        self.sview.SkillTreeCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.updateDescription)

    def closeEvent(self, event):
        pass

    def charChanged(self, event):
        pass

    def updateDescription(self, event):
        root = event.Item
        tree = self.sview.SkillTreeCtrl
        cChar = controller.Character.getInstance()
        if tree.GetChildrenCount(root) == 0:
            description = cChar.getSkillDescription(tree.GetPyData(root))
        else:
            description = cChar.getGroupDescription(tree.GetPyData(root))

        self.description.SetLabel(description)
        self.description.Wrap(620)
        self.description.Show()

class NewCharacter (wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"Create new character", pos=wx.DefaultPosition, size=wx.Size(344, 89), style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        sbSizerEditBox = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Enter character name"), wx.HORIZONTAL)

        self.inputName = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizerEditBox.Add(self.inputName, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        mainSizer.Add(sbSizerEditBox, 1, wx.EXPAND | wx.ALL, 5)

        bSizerButtons = wx.BoxSizer(wx.VERTICAL)

        self.btnOk = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerButtons.Add(self.btnOk, 0, wx.ALL, 5)

        self.btnCancel = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerButtons.Add(self.btnCancel, 0, wx.ALL, 5)

        mainSizer.Add(bSizerButtons, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

class SkillTreeView (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL)

        pmainSizer = wx.BoxSizer(wx.VERTICAL)

        self.SkillTreeCtrl = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        pmainSizer.Add(self.SkillTreeCtrl, 1, wx.EXPAND | wx.ALL, 5)

        self.root = self.SkillTreeCtrl.AddRoot("Skills")
        self.imageList = wx.ImageList(16, 16)
        self.SkillTreeCtrl.SetImageList(self.imageList)
        self.skillBookImageId = self.imageList.Add(bitmapLoader.getBitmap("skill_small", "icons"))

        self.populateSkillTree()

        self.SkillTreeCtrl.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)

        self.SetSizer(pmainSizer)
        self.Layout()

    def populateSkillTree(self):
        cChar = controller.Character.getInstance()
        groups = cChar.getSkillGroups()
        imageId = self.skillBookImageId
        root = self.root
        tree = self.SkillTreeCtrl

        for id, name in groups:
            childId = tree.AppendItem(root, name, imageId, data=wx.TreeItemData(id))
            tree.AppendItem(childId, "dummy")

        self.SkillTreeCtrl.SortChildren(root)

    def expandLookup(self, event):
        root = event.Item
        child, cookie = self.SkillTreeCtrl.GetFirstChild(root)
        if self.SkillTreeCtrl.GetItemText(child) == "dummy":
            self.SkillTreeCtrl.Delete(child)

            #Get the real intrestin' stuff
            cChar = controller.Character.getInstance()
            for id, name in cChar.getSkills(self.SkillTreeCtrl.GetPyData(root)):
                iconId = self.skillBookImageId
                self.SkillTreeCtrl.AppendItem(root, name, iconId, data=wx.TreeItemData(id))

            self.SkillTreeCtrl.SortChildren(root)

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

        pmainSizer = wx.BoxSizer(wx.HORIZONTAL)

        fgSizerInput = wx.FlexGridSizer(2, 2, 0, 0)
        fgSizerInput.AddGrowableCol(1)
        fgSizerInput.SetFlexibleDirection(wx.BOTH)
        fgSizerInput.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticIDText = wx.StaticText(self, wx.ID_ANY, u"ID", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticIDText.Wrap(-1)
        fgSizerInput.Add(self.m_staticIDText, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.inputID = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerInput.Add(self.inputID, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticKeyText = wx.StaticText(self, wx.ID_ANY, u"API KEY", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticKeyText.Wrap(-1)
        fgSizerInput.Add(self.m_staticKeyText, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.inputKey = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerInput.Add(self.inputKey, 0, wx.ALL | wx.EXPAND, 5)

        pmainSizer.Add(fgSizerInput, 1, wx.EXPAND, 5)

        self.btnUpdate = wx.Button(self, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0)
        pmainSizer.Add(self.btnUpdate, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.SetSizer(pmainSizer)
        self.Layout()

