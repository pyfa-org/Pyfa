# =============================================================================
# Copyright (C) 2014 Ryan Holmes
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


import math
from collections import OrderedDict

# noinspection PyPackageRequirements
import wx
from logbook import Logger

import gui.globalEvents as GE
import gui.mainFrame
from gui.auxWindow import AuxiliaryFrame
from gui.bitmap_loader import BitmapLoader
from gui.builtinViews.entityEditor import BaseValidator, EntityEditor
from gui.utils.clipboard import fromClipboard, toClipboard
from gui.utils.inputs import FloatBox, InputValidator, strToFloat
from service.fit import Fit
from service.targetProfile import TargetProfile


pyfalog = Logger(__name__)

_t = wx.GetTranslation

class ResistValidator(InputValidator):

    def _validateWithReason(self, value):
        if not value:
            return True, ''
        value = strToFloat(value)
        if value is None:
            return False, _t('Incorrect formatting (decimals only)')
        if value < 0 or value > 100:
            return False, _t('Incorrect range (must be 0-100)')
        return True, ''


class TargetProfileNameValidator(BaseValidator):

    def __init__(self):
        BaseValidator.__init__(self)

    def Clone(self):
        return TargetProfileNameValidator()

    def Validate(self, win):
        entityEditor = win.parent
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()

        try:
            if len(text) == 0:
                raise ValueError(_t("You must supply a name for your Target Profile!"))
            elif text in [x.rawName for x in entityEditor.choices]:
                raise ValueError(_t("Target Profile name already in use, please choose another."))

            return True
        except ValueError as e:
            pyfalog.error(e)
            wx.MessageBox("{}".format(e), _t("Error"))
            textCtrl.SetFocus()
            return False


class TargetProfileEntityEditor(EntityEditor):

    def __init__(self, parent):
        EntityEditor.__init__(self, parent=parent, entityName=_t("Target Profile"))
        self.SetEditorValidator(TargetProfileNameValidator)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getEntitiesFromContext(self):
        sTR = TargetProfile.getInstance()
        choices = sorted(sTR.getUserTargetProfileList(), key=lambda p: p.rawName)
        return choices

    def DoNew(self, name):
        sTR = TargetProfile.getInstance()
        return sTR.newPattern(name)

    def DoRename(self, entity, name):
        sTR = TargetProfile.getInstance()
        sTR.renamePattern(entity, name)
        wx.PostEvent(self.mainFrame, GE.TargetProfileChanged(profileID=entity.ID))

    def DoCopy(self, entity, name):
        sTR = TargetProfile.getInstance()
        copy = sTR.copyPattern(entity)
        sTR.renamePattern(copy, name)
        return copy

    def DoDelete(self, entity):
        sTR = TargetProfile.getInstance()
        sTR.deletePattern(entity)
        wx.PostEvent(self.mainFrame, GE.TargetProfileRemoved(profileID=entity.ID))


