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
import gui.fittingView as fv
import gui.mainFrame
import controller
from eos.types import Slot, Hardpoint
from gui import pygauge as PG

class StatsPane(wx.Panel):
    def collapseChanged(self, event):
        collapsed = event.Collapsed
        if collapsed:
            self.pickerSizer.Replace(self.fullPanel, self.miniPanel)
            self.SetMinSize(self.miniSize)
        else:
            self.pickerSizer.Replace(self.miniPanel, self.fullPanel)
            self.SetMinSize(self.fullSize)

        self.fullPanel.Show(not collapsed)
        self.miniPanel.Show(collapsed)
        self.mainFrame.statsSizer.Layout()

    def fitChanged(self, event):
        cFit = controller.Fit.getInstance()
        fit = cFit.getFit(event.fitID)
        statsMiniFull = (("label%sUsedTurretHardpoints", lambda: fit.getHardpointsUsed(Hardpoint.TURRET), 0),
                         ("label%sTotalTurretHardpoints", lambda: fit.ship.getModifiedItemAttr('turretSlotsLeft'), 0),
                         ("label%sUsedLauncherHardpoints", lambda: fit.getHardpointsUsed(Hardpoint.MISSILE), 0),
                         ("label%sTotalLauncherHardpoints", lambda: fit.ship.getModifiedItemAttr('launcherSlotsLeft'), 0),
                         ("label%sUsedCalibrationPoints", lambda: fit.calibrationUsed, 0),
                         ("label%sTotalCalibrationPoints", lambda: fit.ship.getModifiedItemAttr('upgradeCapacity'), 0),
                         ("label%sUsedPg", lambda: fit.pgUsed, 1),
                         ("label%sUsedCpu", lambda: fit.cpuUsed, 1),
                         ("label%sTotalPg", lambda: fit.ship.getModifiedItemAttr("powerOutput"), 1),
                         ("label%sTotalCpu", lambda: fit.ship.getModifiedItemAttr("cpuOutput"), 1),
                         ("label%sVolleyTotal", lambda: fit.weaponVolley, 1),
                         ("label%sDpsTotal", lambda: fit.totalDPS, 1),
                         ("label%sCapacitorCapacity", lambda: fit.ship.getModifiedItemAttr("capacitorCapacity"), 1),
                         ("label%sCapacitorState", lambda: "Stable at " if fit.capState else "Lasts ", 0),
                         ("label%sCapacitorTime", lambda: ("%.1f%%" if fit.capStable else "%ds") % fit.capState, 0),
                         ("label%sCapacitorRecharge", lambda: fit.capRecharge, 1),
                         ("label%sCapacitorDischarge", lambda: fit.capUsed, 1),
                         ("label%sSpeed", lambda: fit.ship.getModifiedItemAttr("maxVelocity"), 1),
                         ("label%sAlignTime", lambda: 0, 1))

        stats = (("labelFullUsedDroneBay", lambda: fit.droneBayUsed, 0),
                     ("labelFullUsedDroneBandwidth", lambda: fit.droneBandwidthUsed, 0),
                     ("labelFullTotalDroneBay", lambda: fit.ship.getModifiedItemAttr("droneCapacity"), 0),
                     ("labelFullTotalDroneBandwidth", lambda: fit.ship.getModifiedItemAttr("droneBandwidth"), 0),
                     ("labelFullDpsWeapon", lambda: fit.weaponDPS, 1),
                     ("labelFullDpsDrone", lambda: fit.droneDPS, 1),
                     ("labelTankSustainedShieldPassive", lambda: fit.calculateShieldRecharge(), 1),
                     ("labelTargets", lambda: fit.maxTargets, 0),
                     ("labelRange", lambda: fit.ship.getModifiedItemAttr('maxTargetRange') / 1000, 1),
                     ("labelScanRes", lambda: fit.ship.getModifiedItemAttr('scanResolution'), 0),
                     ("labelSensorStr", lambda: fit.scanStrength, 0),
                     ("labelFullCargo", lambda: fit.extraAttributes["capacity"], 1),
                     ("labelFullSigRadius", lambda: fit.ship.getModifiedItemAttr("signatureRadius"), 0))

        for panel in ("Mini", "Full"):
            for labelName, value, rounding in statsMiniFull:
                label = getattr(self, labelName % panel)
                value = value() if fit is not None else 0
                value = value if value is not None else 0
                if isinstance(value, basestring):
                    label.SetLabel(value)
                else:
                    label.SetLabel(("%." + str(rounding) + "f") % value)

        for labelName, value, rounding in stats:
            label = getattr(self, labelName)
            label.SetLabel(("%." + str(rounding) + "f") % (value() if fit is not None else 0))

