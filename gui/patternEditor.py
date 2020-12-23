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
from gui.bitmap_loader import BitmapLoader
from gui.builtinViews.entityEditor import BaseValidator, EntityEditor
from gui.utils.clipboard import fromClipboard, toClipboard
from gui.utils.inputs import FloatBox
from service.damagePattern import DamagePattern, ImportError
from service.fit import Fit


pyfalog = Logger(__name__)

_t = wx.GetTranslation

class DmgPatternNameValidator(BaseValidator):
    def __init__(self):
        BaseValidator.__init__(self)

    def Clone(self):
        return DmgPatternNameValidator()

    def Validate(self, win):
        entityEditor = win.parent
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()

        try:
            if len(text) == 0:
                raise ValueError(_t("You must supply a name for your Damage Profile!"))
            elif text in [x.rawName for x in entityEditor.choices]:
                raise ValueError(_t("Damage Profile name already in use, please choose another."))

            return True
        except ValueError as e:
            pyfalog.error(e)
            wx.MessageBox("{}".format(e), _t("Error"))
            textCtrl.SetFocus()
            return False


class DmgPatternEntityEditor(EntityEditor):
    def __init__(self, parent):
        EntityEditor.__init__(self, parent, _t("Damage Profile"))
        self.SetEditorValidator(DmgPatternNameValidator)

    def getEntitiesFromContext(self):
        sDP = DamagePattern.getInstance()
        choices = sorted(sDP.getUserDamagePatternList(), key=lambda p: p.rawName)
        choices = [c for c in choices if c.rawName != "Selected Ammo"]
        return choices

    def DoNew(self, name):
        sDP = DamagePattern.getInstance()
        return sDP.newPattern(name)

    def DoRename(self, entity, name):
        sDP = DamagePattern.getInstance()
        sDP.renamePattern(entity, name)

    def DoCopy(self, entity, name):
        sDP = DamagePattern.getInstance()
        copy = sDP.copyPattern(entity)
        sDP.renamePattern(copy, name)
        return copy

    def DoDelete(self, entity):
        sDP = DamagePattern.getInstance()
        sDP.deletePattern(entity)


