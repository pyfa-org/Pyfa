# =============================================================================
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
# =============================================================================

from logbook import Logger
# noinspection PyPackageRequirements
import wx

from service.implantSet import ImplantSets
from gui.builtinViews.implantEditor import BaseImplantEditorView
from gui.utils.clipboard import toClipboard, fromClipboard
from gui.builtinViews.entityEditor import EntityEditor, BaseValidator

pyfalog = Logger(__name__)


class ImplantTextValidor(BaseValidator):
    def __init__(self):
        BaseValidator.__init__(self)

    def Clone(self):
        return ImplantTextValidor()

    def Validate(self, win):
        entityEditor = win.parent
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()

        try:
            if len(text) == 0:
                raise ValueError("You must supply a name for the Implant Set!")
            elif text in [x.name for x in entityEditor.choices]:
                raise ValueError("Imlplant Set name already in use, please choose another.")

            return True
        except ValueError as e:
            pyfalog.error(e)
            wx.MessageBox(u"{}".format(e), "Error")
            textCtrl.SetFocus()
            return False


class ImplantSetEntityEditor(EntityEditor):
    def __init__(self, parent):
        EntityEditor.__init__(self, parent, "Implant Set")
        self.SetEditorValidator(ImplantTextValidor)

    def getEntitiesFromContext(self):
        sIS = ImplantSets.getInstance()
        return sorted(sIS.getImplantSetList(), key=lambda c: c.name)

    def DoNew(self, name):
        sIS = ImplantSets.getInstance()
        return sIS.newSet(name)

    def DoRename(self, entity, name):
        sIS = ImplantSets.getInstance()
        sIS.renameSet(entity, name)

    def DoCopy(self, entity, name):
        sIS = ImplantSets.getInstance()
        copy = sIS.copySet(entity)
        sIS.renameSet(copy, name)
        return copy

    def DoDelete(self, entity):
        sIS = ImplantSets.getInstance()
        sIS.deleteSet(entity)


class ImplantSetEditor(BaseImplantEditorView):
    def __init__(self, parent):
        BaseImplantEditorView.__init__(self, parent)
        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

    def bindContext(self):
        self.Parent.entityEditor.Bind(wx.EVT_CHOICE, self.contextChanged)

    def getImplantsFromContext(self):
        sIS = ImplantSets.getInstance()
        set_ = self.Parent.entityEditor.getActiveEntity()
        if set_:
            return sIS.getImplants(set_.ID)
        return []

    def addImplantToContext(self, item):
        sIS = ImplantSets.getInstance()
        set_ = self.Parent.entityEditor.getActiveEntity()

        sIS.addImplant(set_.ID, item.ID)

    def removeImplantFromContext(self, implant):
        sIS = ImplantSets.getInstance()
        set_ = self.Parent.entityEditor.getActiveEntity()

        sIS.removeImplant(set_.ID, implant)


class ImplantSetEditorDlg(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Implant Set Editor", size=wx.Size(640, 600))

        self.block = False
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.entityEditor = ImplantSetEntityEditor(self)
        mainSizer.Add(self.entityEditor, 0, wx.ALL | wx.EXPAND, 2)

        self.sl = wx.StaticLine(self)
        mainSizer.Add(self.sl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.iview = ImplantSetEditor(self)
        mainSizer.Add(self.iview, 1, wx.ALL | wx.EXPAND, 5)

        self.slfooter = wx.StaticLine(self)
        mainSizer.Add(self.slfooter, 0, wx.EXPAND | wx.TOP, 5)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.stNotice = wx.StaticText(self, wx.ID_ANY, u"")
        self.stNotice.Wrap(-1)
        footerSizer.Add(self.stNotice, 1, wx.BOTTOM | wx.TOP | wx.LEFT, 5)

        if "wxGTK" in wx.PlatformInfo:
            self.closeBtn = wx.Button(self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0)
            mainSizer.Add(self.closeBtn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
            self.closeBtn.Bind(wx.EVT_BUTTON, self.closeEvent)

        importExport = (("Import", wx.ART_FILE_OPEN, "from"),
                        ("Export", wx.ART_FILE_SAVE_AS, "to"))

        for name, art, direction in importExport:
            bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON)
            btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)

            btn.SetMinSize(btn.GetSize())
            btn.SetMaxSize(btn.GetSize())

            btn.Layout()
            setattr(self, name, btn)
            btn.Enable(True)
            btn.SetToolTipString("%s implant sets %s clipboard" % (name, direction))
            footerSizer.Add(btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_RIGHT)

        mainSizer.Add(footerSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        if not self.entityEditor.checkEntitiesExist():
            self.Destroy()
            return

        self.Bind(wx.EVT_CHOICE, self.entityChanged)

        self.Import.Bind(wx.EVT_BUTTON, self.importPatterns)
        self.Export.Bind(wx.EVT_BUTTON, self.exportPatterns)

        self.CenterOnParent()
        self.ShowModal()

    def entityChanged(self, event):
        if not self.entityEditor.checkEntitiesExist():
            self.Destroy()
            return

    def closeEvent(self, event):
        self.Destroy()

    def __del__(self):
        pass

    def importPatterns(self, event):
        """Event fired when import from clipboard button is clicked"""

        text = fromClipboard()
        if text:
            sIS = ImplantSets.getInstance()
            try:
                sIS.importSets(text)
                self.stNotice.SetLabel("Patterns successfully imported from clipboard")
            except ImportError as e:
                pyfalog.error(e)
                self.stNotice.SetLabel(str(e))
            except Exception as e:
                pyfalog.error(e)
                self.stNotice.SetLabel("Could not import from clipboard: unknown errors")
            finally:
                self.entityEditor.refreshEntityList()
        else:
            self.stNotice.SetLabel("Could not import from clipboard")

    def exportPatterns(self, event):
        """Event fired when export to clipboard button is clicked"""

        sIS = ImplantSets.getInstance()
        toClipboard(sIS.exportSets())
        self.stNotice.SetLabel("Sets exported to clipboard")