#        resMax = (("cpuTotal", lambda: fit.ship.getModifiedItemAttr("cpuOutput")),
#                    ("pgTotal", lambda: fit.ship.getModifiedItemAttr("powerOutput")),
#                    ("droneBayTotal", lambda: fit.ship.getModifiedItemAttr("droneCapacity")),
#                    ("droneBandwidthTotal", lambda: fit.ship.getModifiedItemAttr("droneBandwidth")))

        if fit is not None:
            resMax = (lambda: fit.ship.getModifiedItemAttr("cpuOutput"),
                    lambda: fit.ship.getModifiedItemAttr("powerOutput"),
                    lambda: fit.ship.getModifiedItemAttr("droneCapacity"),
                    lambda: fit.ship.getModifiedItemAttr("droneBandwidth"),
                    lambda: fit.ship.getModifiedItemAttr("cpuOutput"),
                    lambda: fit.ship.getModifiedItemAttr("powerOutput"))

        for panel in ("Mini","Full"):
            i=0
            for resourceType in ("cpu", "pg", "droneBay", "droneBandwidth"):
                if fit is not None:
                    if i>1 and panel == "Mini": break
                    i+=1
                    capitalizedType = resourceType[0].capitalize() + resourceType[1:]

                    gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))
                    resUsed = getattr(fit,"%sUsed" % resourceType)

                    gauge.SetRange(resMax[i-1]())
                    gauge.SetValue(resUsed)
                else:
                    if i>1 and panel == "Mini": break
                    i+=1
                    capitalizedType = resourceType[0].capitalize() + resourceType[1:]

                    gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))

                    gauge.SetRange(100)
                    gauge.SetValue(0)                    

        for tankType in ("shield", "armor", "hull"):
            for damageType in ("em", "thermal", "kinetic", "explosive"):
                if fit is not None:
                    resonanceType = tankType if tankType != "hull" else ""
                    resonance = "%s%sDamageResonance" % (resonanceType, damageType.capitalize())
                    resonance = resonance[0].lower() + resonance[1:]
                    resonance = (1 - fit.ship.getModifiedItemAttr(resonance)) * 100
                else:
                    resonance = 0

                lbl = getattr(self, "labelResistance%s%s" % (tankType.capitalize(), damageType.capitalize()))
                if self._showNormalGauges == True:
                    lbl.SetLabel("%.2f" % resonance)
                else:
                    lbl.SetValue(resonance)

        ehp = fit.ehp if fit is not None else None
        for tankType in ("shield", "armor", "hull"):
            lbl = getattr(self, "labelResistance%sEhp" % tankType.capitalize())
            if ehp is not None:
                lbl.SetLabel("%.0f" % ehp[tankType])
            else:
                lbl.SetLabel("0")

        damagePattern = fit.damagePattern if fit is not None else None
        for damageType in ("em", "thermal", "kinetic", "explosive"):
            lbl = getattr(self, "labelResistanceDamagepattern%s" % damageType.capitalize())
            if damagePattern:
                lbl.SetLabel("%.2f" % getattr(damagePattern, "%sAmount" % damageType))
            else:
                lbl.SetLabel("0.00")

        for stability in ("reinforced", "sustained"):
            if stability == "reinforced" and fit != None:
                tank = fit.sustainableTank
            elif stability == "sustained" and fit != None:
                tank = fit.extraAttributes
            else:
                tank = None

            for name in ("shield", "armor", "hull"):
                lbl = getattr(self, "labelTank%s%sActive" % (stability.capitalize(), name.capitalize()))
                if tank is not None:
                    lbl.SetLabel("%.1f" % tank["%sRepair" % name])
                else:
                    lbl.SetLabel("0.0")

        self.Layout()
        event.Skip()

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._showNormalGauges = False
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        # Register events
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)

        self.pickerSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.pickerSizer)

        collapsible = wx.CollapsiblePane(self, label="Stats")
        collapsible.Expand()
        collapsible.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChanged)

        self.pickerSizer.Add(collapsible, 0, wx.EXPAND)

        self.fullSize = wx.Size()
        self.fullSize.SetWidth(330)
        self.fullPanel = wx.Panel(self)
        self.SetMinSize(self.fullSize)
        self.pickerSizer.Add(self.fullPanel, 1, wx.EXPAND)

        self.miniSize = wx.Size()
        self.miniSize.SetWidth(120)
        self.miniPanel = wx.Panel(self)
        self.miniPanel.Hide()
        self.miniPanel.SetMinSize(self.miniSize)

        minBase = wx.BoxSizer(wx.VERTICAL)
        self.miniPanel.SetSizer(minBase)

        self.minSizerBase = wx.BoxSizer(wx.VERTICAL)
        minBase.Add(self.minSizerBase, 0, wx.EXPAND | wx.TOP, 15)

        boldFont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldFont.SetWeight(wx.BOLD)

        #Populate the full panel first
        self.sizerBase = wx.BoxSizer(wx.VERTICAL)
        self.fullPanel.SetSizer(self.sizerBase)

        sizerHeaderResources = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderResources, 0, wx.EXPAND | wx.LEFT, 3)

        # Resources stuff
        sizerResources = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerResources, 0, wx.EXPAND | wx.LEFT, 3)


        #Stuff that has to be done for both panels
        for panel in ("full", "mini"):
            parent = getattr(self, "%sPanel" % panel)
            # Resources header
            labelResources = wx.StaticText(parent, wx.ID_ANY, "Resources")
            labelResources.SetFont(boldFont)
            sizer = wx.FlexGridSizer(3, 2)
            for i in xrange(3):
                sizer.AddGrowableCol(i + 1)

            if panel == "mini":
                base = self.minSizerBase
                base.Add(labelResources, 0, wx.ALIGN_CENTER)
                base.Add(sizer, 1, wx.ALIGN_LEFT)
            else:
                base = sizerResources
                base.Add(sizer, 0, wx.ALIGN_CENTER)

                sizerHeaderResources.Add(labelResources, 0, wx.ALIGN_CENTER)
                sizerHeaderResources.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

            #Turrets & launcher hardslots display
            for type in ("turret", "launcher", "calibration"):
                bitmap = bitmapLoader.getStaticBitmap("%s_big" % type, parent, "icons")
                box = wx.BoxSizer(wx.HORIZONTAL)

                sizer.Add(bitmap, 0, wx.ALIGN_LEFT)
                sizer.Add(box, 0, wx.ALIGN_LEFT)

                suffix = "Points" if type == "calibration" else "Hardpoints"
                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sUsed%s%s" % (panel.capitalize(), type.capitalize(), suffix.capitalize()), lbl)
                box.Add(lbl, 0, wx.ALIGN_LEFT)

                box.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_LEFT)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sTotal%s%s" % (panel.capitalize(), type.capitalize(), suffix.capitalize()), lbl)
                box.Add(lbl, 0, wx.ALIGN_LEFT)

            st = wx.VERTICAL if panel == "full" else wx.HORIZONTAL
            base.Add(wx.StaticLine(parent, wx.ID_ANY, style=st), 0, wx.EXPAND | wx.LEFT, 3 if panel == "full" else 0)


            #PG, Cpu & drone stuff
            for i, group in enumerate((("cpu", "pg"), ("droneBay", "droneBandwidth"))):
                main = wx.BoxSizer(wx.VERTICAL)
                base.Add(main, 1 if panel == "full" else 0, wx.ALIGN_CENTER)
                if i == 0 or panel == "full":
                    for type in group:
                        capitalizedType = type[0].capitalize() + type[1:]
                        bitmap = bitmapLoader.getStaticBitmap(type + "_big", parent, "icons")
                        if panel == "mini":
                            main.Add(bitmap, 0, wx.ALIGN_CENTER)

                        stats = wx.BoxSizer(wx.VERTICAL)
                        absolute =  wx.BoxSizer(wx.HORIZONTAL)
                        stats.Add(absolute, 0, wx.ALIGN_RIGHT if panel == "full" else wx.ALIGN_CENTER)

                        if panel == "full":
                            b = wx.BoxSizer(wx.HORIZONTAL)
                            main.Add(b, 1, wx.ALIGN_CENTER)

                            b.Add(bitmap, 0, wx.ALIGN_CENTER)

                            b.Add(stats, 1, wx.EXPAND)
                        else:
                            main.Add(stats, 0, wx.ALIGN_CENTER)

                        lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                        setattr(self, "label%sUsed%s" % (panel.capitalize(), capitalizedType), lbl)
                        absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                        absolute.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_LEFT)

                        lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                        setattr(self, "label%sTotal%s" % (panel.capitalize(), capitalizedType), lbl)
                        absolute.Add(lbl, 0, wx.ALIGN_LEFT)

