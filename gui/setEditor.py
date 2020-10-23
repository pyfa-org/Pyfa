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

# noinspection PyPackageRequirements
import wx
from logbook import Logger

from gui.auxWindow import AuxiliaryFrame
from gui.builtinViews.entityEditor import BaseValidator, EntityEditor
from gui.builtinViews.implantEditor import BaseImplantEditorView
from gui.utils.clipboard import fromClipboard, toClipboard
from service.implantSet import ImplantSets


pyfalog = Logger(__name__)

_t = wx.GetTranslation
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
                raise ValueError(_t("You must supply a name for the Implant Set!"))
            elif text in [x.name for x in entityEditor.choices]:
                raise ValueError(_t("Implant Set name already in use, please choose another."))

            return True
        except ValueError as e:
            pyfalog.error(e)
            wx.MessageBox("{}".format(e), _t("Error"))
            textCtrl.SetFocus()
            return False


class ImplantSetEntityEditor(EntityEditor):
    def __init__(self, parent):
        EntityEditor.__init__(self, parent, _t("Implant Set"))
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


class ImplantSetEditorView(BaseImplantEditorView):

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

        sIS.addImplants(set_.ID, item.ID)

    def removeImplantFromContext(self, implant):
        sIS = ImplantSets.getInstance()
        set_ = self.Parent.entityEditor.getActiveEntity()

        sIS.removeImplant(set_.ID, implant)


class ImplantSetEditor(AuxiliaryFrame):

    def __init__(self, parent, dataToAdd=None):
        super().__init__(
            parent, id=wx.ID_ANY, title=_t("Implant Set Editor"), resizeable=True,
            size=wx.Size(950, 500) if "wxGTK" in wx.PlatformInfo else wx.Size(850, 420))

        self.block = False
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.entityEditor = ImplantSetEntityEditor(self)
        mainSizer.Add(self.entityEditor, 0, wx.ALL | wx.EXPAND, 2)

        self.sl = wx.StaticLine(self)
        mainSizer.Add(self.sl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.iview = ImplantSetEditorView(self)
        mainSizer.Add(self.iview, 1, wx.ALL | wx.EXPAND, 5)

        self.slfooter = wx.StaticLine(self)
        mainSizer.Add(self.slfooter, 0, wx.EXPAND | wx.TOP, 5)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.stNotice = wx.StaticText(self, wx.ID_ANY, "")
        self.stNotice.Wrap(-1)
        footerSizer.Add(self.stNotice, 1, wx.BOTTOM | wx.TOP | wx.LEFT, 5)

        importExport = ((_t("Import implant sets from clipboard"), wx.ART_FILE_OPEN, "Import"),
                        (_t("Export implant sets to clipboard"), wx.ART_FILE_SAVE_AS, "Export"))

        for tooltip, art, attr in importExport:
            bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON)
            btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)

            btn.SetMinSize(btn.GetSize())
            btn.SetMaxSize(btn.GetSize())

            btn.Layout()
            setattr(self, attr, btn)
            btn.Enable(True)
            btn.SetToolTip(tooltip)
            footerSizer.Add(btn, 0)

        mainSizer.Add(footerSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        if dataToAdd:
            name, implants = dataToAdd
            newSet = self.entityEditor.DoNew(name)
            ImplantSets.getInstance().addImplants(newSet.ID, *[i.item.ID for i in implants])
            self.entityEditor.refreshEntityList(newSet)
            wx.PostEvent(self.entityEditor.entityChoices, wx.CommandEvent(wx.wxEVT_COMMAND_CHOICE_SELECTED))
        elif not self.entityEditor.checkEntitiesExist():
            self.Close()
            return

        self.Bind(wx.EVT_CHOICE, self.entityChanged)
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)

        self.Import.Bind(wx.EVT_BUTTON, self.importPatterns)
        self.Export.Bind(wx.EVT_BUTTON, self.exportPatterns)

        self.SetMinSize(self.GetSize())
        self.CenterOnParent()

    def entityChanged(self, event):
        if not self.entityEditor.checkEntitiesExist():
            self.Close()
            return

    def kbEvent(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE and event.GetModifiers() == wx.MOD_NONE:
            self.Close()
            return
        event.Skip()

    def __del__(self):
        pass

    def importPatterns(self, event):
        """Event fired when import from clipboard button is clicked"""

        text = fromClipboard()
        if text:
            sIS = ImplantSets.getInstance()
            try:
                sIS.importSets(text)
                self.stNotice.SetLabel(_t("Patterns successfully imported from clipboard"))
            except ImportError as e:
                pyfalog.error(e)
                self.stNotice.SetLabel(str(e))
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                pyfalog.error(e)
                self.stNotice.SetLabel(_t("Could not import from clipboard: unknown errors"))
            finally:
                self.entityEditor.refreshEntityList()
        else:
            self.stNotice.SetLabel(_t("Could not import from clipboard"))

    def exportPatterns(self, event):
        """Event fired when export to clipboard button is clicked"""

        sIS = ImplantSets.getInstance()
        toClipboard(sIS.exportSets())
        self.stNotice.SetLabel(_t("Sets exported to clipboard"))