class DmgPatternEditor(AuxiliaryFrame):

    DAMAGE_TYPES = ("em", "thermal", "kinetic", "explosive")

    def __init__(self, parent):
        super().__init__(
            parent, id=wx.ID_ANY, title=_t("Damage Pattern Editor"), resizeable=True,
            # Dropdown list widget is scaled to its longest content line on GTK, adapt to that
            size=wx.Size(500, 240) if "wxGTK" in wx.PlatformInfo else wx.Size(400, 240))

        self.block = False
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.entityEditor = DmgPatternEntityEditor(self)
        mainSizer.Add(self.entityEditor, 0, wx.ALL | wx.EXPAND, 2)

        self.sl = wx.StaticLine(self)
        mainSizer.Add(self.sl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        contentSizer = wx.BoxSizer(wx.VERTICAL)
        self.embitmap = BitmapLoader.getBitmap("em_big", "gui")
        self.thermbitmap = BitmapLoader.getBitmap("thermal_big", "gui")
        self.kinbitmap = BitmapLoader.getBitmap("kinetic_big", "gui")
        self.expbitmap = BitmapLoader.getBitmap("explosive_big", "gui")

        dmgeditSizer = wx.FlexGridSizer(2, 6, 0, 2)
        dmgeditSizer.AddGrowableCol(0)
        dmgeditSizer.AddGrowableCol(5)
        dmgeditSizer.SetFlexibleDirection(wx.BOTH)
        dmgeditSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        width = -1
        defSize = wx.Size(width, -1)

        for i, type_ in enumerate(self.DAMAGE_TYPES):
            bmp = wx.StaticBitmap(self, wx.ID_ANY, BitmapLoader.getBitmap("%s_big" % type_, "gui"))
            if i % 2:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT
                border = 20
            else:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
                border = 5

            # set text edit
            editBox = FloatBox(parent=self, id=wx.ID_ANY, value=0, pos=wx.DefaultPosition, size=defSize)
            percLabel = wx.StaticText(self, wx.ID_ANY, "0%")
            setattr(self, "%sEdit" % type_, editBox)
            setattr(self, "%sPerc" % type_, percLabel)

            dmgeditSizer.Add(bmp, 0, style, border)
            dmgeditSizer.Add(editBox, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)
            dmgeditSizer.Add(percLabel, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

            editBox.Bind(wx.EVT_TEXT, self.OnFieldChanged)

        contentSizer.Add(dmgeditSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.slfooter = wx.StaticLine(self)
        contentSizer.Add(self.slfooter, 0, wx.EXPAND | wx.TOP, 5)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        perSizer = wx.BoxSizer(wx.VERTICAL)

        self.stNotice = wx.StaticText(self, wx.ID_ANY, "")
        self.stNotice.Wrap(-1)
        perSizer.Add(self.stNotice, 0, wx.BOTTOM | wx.TOP | wx.LEFT, 5)

        footerSizer.Add(perSizer, 1, wx.ALIGN_CENTER_VERTICAL, 5)

        self.totSizer = wx.BoxSizer(wx.VERTICAL)

        contentSizer.Add(footerSizer, 0, wx.EXPAND, 5)

        mainSizer.Add(contentSizer, 1, wx.EXPAND, 0)

        self.SetSizer(mainSizer)

        importExport = ((_t("Import patterns from clipboard"), wx.ART_FILE_OPEN, "import"),
                        (_t("Export patterns to clipboard"), wx.ART_FILE_SAVE_AS, "export"))

        for tooltip, art, attr in importExport:
            bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON)
            btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)

            btn.SetMinSize(btn.GetSize())
            btn.SetMaxSize(btn.GetSize())

            btn.Layout()
            setattr(self, "{}Btn".format(attr), btn)
            btn.Enable(True)
            btn.SetToolTip(tooltip)
            footerSizer.Add(btn, 0)
            btn.Bind(wx.EVT_BUTTON, getattr(self, "{}Patterns".format(attr)))

        if not self.entityEditor.checkEntitiesExist():
            self.Close()
            return

        self.Layout()
        bsize = self.GetBestSize()
        self.SetSize((-1, bsize.height))
        self.SetMinSize(self.GetSize())
        self.CenterOnParent()

        self.Bind(wx.EVT_CHOICE, self.patternChanged)
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)

        self.inputTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnInputTimer, self.inputTimer)

        self.patternChanged()

    def OnFieldChanged(self, event=None):
        if event is not None:
            event.Skip()
        self.inputTimer.Stop()
        self.inputTimer.Start(Fit.getInstance().serviceFittingOptions['marketSearchDelay'], True)

    def OnInputTimer(self, event):
        event.Skip()
        if self.block:
            return
        p = self.entityEditor.getActiveEntity()
        total = sum([(getattr(self, "%sEdit" % attr).GetValueFloat() or 0) for attr in self.DAMAGE_TYPES])
        for type_ in self.DAMAGE_TYPES:
            editBox = getattr(self, "%sEdit" % type_)
            percLabel = getattr(self, "%sPerc" % type_)
            setattr(p, "%sAmount" % type_, editBox.GetValueFloat() or 0)
            percLabel.SetLabel("%.1f%%" % ((editBox.GetValueFloat() or 0) * 100 / total if total > 0 else 0))
        self.totSizer.Layout()
        DamagePattern.getInstance().saveChanges(p)

    def restrict(self):
        for type_ in self.DAMAGE_TYPES:
            editObj = getattr(self, "%sEdit" % type_)
            editObj.Enable(False)
        self.entityEditor.btnRename.Enable(False)
        self.entityEditor.btnDelete.Enable(False)

    def unrestrict(self):
        for type_ in self.DAMAGE_TYPES:
            editObj = getattr(self, "%sEdit" % type_)
            editObj.Enable()
        self.entityEditor.btnRename.Enable()
        self.entityEditor.btnDelete.Enable()

    def patternChanged(self, event=None):

        if not self.entityEditor.checkEntitiesExist():
            self.Close()
            return

        p = self.entityEditor.getActiveEntity()

        if p is None:
            return

        # localization todo: unsure if these names are internal only or also displayed somewhere...
        if p.rawName == "Uniform" or p.rawName == "Selected Ammo":
            self.restrict()
        else:
            self.unrestrict()

        self.block = True

        for field in self.DAMAGE_TYPES:
            edit = getattr(self, "%sEdit" % field)
            amount = int(round(getattr(p, "%sAmount" % field)))
            edit.ChangeValueFloat(amount)

        self.block = False
        self.OnFieldChanged()

    def __del__(self):
        pass

    def importPatterns(self, event):
        text = fromClipboard()
        if text:
            sDP = DamagePattern.getInstance()
            try:
                sDP.importPatterns(text)
                self.stNotice.SetLabel(_t("Patterns successfully imported from clipboard"))
            except ImportError as e:
                pyfalog.error(e)
                self.stNotice.SetLabel(str(e))
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                msg = _t("Could not import from clipboard: unknown errors")
                pyfalog.warning(msg)
                pyfalog.error(e)
                self.stNotice.SetLabel(msg)
            finally:
                self.entityEditor.refreshEntityList()
        else:
            self.stNotice.SetLabel(_t("Could not import from clipboard"))

    def exportPatterns(self, event):
        sDP = DamagePattern.getInstance()
        toClipboard(sDP.exportPatterns())
        self.stNotice.SetLabel(_t("Patterns exported to clipboard"))

    def kbEvent(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE and event.GetModifiers() == wx.MOD_NONE:
            self.Close()
            return
        event.Skip()
