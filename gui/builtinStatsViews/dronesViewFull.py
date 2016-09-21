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
from gui.statsView import StatsView
from gui import builtinStatsViews
from gui.bitmapLoader import BitmapLoader
from gui import pygauge as PG
import gui.mainFrame
import gui.chromeTabs

from eos.types import Hardpoint

from gui.utils.numberFormatter import formatAmount

class ResourcesViewFull(StatsView):
    name = "dronesViewFull"
    contexts = ["drones", "fighter", "cargo"]

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        #self.mainFrame.additionsPane.notebook.Bind(gui.chromeTabs.EVT_NOTEBOOK_PAGE_CHANGED, self.pageChanged)

    def getHeaderText(self, fit):
        return "Drones/Fighters"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
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
        sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        #Turrets & launcher hardslots display
        tooltipText = {"Controlrange":"Control Range"}
        suffix = {'Controlrange':'km'}

        typeValues = []
        typeValues.append("Controlrange")
        for type in typeValues:
            box = wx.BoxSizer(wx.HORIZONTAL)

            text = tooltipText[type]
            typeText = wx.StaticText(parent, wx.ID_ANY, "%s : " % (text))
            box.Add(typeText, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

            sizer.Add(box, 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0")
            setattr(self, "label%s%s" % (panel.capitalize(), type.capitalize()), lbl)

            box.Add(lbl, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

            text = suffix[type]
            typeSuffix = wx.StaticText(parent, wx.ID_ANY, "%s" % (text))
            box.Add(typeSuffix, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

            # Hack - We add a spacer after each thing, but we are always hiding something. The spacer is stil there.
            # This way, we only have one space after the drones/fighters
            if type != "drones":
                sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)


        #PG, Cpu & drone stuff
        tooltipText = {"cpu":"CPU", "pg":"PowerGrid", "droneBay":"Drone bay", "fighterBay": "Fighter bay", "droneBandwidth":"Drone bandwidth", "cargoBay":"Cargo bay", "turret":"Turret hardpoints", "launcher":"Launcher hardpoints", "drones":"Drones active", "fighter": "Fighter squadrons active", "calibration":"Calibration"}
        units = {"droneBandwidth": " mbit/s", "droneBay": u" m\u00B3", "fighterBay": u" m\u00B3", "cargoBay": u" m\u00B3", 'drones': ' Active', 'fighter': ' Tubes'}

        for i, group in enumerate((("drones", "droneBandwidth", "droneBay"), ("fighter", "fighterBay"))):
            main = wx.BoxSizer(wx.VERTICAL)
            base.Add(main, 1 , wx.ALIGN_CENTER)

            for type in group:
                capitalizedType = type[0].capitalize() + type[1:]
                bitmap = BitmapLoader.getStaticBitmap(type + "_big", parent, "gui")
                tooltip = wx.ToolTip(tooltipText[type])
                bitmap.SetToolTip(tooltip)

                stats = wx.BoxSizer(wx.VERTICAL)
                absolute =  wx.BoxSizer(wx.HORIZONTAL)
                stats.Add(absolute, 0, wx.EXPAND)

                b = wx.BoxSizer(wx.HORIZONTAL)
                main.Add(b, 1, wx.ALIGN_CENTER)

                b.Add(bitmap, 0, wx.ALIGN_BOTTOM)

                b.Add(stats, 1, wx.EXPAND)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                test = ("label%sUsed%s" % (panel.capitalize(), capitalizedType), lbl)
                setattr(self, "label%sUsed%s" % (panel.capitalize(), capitalizedType), lbl)
                absolute.Add(lbl, 0, wx.ALIGN_LEFT | wx.LEFT, 3)

                absolute.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_LEFT)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sTotal%s" % (panel.capitalize(), capitalizedType), lbl)
                absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                lbl = wx.StaticText(parent, wx.ID_ANY, "%s" % units[type])
                absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                # Gauges modif. - Darriele

                gauge = PG.PyGauge(parent, wx.ID_ANY, 1)
                gauge.SetValueRange(0, 0)
                gauge.SetMinSize((self.getTextExtentW("1.999M/1.99M MW"), 23))
                gauge.SetFractionDigits(2)

                setattr(self, "gauge%s%s" % (panel.capitalize(),capitalizedType), gauge)
                stats.Add(gauge, 0, wx.ALIGN_CENTER)

                setattr(self, "base%s%s" % (panel.capitalize(), capitalizedType), b)
                setattr(self, "bitmap%s%s" % (panel.capitalize(), capitalizedType), bitmap)

        #self.toggleContext("drone")

    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = (("label%sUsedDrones", lambda: fit.activeDrones, 0, 0, 0),
                         ("label%sTotalDrones", lambda: fit.extraAttributes["maxActiveDrones"], 0, 0, 0),
                         ("label%sUsedFighter", lambda: fit.fighterTubesUsed, 3, 0, 9),
                         ("label%sTotalFighter", lambda: fit.ship.getModifiedItemAttr("fighterTubes"), 3, 0, 9),
                         ("label%sUsedDroneBay", lambda: fit.droneBayUsed, 3, 0, 9),
                         ("label%sUsedFighterBay", lambda: fit.fighterBayUsed, 3, 0, 9),
                         ("label%sUsedDroneBandwidth", lambda: fit.droneBandwidthUsed, 3, 0, 9),
                         ("label%sTotalDroneBay", lambda: fit.ship.getModifiedItemAttr("droneCapacity"), 3, 0, 9),
                         ("label%sTotalDroneBandwidth", lambda: fit.ship.getModifiedItemAttr("droneBandwidth"), 3, 0, 9),
                         ("label%sTotalFighterBay", lambda: fit.ship.getModifiedItemAttr("fighterCapacity"), 3, 0, 9),
                         ("label%sControlrange", lambda: fit.extraAttributes["droneControlRange"]/1000, 3, 0, 9))
        panel = "Full"
        usedTurretHardpoints = 0
        totalTurretHardpoints = 0
        usedLauncherHardpoints = 0
        totalLauncherHardPoints = 0

        for labelName, value, prec, lowest, highest in stats:
            label = getattr(self, labelName % panel)
            value = value() if fit is not None else 0
            value = value if value is not None else 0

            if labelName % panel == "label%sUsedDrones" % panel:
                usedDrones = value
                labelUDA = label

            if labelName % panel == "label%sTotalDrones" % panel:
                totalDrones = value
                labelTDA = label

            if labelName % panel == "label%sUsedFighter" % panel:
                usedFighter = value
                labelUFT = label

            if labelName % panel == "label%sTotalFighter" % panel:
                totalFighter = value
                labelTFT = label

            if isinstance(value, basestring):
                label.SetLabel(value)
                label.SetToolTip(wx.ToolTip(value))
            else:
                label.SetLabel(formatAmount(value, prec, lowest, highest))
                label.SetToolTip(wx.ToolTip("%.1f" % value))

        colorWarn = wx.Colour(204, 51, 51)
        colorNormal = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        '''
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
        '''

        '''
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
        '''

        if fit is not None:
            resMax = (lambda: fit.ship.getModifiedItemAttr("droneCapacity"),
                    lambda: fit.ship.getModifiedItemAttr("fighterCapacity"),
                    lambda: fit.ship.getModifiedItemAttr("droneBandwidth"))

        i = 0
        for resourceType in ("droneBay", "fighterBay", "droneBandwidth", "drones", "fighter"):

            try:
                testUsed = "used%s" % resourceType.capitalize()
                resUsed = eval(testUsed)
            except NameError:
                resUsed = None

            try:
                testTotal = "total%s" % resourceType.capitalize()
                resTotal = eval(testTotal)
            except NameError:
                resTotal = None

            if fit is not None:
                capitalizedType = resourceType[0].capitalize() + resourceType[1:]
                gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))
                if resUsed is None:
                    resUsed = getattr(fit,"%sUsed" % resourceType)

                if resTotal is None:
                    resTotal = resMax[i]()

                gauge.SetValueRange(resUsed or 0, resTotal or 0)
                i+=1
            else:
                capitalizedType = resourceType[0].capitalize() + resourceType[1:]
                gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))
                gauge.SetValueRange(0, 0)
                i+=1

        self.panel.Layout()
        self.headerPanel.Layout()

ResourcesViewFull.register()