# Gauges modif. - Darriele
                        if self._showNormalGauges == True:
                            gauge = wx.Gauge(parent, wx.ID_ANY, 100)
                            gauge.SetMinSize((80, 20))
                        else:
                            gauge = PG.PyGauge(parent, wx.ID_ANY, 100)
                            gauge.SetMinSize((80, 16))
                            gauge.SetSkipDigitsFlag(True)

                        setattr(self, "gauge%s%s" % (panel.capitalize(),capitalizedType), gauge)
                        stats.Add(gauge, 0, wx.ALIGN_CENTER)
                if panel == "mini":
                    base.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)

                if i == 0 and panel == "full":
                    base.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.VERTICAL), 0, wx.EXPAND)

        # Resistances
        sizerHeaderResistances = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderResistances, 0, wx.EXPAND | wx.LEFT, 3)

        # Header & EHP
        labelResistances = wx.StaticText(self.fullPanel, wx.ID_ANY, "Resistances")
        labelResistances.SetFont(boldFont)
        sizerHeaderResistances.Add(labelResistances, 0, wx.ALIGN_CENTER)

        sizerHeaderResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, " (Effective HP: "), 0, wx.ALIGN_CENTER)

        self.labelEhp = wx.StaticText(self.fullPanel, wx.ID_ANY, "0")
        sizerHeaderResistances.Add(self.labelEhp, 0, wx.ALIGN_CENTER)

        sizerHeaderResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, ")"), 0, wx.ALIGN_CENTER)
        sizerHeaderResistances.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

        # Display table
        sizerResistances = wx.FlexGridSizer(4, 6)
        for i in xrange(5):
            sizerResistances.AddGrowableCol(i + 1)

        self.sizerBase.Add(sizerResistances, 0, wx.EXPAND | wx.LEFT, 3)

        # Add an empty label, then the rest.
        sizerResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY))

        for damageType in ("em", "thermal", "kinetic", "explosive"):
            sizerResistances.Add(bitmapLoader.getStaticBitmap("%s_big" % damageType, self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)

        sizerResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "EHP"), 0, wx.ALIGN_CENTER)

        gaugeColours=( ((38,133,198),(52,86,98)), ((198,38,38),(83,65,67)), ((163,163,163),(74,90,93)), ((198,133,38),(81,83,67)) )

        for tankType in ("damagePattern", "shield", "armor", "hull"):
            sizerResistances.Add(bitmapLoader.getStaticBitmap("%s_big" % tankType, self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)
            currGColour=0

            for damageType in ("em", "thermal", "kinetic", "explosive"):
                box = wx.BoxSizer(wx.HORIZONTAL)
                sizerResistances.Add(box, 1, wx.ALIGN_CENTER)

#Fancy gauges addon

                pgColour= gaugeColours[currGColour]
                fc = pgColour[0]
                bc = pgColour[1]
                currGColour+=1
                if self._showNormalGauges == True:
                    lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.00")
                else:
                    lbl = PG.PyGauge(self.fullPanel, wx.ID_ANY, 100)
                    lbl.SetMinSize((48, 16))
                    lbl.SetBackgroundColour(wx.Colour(bc[0],bc[1],bc[2]))
                    lbl.SetBarColour(wx.Colour(fc[0],fc[1],fc[2]))
                    lbl.SetBarGradient()
                    lbl.SetSkipDigitsFlag(False)

                setattr(self, "labelResistance%s%s" % (tankType.capitalize(), damageType.capitalize()), lbl)
                box.Add(lbl, 0, wx.ALIGN_CENTER)

                if self._showNormalGauges == True:
                    box.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "%"), 0, wx.ALIGN_CENTER)


            lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0" if tankType != "damagePattern" else "")

            setattr(self, "labelResistance%sEhp" % tankType.capitalize(), lbl)
            sizerResistances.Add(lbl, 0, wx.ALIGN_CENTER)


        # Resistances
        sizerHeaderRechargeRates = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderRechargeRates, 0, wx.EXPAND | wx.LEFT, 3)

        labelRecharge = wx.StaticText(self.fullPanel, wx.ID_ANY, "Recharge Rates")
        labelRecharge.SetFont(boldFont)

        sizerHeaderRechargeRates.Add(labelRecharge, 0, wx.ALIGN_CENTER)
        sizerHeaderRechargeRates.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

        sizerTankStats = wx.FlexGridSizer(3, 5)
        for i in xrange(4):
            sizerTankStats.AddGrowableCol(i + 1)

        self.sizerBase.Add(sizerTankStats, 0, wx.EXPAND | wx.LEFT, 3)

        #Add an empty label first for correct alignment.
        sizerTankStats.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, ""), 0)
        for tankType in ("shieldPassive", "shieldActive", "armorActive", "hullActive"):
            sizerTankStats.Add(bitmapLoader.getStaticBitmap("%s_big" % tankType, self.fullPanel, "icons"), 1, wx.ALIGN_CENTER)

        for stability in ("reinforced", "sustained"):
                sizerTankStats.Add(bitmapLoader.getStaticBitmap("regen%s_big" % stability.capitalize(), self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)
                for tankType in ("shieldPassive", "shieldActive", "armorActive", "hullActive"):
                    if stability == "reinforced" and tankType == "shieldPassive":
                        sizerTankStats.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, ""))
                        continue

                    tankTypeCap = tankType[0].capitalize() + tankType[1:]
                    lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.0")
                    setattr(self, "labelTank%s%s" % (stability.capitalize(), tankTypeCap), lbl)

                    box = wx.BoxSizer(wx.HORIZONTAL)
                    box.Add(lbl, 1, wx.ALIGN_CENTER)
                    box.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, " HP/s"), 0, wx.ALIGN_CENTER)

                    sizerTankStats.Add(box, 1, wx.ALIGN_CENTER)


        #Mini tank display
        labelTank = wx.StaticText(parent, wx.ID_ANY, "Tank")
        labelTank.SetFont(boldFont)
        self.minSizerBase.Add(labelTank, 0, wx.ALIGN_CENTER)
        miniTankSizer = wx.FlexGridSizer(3, 2)
        for i in xrange(2):
            sizerTankStats.AddGrowableCol(i + 1)

        self.minSizerBase.Add(miniTankSizer, 1, wx.EXPAND)

        miniTankSizer.Add(wx.StaticText(self.miniPanel, wx.ID_ANY, ""))

        self.minitankTypeImage = bitmapLoader.getStaticBitmap("shieldPassive_big", self.miniPanel, "icons")
        miniTankSizer.Add(self.minitankTypeImage, 0, wx.ALIGN_CENTER)


        for stability in ("reinforced", "sustained"):
            miniTankSizer.Add(bitmapLoader.getStaticBitmap("regen%s_big" % stability.capitalize(), self.miniPanel, "icons"), 0, wx.ALIGN_CENTER)
            box = wx.BoxSizer(wx.HORIZONTAL)
            miniTankSizer.Add(box, 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(self.miniPanel, wx.ID_ANY, "0.0")
            setattr(self, "labelMiniTank%s" % stability, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            box.Add(wx.StaticText(self.miniPanel, wx.ID_ANY, " HP/S"), 0, wx.ALIGN_LEFT)

        self.minSizerBase.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)

        # Firepower
        sizerHeaderFirepower = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderFirepower, 0, wx.EXPAND | wx.LEFT, 3)

        for panel in ("full", "mini"):
            parent = getattr(self, "%sPanel" % panel)
            labelFirepower = wx.StaticText(parent, wx.ID_ANY, "Firepower")
            labelFirepower.SetFont(boldFont)

            if panel == "mini":
                self.minSizerBase.Add(labelFirepower, 0, wx.ALIGN_CENTER)
            else:
                sizerHeaderFirepower.Add(labelFirepower, 0, wx.ALIGN_CENTER)
                sizerHeaderFirepower.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

            sizerFirepower = wx.FlexGridSizer(1, 3)
            for i in xrange(3):
                sizerFirepower.AddGrowableCol(i)

            self.sizerBase.Add(sizerFirepower, 0, wx.EXPAND | wx.LEFT, 3)
            if panel == "full":
                for damageType, image in (("weapon", "turret") , ("drone", "droneBay")):
                    baseBox = wx.BoxSizer(wx.HORIZONTAL)
                    sizerFirepower.Add(baseBox, 0, wx.ALIGN_CENTER)

                    baseBox.Add(bitmapLoader.getStaticBitmap("%s_big" % image, parent, "icons"), 0, wx.ALIGN_CENTER)

                    box = wx.BoxSizer(wx.VERTICAL)
                    baseBox.Add(box, 0, wx.ALIGN_CENTER)

                    box.Add(wx.StaticText(parent, wx.ID_ANY, damageType.capitalize()), 0, wx.ALIGN_LEFT)

                    hbox = wx.BoxSizer(wx.HORIZONTAL)
                    box.Add(hbox, 1, wx.ALIGN_CENTER)

                    lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
                    setattr(self, "label%sDps%s" % (panel.capitalize() ,damageType.capitalize()), lbl)

                    hbox.Add(lbl, 0, wx.ALIGN_CENTER)
                    hbox.Add(wx.StaticText(parent, wx.ID_ANY, " DPS"), 0, wx.ALIGN_CENTER)

            if panel == "mini":
                targetSizer = self.minSizerBase
            else:
                targetSizer = sizerFirepower

            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            targetSizer.Add(baseBox, 0, wx.ALIGN_LEFT)
            if panel == "full":
                baseBox.Add(bitmapLoader.getStaticBitmap("volley_big", parent, "icons"), 0, wx.ALIGN_CENTER)

            box = wx.BoxSizer(wx.VERTICAL)
            baseBox.Add(box, 1, wx.ALIGN_CENTER)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 1, wx.ALIGN_LEFT | wx.LEFT, 3)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sVolleyTotal" % panel.capitalize(), lbl)
            hbox.Add(wx.StaticText(parent, wx.ID_ANY, "Volley: "), 0, wx.ALIGN_LEFT)
            hbox.Add(lbl, 0, wx.EXPAND)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 1, wx.ALIGN_LEFT | wx.LEFT, 3)


            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sDpsTotal" % panel.capitalize(), lbl)
            hbox.Add(wx.StaticText(parent, wx.ID_ANY, "DPS: "), 0, wx.ALIGN_LEFT)
            hbox.Add(lbl, 0, wx.ALIGN_CENTER)

        self.minSizerBase.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)

        # Capacitor
        for panel in ("full", "mini"):
            parent = getattr(self, "%sPanel" % panel)
            labelCap = wx.StaticText(parent, wx.ID_ANY, "Capacitor")
            labelCap.SetFont(boldFont)
            sizerHeaderCapacitor = wx.BoxSizer(wx.HORIZONTAL)

            if panel == "mini":
                self.minSizerBase.Add(labelCap, 0, wx.ALIGN_CENTER)
                sizerCapacitor = self.minSizerBase
            else:
                self.sizerBase.Add(sizerHeaderCapacitor, 0, wx.EXPAND | wx.LEFT, 1)
                sizerHeaderCapacitor.Add(labelCap, 0, wx.ALIGN_CENTER)
                sizerHeaderCapacitor.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)
                sizerCapacitor = wx.GridSizer(1, 2)
                self.sizerBase.Add(sizerCapacitor, 0, wx.EXPAND  | wx.LEFT, 1)


            # Capacitor capacity and time
            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            sizerCapacitor.Add(baseBox, 0, wx.ALIGN_LEFT)

            if panel == "full":
                baseBox.Add(bitmapLoader.getStaticBitmap("capacitorInfo_big", parent, "icons"), 0, wx.ALIGN_CENTER)

            box = wx.BoxSizer(wx.VERTICAL)
            baseBox.Add(box, 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 0, wx.ALIGN_LEFT)

            hbox.Add(wx.StaticText(parent, wx.ID_ANY, "Total: "), 0, wx.ALIGN_LEFT | wx.LEFT, 3)
            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sCapacitorCapacity" % panel.capitalize(), lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

            if panel == "full":
                hbox.Add(wx.StaticText(parent, wx.ID_ANY, " GJ"), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(parent, wx.ID_ANY, "Lasts ")
            hbox.Add(lbl, 0, wx.ALIGN_LEFT | wx.LEFT, 3)
            setattr(self, "label%sCapacitorState" % panel.capitalize(), lbl)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0s")
            setattr(self, "label%sCapacitorTime" % panel.capitalize(), lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

            # Capacitor balance
            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            sizerCapacitor.Add(baseBox, 0, wx.ALIGN_TOP)

            baseBox.Add(bitmapLoader.getStaticBitmap("capacitorRecharge_big", parent, "icons"), 0, wx.ALIGN_CENTER)

            # Recharge
            chargeSizer = wx.FlexGridSizer(2, 3)
            baseBox.Add(chargeSizer, 0, wx.ALIGN_CENTER)

            chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, "+ "), 0, wx.ALIGN_CENTER)
            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sCapacitorRecharge" % panel.capitalize(), lbl)
            chargeSizer.Add(lbl, 0, wx.ALIGN_CENTER)
            chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, " GJ/s"), 0, wx.ALIGN_CENTER)

            # Discharge
            chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, "- "), 0, wx.ALIGN_CENTER)
            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sCapacitorDischarge" % panel.capitalize(), lbl)
            chargeSizer.Add(lbl, 0, wx.ALIGN_CENTER)
            chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, " GJ/s"), 0, wx.ALIGN_CENTER)

        self.minSizerBase.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)

        # Targeting & Misc
        grid = wx.GridSizer(1, 2)
        self.sizerBase.Add(grid, 0, wx.EXPAND | wx.LEFT, 3)

        # Targeting header
        sizerHeaderTargeting = wx.BoxSizer(wx.HORIZONTAL)
        grid.Add(sizerHeaderTargeting, 0, wx.EXPAND)

        labelTargeting = wx.StaticText(self.fullPanel, wx.ID_ANY, "Targeting")
        labelTargeting.SetFont(boldFont)

        sizerHeaderTargeting.Add(labelTargeting, 0, wx.ALIGN_CENTER)
        sizerHeaderTargeting.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

        # Misc header
        sizerHeaderMisc = wx.BoxSizer(wx.HORIZONTAL)
        grid.Add(sizerHeaderMisc, 0, wx.EXPAND)

        labelMisc = wx.StaticText(self.fullPanel, wx.ID_ANY, "Misc")
        labelMisc.SetFont(boldFont)

        sizerHeaderMisc.Add(labelMisc, 0, wx.ALIGN_CENTER)
        sizerHeaderMisc.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

        gridTargetingMisc = wx.GridSizer(1, 2)
        self.sizerBase.Add(gridTargetingMisc, 0, wx.EXPAND | wx.LEFT, 3)

        # Targeting

        gridTargeting = wx.FlexGridSizer(4, 2)
        gridTargeting.AddGrowableCol(1)
        gridTargetingMisc.Add(gridTargeting)

        labels = (("Targets", "Targets", ""),
                  ("Range", "Range", "km"),
                  ("Scan res.", "ScanRes", "mm"),
                  ("Sensor str.", "SensorStr", ""))

        for header, labelShort, unit in labels:
            gridTargeting.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "%s: " % header), 0, wx.ALIGN_LEFT)

            box = wx.BoxSizer(wx.HORIZONTAL)
            gridTargeting.Add(box, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0")
            setattr(self, "label%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lblUnit = wx.StaticText(self.fullPanel, wx.ID_ANY, " %s" % unit)
            setattr(self, "labelUnit%s" % labelShort, lblUnit)
            box.Add(lblUnit, 0, wx.ALIGN_LEFT)

        # Misc

        gridMisc = wx.FlexGridSizer(4, 2)
        gridMisc.AddGrowableCol(1)
        gridTargetingMisc.Add(gridMisc)

        labels = (("Speed", "Speed", "m/s"),
                  ("Align time", "AlignTime", "s"),
                  ("Cargo", "Cargo", u"m\u00B3"),
                  ("Signature", "SigRadius", "m"))

        for header, labelShort, unit in labels:
            gridMisc.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "%s: " % header), 0, wx.ALIGN_LEFT)

            box = wx.BoxSizer(wx.HORIZONTAL)
            gridMisc.Add(box, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0")
            setattr(self, "labelFull%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lblUnit = wx.StaticText(self.fullPanel, wx.ID_ANY, " %s" % unit)
            setattr(self, "labelFullUnit%s" % labelShort, lblUnit)
            box.Add(lblUnit, 0, wx.ALIGN_LEFT)


        # Mini speed & align
        labelManeuverability = wx.StaticText(self.miniPanel, wx.ID_ANY, "Agility")
        labelManeuverability.SetFont(boldFont)
        self.minSizerBase.Add(labelManeuverability, 0, wx.ALIGN_CENTER)

        labels = (("Vel", "Speed", "m/s"),
                  ("Align", "AlignTime", "s"))

        for header, labelShort, unit in labels:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.minSizerBase.Add(sizer, 0, wx.ALIGN_LEFT)

            sizer.Add(wx.StaticText(self.miniPanel, wx.ID_ANY, "%s: " % header), 0, wx.ALIGN_LEFT| wx.LEFT, 3)

            box = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(box, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(self.miniPanel, wx.ID_ANY, "0")
            setattr(self, "labelMini%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lblUnit = wx.StaticText(self.miniPanel, wx.ID_ANY, " %s" % unit)
            setattr(self, "labelMiniUnit%s" % labelShort, lblUnit)
            box.Add(lblUnit, 0, wx.ALIGN_LEFT)

        self.minSizerBase.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)

        # Mini price stuff
        labelPrice = wx.StaticText(self.miniPanel, wx.ID_ANY, "Price")
        labelPrice.SetFont(boldFont)
        self.minSizerBase.Add(labelPrice, 0, wx.ALIGN_CENTER)

        image = "totalPrice_big"
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.minSizerBase.Add(box)

        box.Add(bitmapLoader.getStaticBitmap(image, self.miniPanel, "icons"), 0, wx.ALIGN_CENTER)

        lbl = wx.StaticText(self.miniPanel, wx.ID_ANY, "0.00")
        setattr(self, "labelMiniPriceTotal", lbl)
        box.Add(lbl, 0, wx.ALIGN_CENTER)

        box.Add(wx.StaticText(self.miniPanel, wx.ID_ANY, " m ISK"), 0, wx.ALIGN_CENTER)


        # Price
        sizerHeaderPrice = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderPrice, 0, wx.EXPAND | wx.LEFT, 3)

        labelPrice = wx.StaticText(self.fullPanel, wx.ID_ANY, "Price")
        labelPrice.SetFont(boldFont)
        sizerHeaderPrice.Add(labelPrice, 0, wx.ALIGN_CENTER)

        sizerHeaderPrice.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

        # Grid for the price stuff.
        gridPrice = wx.GridSizer(1, 3)
        self.sizerBase.Add(gridPrice, 0, wx.EXPAND | wx.LEFT, 3)

        for type in ("ship", "fittings", "total"):
            image = "%sPrice_big" % type if type != "ship" else "ship_big"
            box = wx.BoxSizer(wx.HORIZONTAL)
            gridPrice.Add(box)

            box.Add(bitmapLoader.getStaticBitmap(image, self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)

            vbox = wx.BoxSizer(wx.VERTICAL)
            box.Add(vbox, 1, wx.EXPAND)

            vbox.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, type.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            vbox.Add(hbox)

            lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.00")
            setattr(self, "labelPrice%s" % type, lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

            hbox.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, " m ISK"), 0, wx.ALIGN_LEFT)
