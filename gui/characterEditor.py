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

class CharacterEditor (wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"pyfa: Character Editor", pos=wx.DefaultPosition,
                            size=wx.Size(641, 377), style=wx.CAPTION | wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER)

        self.SetSizeHintsSz(wx.Size(640, 350), wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        navSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.skillTreeChoice = wx.Choice(self, wx.ID_ANY)
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

        sview = SkillTreeView(self.viewsNBContainer)
        iview = ImplantsTreeView(self.viewsNBContainer)
        aview = APIView(self.viewsNBContainer)

        self.viewsNBContainer.AddPage(sview, "Skills")
        self.viewsNBContainer.AddPage(iview, "Implants")
        self.viewsNBContainer.AddPage(aview, "API")

        mainSizer.Add(self.viewsNBContainer, 1, wx.EXPAND | wx.ALL, 5)

        sbSizerDescription = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Description"), wx.HORIZONTAL)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"Insert descriptions here", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        sbSizerDescription.Add(self.m_staticText7, 0, wx.ALL, 5)

        mainSizer.Add(sbSizerDescription, 0, wx.ALL | wx.EXPAND, 5)

        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.btnOK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerButtons.Add(self.btnOK, 0, wx.ALL, 5)

        self.btnCancel = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerButtons.Add(self.btnCancel, 0, wx.ALL, 5)

        mainSizer.Add(bSizerButtons, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.registerEvents()

    def registerEvents(self):
        self.Bind(wx.EVT_CLOSE, self.closeEvent)

    def closeEvent(self, event):
        pass

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

        self.SkillTreeCtrl = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE)
        pmainSizer.Add(self.SkillTreeCtrl, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(pmainSizer)
        self.Layout()

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

