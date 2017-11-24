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
from gui.statsView import StatsView
from gui.bitmap_loader import BitmapLoader
from gui.pyfa_gauge import PyGauge
import gui.mainFrame
from gui.chrome_tabs import EVT_NOTEBOOK_PAGE_CHANGED
from gui.utils import fonts

from eos.saveddata.module import Hardpoint

from gui.utils.numberFormatter import formatAmount


class ResourcesViewFull(StatsView):
    name = "resourcesViewFull"
    contexts = ["drone", "fighter", "cargo"]

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.mainFrame.additionsPane.notebook.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self.pageChanged)

    def pageChanged(self, event):
        page = self.mainFrame.additionsPane.getName(event.GetSelection())
        if page == "Cargo":
            self.toggleContext("cargo")
        elif page == "Fighters":
            self.toggleContext("fighter")
        else:
            self.toggleContext("drone")

    def toggleContext(self, context):
        # Apparently you cannot .Hide(True) on a Window, otherwise I would just .Hide(context !== x).
        # This is a gimpy way to toggle this shit
        for x in self.contexts:
            bitmap = getattr(self, "bitmapFull{}Bay".format(x.capitalize()))
            base = getattr(self, "baseFull{}Bay".format(x.capitalize()))

            if context == x:
                bitmap.Show()
                base.Show(True)
            else:
                bitmap.Hide()
                base.Hide(True)

        fighter_sizer = getattr(self, "boxSizerFighter")
        drone_sizer = getattr(self, "boxSizerDrones")

        if context != "fighter":
            fighter_sizer.ShowItems(False)
            drone_sizer.ShowItems(True)
        else:
            fighter_sizer.ShowItems(True)
            drone_sizer.ShowItems(False)

        self.panel.Layout()
        self.headerPanel.Layout()

    def getHeaderText(self, fit):
        return "Resources"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    def populatePanel(self, contentPanel, headerPanel):

        contentSizer = contentPanel.GetSizer()
        root = wx.BoxSizer(wx.VERTICAL)
        contentSizer.Add(root, 0, wx.EXPAND, 0)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        root.Add(sizer, 0, wx.EXPAND)
        root.Add(wx.StaticLine(contentPanel, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)

        sizerResources = wx.BoxSizer(wx.HORIZONTAL)
        root.Add(sizerResources, 1, wx.EXPAND, 0)

        parent = self.panel = contentPanel
        self.headerPanel = headerPanel
        panel = "full"

        base = sizerResources
        sizer.AddStretchSpacer()
        # Turrets & launcher hardslots display
        tooltipText = {"turret": "Turret hardpoints", "launcher": "Launcher hardpoints", "drones": "Drones active",
                       "fighter": "Fighter squadrons active", "calibration": "Calibration"}
        for type_ in ("turret", "launcher", "drones", "fighter", "calibration"):
            box = wx.BoxSizer(wx.HORIZONTAL)

            bitmap = BitmapLoader.getStaticBitmap("%s_big" % type_, parent, "gui")
            tooltip = wx.ToolTip(tooltipText[type_])
            bitmap.SetToolTip(tooltip)

            box.Add(bitmap, 0, wx.ALIGN_CENTER)

            sizer.Add(box, 0, wx.ALIGN_CENTER)

            suffix = {'turret': 'Hardpoints', 'launcher': 'Hardpoints', 'drones': 'Active', 'fighter': 'Tubes',
                      'calibration': 'Points'}
            lbl = wx.StaticText(parent, wx.ID_ANY, "0")
            setattr(self, "label%sUsed%s%s" % (panel.capitalize(), type_.capitalize(), suffix[type_].capitalize()), lbl)
            box.Add(lbl, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

            box.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0")
            setattr(self, "label%sTotal%s%s" % (panel.capitalize(), type_.capitalize(), suffix[type_].capitalize()),
                    lbl)
            box.Add(lbl, 0, wx.ALIGN_CENTER)
            setattr(self, "boxSizer{}".format(type_.capitalize()), box)

            # Hack - We add a spacer after each thing, but we are always hiding something. The spacer is stil there.
            # This way, we only have one space after the drones/fighters
            if type_ != "drones":
                sizer.AddStretchSpacer()

        gauge_font = wx.Font(fonts.NORMAL, wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        # PG, Cpu & drone stuff
        tooltipText = {"cpu": "CPU", "pg": "PowerGrid", "droneBay": "Drone bay", "fighterBay": "Fighter bay",
                       "droneBandwidth": "Drone bandwidth", "cargoBay": "Cargo bay"}
        for i, group in enumerate((("cpu", "pg"), ("cargoBay", "droneBay", "fighterBay", "droneBandwidth"))):
            main = wx.BoxSizer(wx.VERTICAL)
            base.Add(main, 1, wx.ALIGN_CENTER)

            for type_ in group:
                capitalizedType = type_[0].capitalize() + type_[1:]
                bitmap = BitmapLoader.getStaticBitmap(type_ + "_big", parent, "gui")
                tooltip = wx.ToolTip(tooltipText[type_])
                bitmap.SetToolTip(tooltip)

                stats = wx.BoxSizer(wx.VERTICAL)
                absolute = wx.BoxSizer(wx.HORIZONTAL)
                stats.Add(absolute, 0, wx.EXPAND)

                b = wx.BoxSizer(wx.HORIZONTAL)
                main.Add(b, 1, wx.ALIGN_CENTER)

                b.Add(bitmap, 0, wx.ALIGN_BOTTOM)

                b.Add(stats, 1, wx.EXPAND)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sUsed%s" % (panel.capitalize(), capitalizedType), lbl)
                absolute.Add(lbl, 0, wx.ALIGN_LEFT | wx.LEFT, 3)

                absolute.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_LEFT)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sTotal%s" % (panel.capitalize(), capitalizedType), lbl)
                absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                units = {"cpu": " tf", "pg": " MW", "droneBandwidth": " mbit/s", "droneBay": " m\u00B3",
                         "fighterBay": " m\u00B3", "cargoBay": " m\u00B3"}
                lbl = wx.StaticText(parent, wx.ID_ANY, "%s" % units[type_])
                absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                # Gauges modif. - Darriele

                gauge = PyGauge(parent, gauge_font, 1)
                gauge.SetValueRange(0, 0)
                gauge.SetMinSize((self.getTextExtentW("1.999M/1.99M MW"), 23))
                gauge.SetFractionDigits(2)

                setattr(self, "gauge%s%s" % (panel.capitalize(), capitalizedType), gauge)
                stats.Add(gauge, 0, wx.ALIGN_CENTER)

                setattr(self, "base%s%s" % (panel.capitalize(), capitalizedType), b)
                setattr(self, "bitmap%s%s" % (panel.capitalize(), capitalizedType), bitmap)

        self.toggleContext("drone")

    def refreshPanel(self, fit):
        # If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = (
            ("label%sUsedTurretHardpoints", lambda: fit.getHardpointsUsed(Hardpoint.TURRET), 0, 0, 0),
            ("label%sTotalTurretHardpoints", lambda: fit.ship.getModifiedItemAttr('turretSlotsLeft'), 0, 0, 0),
            ("label%sUsedLauncherHardpoints", lambda: fit.getHardpointsUsed(Hardpoint.MISSILE), 0, 0, 0),
            ("label%sTotalLauncherHardpoints", lambda: fit.ship.getModifiedItemAttr('launcherSlotsLeft'), 0, 0, 0),
            ("label%sUsedDronesActive", lambda: fit.activeDrones, 0, 0, 0),
            ("label%sTotalDronesActive", lambda: fit.extraAttributes["maxActiveDrones"], 0, 0, 0),
            ("label%sUsedFighterTubes", lambda: fit.fighterTubesUsed, 3, 0, 9),
            ("label%sTotalFighterTubes", lambda: fit.ship.getModifiedItemAttr("fighterTubes"), 3, 0, 9),
            ("label%sUsedCalibrationPoints", lambda: fit.calibrationUsed, 0, 0, 0),
            ("label%sTotalCalibrationPoints", lambda: fit.ship.getModifiedItemAttr('upgradeCapacity'), 0, 0, 0),
            ("label%sUsedPg", lambda: fit.pgUsed, 4, 0, 9),
            ("label%sUsedCpu", lambda: fit.cpuUsed, 4, 0, 9),
            ("label%sTotalPg", lambda: fit.ship.getModifiedItemAttr("powerOutput"), 4, 0, 9),
            ("label%sTotalCpu", lambda: fit.ship.getModifiedItemAttr("cpuOutput"), 4, 0, 9),
            ("label%sUsedDroneBay", lambda: fit.droneBayUsed, 3, 0, 9),
            ("label%sUsedFighterBay", lambda: fit.fighterBayUsed, 3, 0, 9),
            ("label%sUsedDroneBandwidth", lambda: fit.droneBandwidthUsed, 3, 0, 9),
            ("label%sTotalDroneBay", lambda: fit.ship.getModifiedItemAttr("droneCapacity"), 3, 0, 9),
            ("label%sTotalDroneBandwidth", lambda: fit.ship.getModifiedItemAttr("droneBandwidth"), 3, 0, 9),
            ("label%sTotalFighterBay", lambda: fit.ship.getModifiedItemAttr("fighterCapacity"), 3, 0, 9),
            ("label%sUsedCargoBay", lambda: fit.cargoBayUsed, 3, 0, 9),
            ("label%sTotalCargoBay", lambda: fit.ship.getModifiedItemAttr("capacity"), 3, 0, 9),
        )
        panel = "Full"

        usedTurretHardpoints = 0
        labelUTH = ""
        totalTurretHardpoints = 0
        labelTTH = ""
        usedLauncherHardpoints = 0
        labelULH = ""
        totalLauncherHardPoints = 0
        labelTLH = ""
        usedDronesActive = 0
        labelUDA = ""
        totalDronesActive = 0
        labelTDA = ""
        usedFighterTubes = 0
        labelUFT = ""
        totalFighterTubes = 0
        labelTFT = ""
        usedCalibrationPoints = 0
        labelUCP = ""
        totalCalibrationPoints = 0
        labelTCP = ""

        for labelName, value, prec, lowest, highest in stats:
            label = getattr(self, labelName % panel)
            value = value() if fit is not None else 0
            value = value if value is not None else 0

            if labelName % panel == "label%sUsedTurretHardpoints" % panel:
                usedTurretHardpoints = value
                labelUTH = label
            elif labelName % panel == "label%sTotalTurretHardpoints" % panel:
                totalTurretHardpoints = value
                labelTTH = label
            elif labelName % panel == "label%sUsedLauncherHardpoints" % panel:
                usedLauncherHardpoints = value
                labelULH = label
            elif labelName % panel == "label%sTotalLauncherHardpoints" % panel:
                totalLauncherHardPoints = value
                labelTLH = label
            elif labelName % panel == "label%sUsedDronesActive" % panel:
                usedDronesActive = value
                labelUDA = label
            elif labelName % panel == "label%sTotalDronesActive" % panel:
                totalDronesActive = value
                labelTDA = label
            elif labelName % panel == "label%sUsedFighterTubes" % panel:
                usedFighterTubes = value
                labelUFT = label
            elif labelName % panel == "label%sTotalFighterTubes" % panel:
                totalFighterTubes = value
                labelTFT = label
            elif labelName % panel == "label%sUsedCalibrationPoints" % panel:
                usedCalibrationPoints = value
                labelUCP = label
            elif labelName % panel == "label%sTotalCalibrationPoints" % panel:
                totalCalibrationPoints = value
                labelTCP = label

            if isinstance(value, str):
                label.SetLabel(value)
                label.SetToolTip(wx.ToolTip(value))
            else:
                label.SetLabel(formatAmount(value, prec, lowest, highest))
                label.SetToolTip(wx.ToolTip("%.1f" % value))

        colorWarn = wx.Colour(204, 51, 51)
        colorNormal = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        if usedTurretHardpoints > totalTurretHardpoints:
            colorT = colorWarn
        else:
            colorT = colorNormal
        if usedLauncherHardpoints > totalLauncherHardPoints:
            colorL = colorWarn
        else:
            colorL = colorNormal
        if usedDronesActive > totalDronesActive:
            colorD = colorWarn
        else:
            colorD = colorNormal
        if usedFighterTubes > totalFighterTubes:
            colorF = colorWarn
        else:
            colorF = colorNormal
        if usedCalibrationPoints > totalCalibrationPoints:
            colorC = colorWarn
        else:
            colorC = colorNormal

        labelUTH.SetForegroundColour(colorT)
        labelTTH.SetForegroundColour(colorT)
        labelULH.SetForegroundColour(colorL)
        labelTLH.SetForegroundColour(colorL)
        labelUDA.SetForegroundColour(colorD)
        labelTDA.SetForegroundColour(colorD)
        labelUFT.SetForegroundColour(colorF)
        labelTFT.SetForegroundColour(colorF)
        labelUCP.SetForegroundColour(colorC)
        labelTCP.SetForegroundColour(colorC)

        if fit is not None:
            resMax = (
                lambda: fit.ship.getModifiedItemAttr("cpuOutput"),
                lambda: fit.ship.getModifiedItemAttr("powerOutput"),
                lambda: fit.ship.getModifiedItemAttr("droneCapacity"),
                lambda: fit.ship.getModifiedItemAttr("fighterCapacity"),
                lambda: fit.ship.getModifiedItemAttr("droneBandwidth"),
                lambda: fit.ship.getModifiedItemAttr("capacity"),
            )
        else:
            resMax = None

        i = 0
        for resourceType in ("cpu", "pg", "droneBay", "fighterBay", "droneBandwidth", "cargoBay"):
            if fit is not None:
                capitalizedType = resourceType[0].capitalize() + resourceType[1:]

                gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))
                resUsed = getattr(fit, "%sUsed" % resourceType)

                gauge.SetValueRange(resUsed or 0, resMax[i]() or 0)

                i += 1
            else:
                capitalizedType = resourceType[0].capitalize() + resourceType[1:]

                gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))

                gauge.SetValueRange(0, 0)

                i += 1

        self.panel.Layout()
        self.headerPanel.Layout()


ResourcesViewFull.register()