class TargetProfileEditor(AuxiliaryFrame):

    DAMAGE_TYPES = OrderedDict([
        ("em", _t("EM resistance")),
        ("thermal", _t("Thermal resistance")),
        ("kinetic", _t("Kinetic resistance")),
        ("explosive", _t("Explosive resistance"))])
    ATTRIBUTES = OrderedDict([
        ('maxVelocity', (_t('Maximum speed'), 'm/s')),
        ('signatureRadius', (_t('Signature radius\nLeave blank for infinitely big value'), 'm')),
        ('radius', (_t('Radius'), 'm'))])

    def __init__(self, parent):
        super().__init__(
            parent, id=wx.ID_ANY, title=_t("Target Profile Editor"), resizeable=True,
            # Dropdown list widget is scaled to its longest content line on GTK, adapt to that
            size=wx.Size(500, 240) if "wxGTK" in wx.PlatformInfo else wx.Size(350, 240))

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.block = False
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.entityEditor = TargetProfileEntityEditor(parent=self)
        mainSizer.Add(self.entityEditor, 0, wx.ALL | wx.EXPAND, 2)

        self.sl = wx.StaticLine(self)
        mainSizer.Add(self.sl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        contentSizer = wx.BoxSizer(wx.VERTICAL)

        resistEditSizer = wx.FlexGridSizer(2, 6, 0, 2)
        resistEditSizer.AddGrowableCol(0)
        resistEditSizer.AddGrowableCol(5)
        resistEditSizer.SetFlexibleDirection(wx.BOTH)
        resistEditSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        defSize = wx.Size(50, -1)

        for i, type_ in enumerate(self.DAMAGE_TYPES):
            if i % 2:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT
                border = 25
            else:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
                border = 5
            ttText = self.DAMAGE_TYPES[type_]
            bmp = wx.StaticBitmap(self, wx.ID_ANY, BitmapLoader.getBitmap("%s_big" % type_, "gui"))
            bmp.SetToolTip(wx.ToolTip(ttText))
            resistEditSizer.Add(bmp, 0, style, border)
            # set text edit
            editBox = FloatBox(parent=self, id=wx.ID_ANY, value=None, pos=wx.DefaultPosition, size=defSize, validator=ResistValidator())
            editBox.SetToolTip(wx.ToolTip(ttText))
            self.Bind(event=wx.EVT_TEXT, handler=self.OnFieldChanged, source=editBox)
            setattr(self, '{}Edit'.format(type_), editBox)
            resistEditSizer.Add(editBox, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)
            unit = wx.StaticText(self, wx.ID_ANY, "%", wx.DefaultPosition, wx.DefaultSize, 0)
            unit.SetToolTip(wx.ToolTip(ttText))
            resistEditSizer.Add(unit, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)

        contentSizer.Add(resistEditSizer, 0, wx.EXPAND | wx.ALL, 5)

        miscAttrSizer = wx.BoxSizer(wx.HORIZONTAL)
        miscAttrSizer.AddStretchSpacer()

        for attr in self.ATTRIBUTES:
            leftPad = 25 if attr != list(self.ATTRIBUTES)[0] else 0
            ttText, unitText = self.ATTRIBUTES[attr]
            bmp = wx.StaticBitmap(self, wx.ID_ANY, BitmapLoader.getBitmap("%s_big" % attr, "gui"))
            bmp.SetToolTip(wx.ToolTip(ttText))
            miscAttrSizer.Add(bmp, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, leftPad)
            # set text edit
            editBox = FloatBox(parent=self, id=wx.ID_ANY, value=None, pos=wx.DefaultPosition, size=defSize)
            editBox.SetToolTip(wx.ToolTip(ttText))
            self.Bind(event=wx.EVT_TEXT, handler=self.OnFieldChanged, source=editBox)
            setattr(self, '{}Edit'.format(attr), editBox)
            miscAttrSizer.Add(editBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            unit = wx.StaticText(self, wx.ID_ANY, unitText, wx.DefaultPosition, wx.DefaultSize, 0)
            unit.SetToolTip(wx.ToolTip(ttText))
            miscAttrSizer.Add(unit, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)

        miscAttrSizer.AddStretchSpacer()
        contentSizer.Add(miscAttrSizer, 1, wx.EXPAND | wx.ALL, 5)

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

        importExport = ((_t("Import profiles from clipboard"), wx.ART_FILE_OPEN, "import"),
                        (_t("Export profiles to clipboard"), wx.ART_FILE_SAVE_AS, "export"))

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

    @classmethod
    def openOne(cls, parent, selected=None):
        super().openOne(parent)
        if selected is not None:
            cls._instance.selectTargetProfile(selected)

    def OnFieldChanged(self, event=None):
        if event is not None:
            event.Skip()
        self.inputTimer.Stop()
        self.inputTimer.Start(Fit.getInstance().serviceFittingOptions['marketSearchDelay'], True)

    def OnInputTimer(self, event):
        event.Skip()
        if self.block:
            return
        if self.validateFields():
            p = self.entityEditor.getActiveEntity()
            TargetProfile.getInstance().saveChanges(p)
            wx.PostEvent(self.mainFrame, GE.TargetProfileChanged(profileID=p.ID))

    def validateFields(self):
        valid = True
        try:
            p = self.entityEditor.getActiveEntity()

            for type_ in self.DAMAGE_TYPES:
                editBox = getattr(self, "%sEdit" % type_)
                # Raise exception if value is not valid
                if not editBox.isValid():
                    reason = editBox.getInvalidationReason()
                    raise ValueError(reason)

                value = editBox.GetValueFloat() or 0
                setattr(p, "%sAmount" % type_, value / 100)

            for attr in self.ATTRIBUTES:
                editBox = getattr(self, "%sEdit" % attr)
                # Raise exception if value is not valid
                if not editBox.isValid():
                    reason = editBox.getInvalidationReason()
                    raise ValueError(reason)

                value = editBox.GetValueFloat()
                setattr(p, attr, value)

            self.stNotice.SetLabel("")
            self.totSizer.Layout()

        except ValueError as e:
            self.stNotice.SetLabel(e.args[0])
            valid = False
        finally:  # Refresh for color changes to take effect immediately
            self.Refresh()
        return valid

    def patternChanged(self, event=None):
        """Event fired when user selects pattern. Can also be called from script"""

        if not self.entityEditor.checkEntitiesExist():
            self.Close()
            return

        p = self.entityEditor.getActiveEntity()
        if p is None:
            return

        self.block = True
        # Set new values
        for field in self.DAMAGE_TYPES:
            edit = getattr(self, "%sEdit" % field)
            amount = getattr(p, "%sAmount" % field) * 100
            edit.ChangeValueFloat(amount)

        for attr in self.ATTRIBUTES:
            edit = getattr(self, "%sEdit" % attr)
            amount = getattr(p, attr)
            if amount == math.inf:
                edit.ChangeValueFloat(None)
            else:
                edit.ChangeValueFloat(amount)

        self.block = False
        self.validateFields()

    def __del__(self):
        pass

    def importPatterns(self, event):
        """Event fired when import from clipboard button is clicked"""

        text = fromClipboard()
        if text:
            sTR = TargetProfile.getInstance()
            try:
                sTR.importPatterns(text)
                self.stNotice.SetLabel(_t("Profiles successfully imported from clipboard"))
            except ImportError as e:
                pyfalog.error(e)
                self.stNotice.SetLabel(str(e))
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                msg = _t("Could not import from clipboard:")
                pyfalog.warning(msg)
                pyfalog.error(e)
                self.stNotice.SetLabel(msg)
            finally:
                self.entityEditor.refreshEntityList()
        else:
            self.stNotice.SetLabel(_t("Could not import from clipboard"))

    def exportPatterns(self, event):
        """Event fired when export to clipboard button is clicked"""
        sTR = TargetProfile.getInstance()
        toClipboard(sTR.exportPatterns())
        self.stNotice.SetLabel(_t("Profiles exported to clipboard"))

    def kbEvent(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE and event.GetModifiers() == wx.MOD_NONE:
            self.Close()
            return
        event.Skip()

    def processChanges(self):
        changedFitIDs = Fit.getInstance().processTargetProfileChange()
        if changedFitIDs:
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=changedFitIDs))

    def selectTargetProfile(self, profile):
        self.entityEditor.setActiveEntity(profile)
        self.patternChanged()
