# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (C) 2017 taleden
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

from math import floor, ceil, sin, cos, atan2, radians, degrees
from gui.graph import Graph
from gui.bitmapLoader import BitmapLoader
from eos.saveddata.fit import Fit
from eos.saveddata.targetResists import TargetResists
from eos.graph.fitDps import FitDpsGraph as FitDps
from eos.graph import Data
import gui.mainFrame
from service.attribute import Attribute
from logbook import Logger

pyfalog = Logger(__name__)


class FitDpsGraphSim(Graph):
    propertyAttributeMap = {"signatureRadius": "signatureRadius",
                            "velocity": "maxVelocity"}

    defaults = FitDps.defaults.copy()

    def __init__(self):
        Graph.__init__(self)
        self.defaults["distance"] = "0-20"
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.fields = {}

    def getName(self):
        return "DPS Simulator"

    def allowTargetFits(self):
        return True

    def allowTargetResists(self):
        return True

    def getControlPanel(self, parent, onFieldChanged):
        self.fields.clear()

        panel = wx.Panel(parent)
        sizer = wx.GridBagSizer(vgap=3, hgap=3)
        panel.SetSizer(sizer)

        # attacker vector
        self.fields["attackerVector"] = vector = VectorPicker(panel, style=wx.NO_BORDER, size=60, offset=90, label="Atk", labelpos=2)
        vector.Bind(VectorPicker.EVT_VECTOR_CHANGED, onFieldChanged)
        sizer.Add(vector, pos=(0, 1), span=(3, 1), flag=wx.SHAPED | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        # target vector
        self.fields["targetVector"] = vector = VectorPicker(panel, style=wx.NO_BORDER, size=60, offset=-90, label="Tgt", labelpos=3)
        vector.Bind(VectorPicker.EVT_VECTOR_CHANGED, onFieldChanged)
        sizer.Add(vector, pos=(0, 2), span=(3, 1), flag=wx.SHAPED | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        """
        # behavior
        icon = wx.StaticBitmap(panel, bitmap=BitmapLoader.getBitmap("22_13", "icons"))
        sizer.Add(icon, pos=(1,7), flag=wx.ALIGN_CENTER)

        label = wx.StaticText(panel, label="Behavior: ")
        sizer.Add(label, pos=(1,8), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        self.fields["behavior"] = choice = wx.Choice(panel)
        choice.Append("Target Vector", "vector")
        choice.Append("Target Profile AI", "ai")
        choice.SetSelection(0)
        choice.Bind(wx.EVT_CHOICE, onFieldChanged)
        sizer.Add(choice, pos=(1,9), flag=wx.EXPAND | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
"""

        # resists
        icon = wx.StaticBitmap(panel, bitmap=BitmapLoader.getBitmap("22_19", "icons"))
        sizer.Add(icon, pos=(1, 3), flag=wx.ALIGN_CENTER)

        label = wx.StaticText(panel, label="Resistances: ")
        sizer.Add(label, pos=(1, 4), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        self.fields["resists"] = choice = wx.Choice(panel)
        choice.Append("Weighted Average", "ehp")
        choice.Append("Shield", "shield")
        choice.Append("Armor", "armor")
        choice.Append("Hull", "hull")
        choice.Append("None", "")
        choice.SetSelection(0)
        choice.Bind(wx.EVT_CHOICE, onFieldChanged)
        sizer.Add(choice, pos=(1, 5), flag=wx.EXPAND | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        # spacers
        sizer.Add(wx.StaticText(panel, label=""), pos=(1, 0), flag=wx.EXPAND)
        sizer.Add(wx.StaticText(panel, label=""), pos=(1, 6), flag=wx.EXPAND)

        sizer.AddGrowableRow(0, proportion=1)
        sizer.AddGrowableRow(2, proportion=1)
        sizer.AddGrowableCol(0, proportion=1)
        sizer.AddGrowableCol(6, proportion=1)
        return panel

    def getVariableLabels(self, values):
        return ("Distance (km)",)

    def prepareData(self, values, fit, tgt):
        data = FitDps.defaults.copy()

        resists = self.fields["resists"].GetClientData(self.fields["resists"].GetSelection())
        if hasattr(tgt, "ship"):
            hp = tgt.hp
            if resists == "ehp":
                for type in ("em", "thermal", "kinetic", "explosive"):
                    ehp = 0
                    for layer, layerHP in hp.iteritems():
                        if layer == "hull":
                            ehp += (layerHP / tgt.ship.getModifiedItemAttr("%sDamageResonance" % type))
                        else:
                            ehp += (layerHP / tgt.ship.getModifiedItemAttr("%s%s%sDamageResonance" % (layer, type[0].upper(), type[1:])))
                    data["%sRes" % (type[:2],)] = 100.0 * (1 - (sum(hp.itervalues()) / ehp))
            elif resists in hp:
                for type in ("em", "thermal", "kinetic", "explosive"):
                    if resists == "hull":
                        res = 1 - tgt.ship.getModifiedItemAttr("%sDamageResonance" % type)
                    else:
                        res = 1 - tgt.ship.getModifiedItemAttr("%s%s%sDamageResonance" % (resists, type[0].upper(), type[1:]))
                    data["%sRes" % (type[:2],)] = 100.0 * res
            data["signatureRadius"] = tgt.ship.getModifiedItemAttr("signatureRadius")
            data["tgtSpeed"] = tgt.ship.getModifiedItemAttr("maxVelocity")
        else:
            if resists != "":
                for type in ("em", "thermal", "kinetic", "explosive"):
                    data["%sRes" % (type[:2],)] = 100.0 * getattr(tgt, "%sAmount" % (type,))
            data["signatureRadius"] = tgt.signatureRadius
            data["tgtSpeed"] = tgt.maxVelocity

        data["distance"] = "0-%d" % (ceil(fit.maxTargetRange / 1000.0),)
        data["atkAngle"], atkThrottle = self.fields["attackerVector"].GetValue()
        data["atkSpeed"] = atkThrottle * fit.ship.getModifiedItemAttr("maxVelocity")
        data["tgtAngle"], tgtThrottle = self.fields["targetVector"].GetValue()
        data["tgtSpeed"] *= tgtThrottle

        return data

    def getPoint(self, values, point, fit=None, tgt=None):
        # yes, we're bypassing the whole superclass pipeline because it's futzy and overcomplicated for fetching just one point
        if fit and tgt and point[0] > 0 and point[0] <= fit.maxTargetRange:
            fitDps = FitDps(fit)
            data = self.prepareData(values, fit, tgt)
            data["distance"] = point[0]
            return fitDps.calcDps(data)
        return None

    def getPoints(self, values, fit=None, tgt=None):
        if not fit:
            return False, "Attacker is required"
        if not tgt:
            return False, "Target is required"

        fitDps = FitDps(fit)
        data = self.prepareData(values, fit, tgt)
        variable = None
        for fieldName, value in data.iteritems():
            d = Data(fieldName, value, 1 if fieldName == "distance" else None)
            if not d.isConstant():
                if variable is None:
                    variable = fieldName
                else:
                    # We can't handle more then one variable atm, OOPS FUCK OUT
                    return False, "Can only handle 1 variable"

            fitDps.setData(d)

        if variable is None:
            return False, "No variable"

        x = []
        y = []
        for point, val in fitDps.getIterator():
            x.append(point[variable])
            y.append(val)

        return x, y


class VectorEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self._angle = 0
        self._length = 0

    def GetValue(self):
        return self._angle, self._length

    def GetAngle(self):
        return self._angle

    def GetLength(self):
        return self._length


class VectorPicker(wx.PyControl):

    UNICODE = "unicode" in wx.PlatformInfo
    myEVT_VECTOR_CHANGED = wx.NewEventType()
    EVT_VECTOR_CHANGED = wx.PyEventBinder(myEVT_VECTOR_CHANGED, 1)

    def __init__(self, *args, **kwargs):
        self._label = str(kwargs.pop("label", ""))
        self._labelpos = int(kwargs.pop("labelpos", 0))
        self._offset = float(kwargs.pop("offset", 0))
        self._size = max(0, float(kwargs.pop("size", 50)))
        self._fontsize = max(1, float(kwargs.pop("fontsize", 8)))
        wx.PyControl.__init__(self, *args, **kwargs)
        self._font = wx.Font(self._fontsize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        self._angle = 0
        self._length = 1
        self._left = False
        self._right = False
        self._tooltip = "Click to set angle and velocity, right-click for increments; mouse wheel for velocity only"
        self.SetToolTip(wx.ToolTip(self._tooltip))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)

    def DoGetBestSize(self):
        return wx.Size(self._size, self._size)

    def AcceptsFocusFromKeyboard(self):
        return False

    def GetValue(self):
        return self._angle, self._length

    def GetAngle(self):
        return self._angle

    def GetLength(self):
        return self._length

    def SetValue(self, angle=None, length=None):
        if angle is not None:
            self._angle = min(max(angle, -180), 180)
        if length is not None:
            self._length = min(max(length, 0), 1)
        self.Refresh()

    def SetAngle(self, angle):
        self.SetValue(angle, None)

    def SetLength(self, length):
        self.SetValue(None, length)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def Draw(self, dc):
        width, height = self.GetClientSize()
        if not width or not height:
            return

        dc.SetBackground(wx.Brush(self.GetBackgroundColour(), wx.SOLID))
        dc.Clear()
        dc.SetTextForeground(wx.Colour(0))
        dc.SetFont(self._font)

        radius = min(width, height) / 2 - 2
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.DrawCircle(radius + 2, radius + 2, radius)
        a = radians(self._angle + self._offset)
        x = sin(a) * radius
        y = cos(a) * radius
        dc.DrawLine(radius + 2, radius + 2, radius + 2 + x * self._length, radius + 2 - y * self._length)
        dc.SetBrush(wx.BLACK_BRUSH)
        dc.DrawCircle(radius + 2 + x * self._length, radius + 2 - y * self._length, 2)

        if self._label:
            labelText = self._label
            labelTextW, labelTextH = dc.GetTextExtent(labelText)
            labelTextX = (radius * 2 + 4 - labelTextW) if (self._labelpos & 1) else 0
            labelTextY = (radius * 2 + 4 - labelTextH) if (self._labelpos & 2) else 0
            dc.DrawText(labelText, labelTextX, labelTextY)

        lengthText = "%d%%" % (100 * self._length,)
        lengthTextW, lengthTextH = dc.GetTextExtent(lengthText)
        lengthTextX = radius + 2 + x / 2 - y / 3 - lengthTextW / 2
        lengthTextY = radius + 2 - y / 2 - x / 3 - lengthTextH / 2
        dc.DrawText(lengthText, lengthTextX, lengthTextY)

        angleText = (u"%d\u00B0" if self.UNICODE else "%d") % (self._angle,)
        angleTextW, angleTextH = dc.GetTextExtent(angleText)
        angleTextX = radius + 2 - x / 2 - angleTextW / 2
        angleTextY = radius + 2 + y / 2 - angleTextH / 2
        if not self.UNICODE:
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.DrawCircle(angleTextX + angleTextW + 1, angleTextY + 1, 1.5)
        dc.DrawText(angleText, angleTextX, angleTextY)

    def OnEraseBackground(self, event):
        pass

    def OnLeftDown(self, event):
        self._left = True
        self.SetToolTip(None)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnLeftUp)
        if not self._right:
            self.Bind(wx.EVT_MOTION, self.OnMotion)
        if not self.HasCapture():
            self.CaptureMouse()
        self.HandleMouseEvent(event)

    def OnRightDown(self, event):
        self._right = True
        self.SetToolTip(None)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnRightUp)
        if not self._left:
            self.Bind(wx.EVT_MOTION, self.OnMotion)
        if not self.HasCapture():
            self.CaptureMouse()
        self.HandleMouseEvent(event)

    def OnLeftUp(self, event):
        self.HandleMouseEvent(event)
        self.Unbind(wx.EVT_LEFT_UP, handler=self.OnLeftUp)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST, handler=self.OnLeftUp)
        self._left = False
        if not self._right:
            self.Unbind(wx.EVT_MOTION, handler=self.OnMotion)
            self.SendChangeEvent()
            self.SetToolTip(wx.ToolTip(self._tooltip))
            if self.HasCapture():
                self.ReleaseMouse()

    def OnRightUp(self, event):
        self.HandleMouseEvent(event)
        self.Unbind(wx.EVT_RIGHT_UP, handler=self.OnRightUp)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST, handler=self.OnRightUp)
        self._right = False
        if not self._left:
            self.Unbind(wx.EVT_MOTION, handler=self.OnMotion)
            self.SendChangeEvent()
            self.SetToolTip(wx.ToolTip(self._tooltip))
            if self.HasCapture():
                self.ReleaseMouse()

    def OnMotion(self, event):
        self.HandleMouseEvent(event)
        event.Skip()

    def OnWheel(self, event):
        amount = 0.1 * event.GetWheelRotation() / event.GetWheelDelta()
        self._length = min(max(self._length + amount, 0.0), 1.0)
        self.Refresh()
        self.SendChangeEvent()

    def HandleMouseEvent(self, event):
        width, height = self.GetClientSize()
        if width and height:
            center = min(width, height) / 2
            x, y = event.GetPositionTuple()
            x = x - center
            y = center - y
            angle = self._angle
            length = min((x * x + y * y) ** 0.5 / (center - 2), 1.0)
            if length < 0.01:
                length = 0
            else:
                angle = ((degrees(atan2(x, y)) - self._offset + 180) % 360) - 180
            if (self._right and not self._left) or event.ShiftDown():
                angle = round(angle / 15.0) * 15.0
                # floor() for length to make it easier to hit 0%, can still hit 100% outside the circle
                length = floor(length / 0.05) * 0.05
            if (angle != self._angle) or (length != self._length):
                self._angle = angle
                self._length = length
                self.Refresh()
                if self._right and not self._left:
                    self.SendChangeEvent()

    def SendChangeEvent(self):
        changeEvent = wx.CommandEvent(self.myEVT_VECTOR_CHANGED, self.GetId())
        changeEvent._object = self
        changeEvent._angle = self._angle
        changeEvent._length = self._length
        self.GetEventHandler().ProcessEvent(changeEvent)


FitDpsGraphSim.register()
