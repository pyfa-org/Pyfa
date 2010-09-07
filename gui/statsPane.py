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
from util import formatAmount
from gui.pyfatogglepanel import TogglePanel

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

    def getTextExtentW(self, text):
        width, height = self.GetTextExtent( text )
        return width

    def fitChanged(self, event):
        cFit = controller.Fit.getInstance()
        fit = cFit.getFit(event.fitID)
        statsMiniFull = (("label%sUsedTurretHardpoints", lambda: fit.getHardpointsUsed(Hardpoint.TURRET), 0, 0, 0),
                         ("label%sTotalTurretHardpoints", lambda: fit.ship.getModifiedItemAttr('turretSlotsLeft'), 0, 0, 0),
                         ("label%sUsedLauncherHardpoints", lambda: fit.getHardpointsUsed(Hardpoint.MISSILE), 0, 0, 0),
                         ("label%sTotalLauncherHardpoints", lambda: fit.ship.getModifiedItemAttr('launcherSlotsLeft'), 0, 0, 0),
                         ("label%sUsedCalibrationPoints", lambda: fit.calibrationUsed, 0, 0, 0),
                         ("label%sTotalCalibrationPoints", lambda: fit.ship.getModifiedItemAttr('upgradeCapacity'), 0, 0, 0),
                         ("label%sUsedPg", lambda: fit.pgUsed, 4, 0, 9),
                         ("label%sUsedCpu", lambda: fit.cpuUsed, 4, 0, 9),
                         ("label%sTotalPg", lambda: fit.ship.getModifiedItemAttr("powerOutput"), 4, 0, 9),
                         ("label%sTotalCpu", lambda: fit.ship.getModifiedItemAttr("cpuOutput"), 4, 0, 9),
                         ("label%sVolleyTotal", lambda: fit.weaponVolley, 3, 0, 9),
                         ("label%sDpsTotal", lambda: fit.totalDPS, 3, 0, 9),
                         ("label%sCapacitorCapacity", lambda: fit.ship.getModifiedItemAttr("capacitorCapacity"), 3, 0, 9),
                         ("label%sCapacitorRecharge", lambda: fit.capRecharge, 3, 0, 0),
                         ("label%sCapacitorDischarge", lambda: fit.capUsed, 3, 0, 0),
                         ("label%sSpeed", lambda: fit.ship.getModifiedItemAttr("maxVelocity"), 3, 0, 0),
                         ("label%sAlignTime", lambda: fit.alignTime, 3, 0, 0))

        stats = (("labelFullUsedDroneBay", lambda: fit.droneBayUsed, 3, 0, 9),
                 ("labelFullUsedDroneBandwidth", lambda: fit.droneBandwidthUsed, 3, 0, 9),
                 ("labelFullTotalDroneBay", lambda: fit.ship.getModifiedItemAttr("droneCapacity"), 3, 0, 9),
                 ("labelFullTotalDroneBandwidth", lambda: fit.ship.getModifiedItemAttr("droneBandwidth"), 3, 0, 9),
                 ("labelFullDpsWeapon", lambda: fit.weaponDPS, 3, 0, 9),
                 ("labelFullDpsDrone", lambda: fit.droneDPS, 3, 0, 9),
                 ("labelTankSustainedShieldPassive", lambda: fit.calculateShieldRecharge(), 3, 0, 9),
                 ("labelTargets", lambda: fit.maxTargets, 3, 0, 0),
                 ("labelRange", lambda: fit.ship.getModifiedItemAttr('maxTargetRange') / 1000, 3, 0, 0),
                 ("labelScanRes", lambda: fit.ship.getModifiedItemAttr('scanResolution'), 3, 0, 0),
                 ("labelSensorStr", lambda: fit.scanStrength, 3, 0, 0),
                 ("labelFullCargo", lambda: fit.extraAttributes["capacity"], 3, 0, 9),
                 ("labelFullSigRadius", lambda: fit.ship.getModifiedItemAttr("signatureRadius"), 3, 0, 9))

        for panel in ("Mini", "Full"):
            for labelName, value, prec, lowest, highest in statsMiniFull:
                label = getattr(self, labelName % panel)
                value = value() if fit is not None else 0
                value = value if value is not None else 0
                if isinstance(value, basestring):
                    label.SetLabel(value)
                    label.SetToolTip(wx.ToolTip(value))
                else:
                    label.SetLabel(formatAmount(value, prec, lowest, highest))
                    label.SetToolTip(wx.ToolTip("%.1f" % value))

        for labelName, value, prec, lowest, highest in stats:
            label = getattr(self, labelName)
            value = value() if fit is not None else 0
            value = value if value is not None else 0
            label.SetLabel(formatAmount(value, prec, lowest, highest))
            label.SetToolTip(wx.ToolTip("%.1f" % value))
        # cap stuff
        capState = fit.capState if fit is not None else 0
        capStable = fit.capStable if fit is not None else False
        lblNameTime = "label%sCapacitorTime"
        lblNameState = "label%sCapacitorState"
        if isinstance(capState, tuple):
            t = "%.1f%%-%.1f%%" % capState
            s = ""
        else:
            t = ("%ds" if not capStable else "%.1f%%") % capState
            s = "Stable: " if capStable else "Lasts "
        for panel in ("Mini", "Full"):
            getattr(self, lblNameTime % panel).SetLabel(t)
            getattr(self, lblNameState % panel).SetLabel(s)

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
                    capitalizedType = resourceType[0].capitalize() + resourceType[1:]

                    gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))
                    resUsed = getattr(fit,"%sUsed" % resourceType)

                    if resMax[i]() > 0:
                        gauge.SetRange(resMax[i]())
                        gauge.SetValue(resUsed)
                    i+=1
                else:
                    if i>1 and panel == "Mini": break

                    capitalizedType = resourceType[0].capitalize() + resourceType[1:]

                    gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))

                    gauge.SetRange(100)
                    gauge.SetValue(0)
                    i+=1

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
        total = 0
        for tankType in ("shield", "armor", "hull"):
            lbl = getattr(self, "labelResistance%sEhp" % tankType.capitalize())
            if ehp is not None:
                total += ehp[tankType]
                lbl.SetLabel(formatAmount(ehp[tankType], 3, 0, 9))
                lbl.SetToolTip(wx.ToolTip("%s: %d" % (tankType.capitalize(), ehp[tankType])))
            else:
                lbl.SetLabel("0")

        self.labelEhp.SetLabel(formatAmount(total, 3, 0, 9))
        self.labelEhp.SetToolTip(wx.ToolTip("Effective: %d" % total))

        damagePattern = fit.damagePattern if fit is not None else None
        for damageType in ("em", "thermal", "kinetic", "explosive"):
            lbl = getattr(self, "labelResistanceDamagepattern%s" % damageType.capitalize())
            if damagePattern:
                lbl.SetLabel("%.2f" % getattr(damagePattern, "%sAmount" % damageType))
            else:
                lbl.SetLabel("0.00")

        for stability in ("reinforced", "sustained"):
            if stability == "reinforced" and fit != None:
                tank = fit.effectiveTank
            elif stability == "sustained" and fit != None:
                tank = fit.effectiveSustainableTank
            else:
                tank = None


            for name in ("shield", "armor", "hull"):
                lbl = getattr(self, "labelTank%s%sActive" % (stability.capitalize(), name.capitalize()))
                if tank is not None:
                    lbl.SetLabel("%.1f" % tank["%sRepair" % name])
                else:
                    lbl.SetLabel("0.0")

        tank = fit.effectiveTank if fit != None else None
        maxTank = ("shieldPassive", fit.calculateShieldRecharge() if fit else 0)
        for tankType in ("shield", "armor", "hull"):
            if tank is not None:
                maxType, maxAmount = maxTank
                currAmount = tank["%sRepair" % tankType]
                if  currAmount > maxAmount:
                    maxTank = ("%s" % tankType, currAmount)

        maxType, maxAmount = maxTank

        if maxType == "shieldPassive":
            self.labelMiniTankReinforced.SetLabel("")
            self.labelMiniTankSustained.SetLabel(formatAmount(maxAmount, 3, 0, 9))
            self.labelMiniTankUnitReinforced.SetLabel("")
            bitmap = bitmapLoader.getBitmap("%s_big" % maxType, "icons")
        else:
            self.labelMiniTankReinforced.SetLabel(formatAmount(maxAmount, 3, 0, 9))
            sustainable = fit.sustainableTank["%sRepair" % maxType]
            self.labelMiniTankSustained.SetLabel(formatAmount(sustainable, 3, 0, 9))
            self.labelMiniTankUnitReinforced.SetLabel(" HP/S")
            bitmap = bitmapLoader.getBitmap("%sActive_big" % maxType, "icons")

        self.minitankTypeImage.SetBitmap(bitmap)
        self.Layout()
        self.fullPanel.Layout()
        self.miniPanel.Layout()
        event.Skip()

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._showNormalGauges = False
        self._showTogglePanels = True

        self.initWithTogglePanels(parent)

    def initNormal(self, parent):    
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        standardFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        standardFont.SetPointSize(8)
        self.SetFont(standardFont)
        # Register events
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)

        self.pickerSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.pickerSizer)

        collapsible = wx.CollapsiblePane(self, label="Stats")

        colPane=collapsible.GetPane()
        colPane.SetMinSize(wx.Size(0,0))
        colPane.SetSize(wx.Size(0,0))

        collapsible.Expand()
        collapsible.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChanged)

        self.pickerSizer.Add(collapsible, 0, wx.EXPAND)

        self.fullSize = wx.Size()

        self.fullPanel = wx.Panel(self)

        self.pickerSizer.Add(self.fullPanel, 1, wx.EXPAND)

        self.miniSize = wx.Size()

        self.miniPanel = wx.Panel(self)
        self.miniPanel.Hide()


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
            sizer.SetMinSize(wx.Size(27 + self.getTextExtentW("400/400"), 0))
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

                sizer.Add(bitmap, 0, wx.ALIGN_CENTER)
                sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL)

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
                        stats.Add(absolute, 0, wx.EXPAND)

                        if panel == "full":
                            b = wx.BoxSizer(wx.HORIZONTAL)
                            main.Add(b, 1, wx.ALIGN_CENTER)

                            b.Add(bitmap, 0, wx.ALIGN_BOTTOM)

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

                        units = {"cpu":" tf", "pg":" MW", "droneBandwidth":" mbit/s", "droneBay":u" m\u00B3"}
                        lbl = wx.StaticText(parent, wx.ID_ANY, "%s" % units[type])
                        absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                        # Gauges modif. - Darriele
                        if self._showNormalGauges == True:
                            gauge = wx.Gauge(parent, wx.ID_ANY, 100)
                            gauge.SetMinSize((80, 20))
                        else:
                            gauge = PG.PyGauge(parent, wx.ID_ANY, 100)
                            gauge.SetMinSize((self.getTextExtentW("999.9k/1.3M GJ"), 23))
                            gauge.SetFractionDigits(2)

                        setattr(self, "gauge%s%s" % (panel.capitalize(),capitalizedType), gauge)
                        stats.Add(gauge, 0, wx.ALIGN_CENTER)
                if i >0 and panel == "mini":
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
        col = 0
        row = 0
        sizerResistances = wx.GridBagSizer(4, 6)
        for i in xrange(6):
            sizerResistances.AddGrowableCol(i + 1)

        self.sizerBase.Add(sizerResistances, 0, wx.EXPAND | wx.LEFT, 3)

        # Add an empty label, then the rest.
        sizerResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY), wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ))
        col+=1
        for damageType in ("em", "thermal", "kinetic", "explosive"):
            sizerResistances.Add(bitmapLoader.getStaticBitmap("%s_big" % damageType, self.fullPanel, "icons"), wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
            col+=1

        sizerResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "EHP"), wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
        col=0
        row+=1

        gaugeColours=( ((38,133,198),(52,86,98)), ((198,38,38),(83,65,67)), ((163,163,163),(74,90,93)), ((198,133,38),(81,83,67)) )

        for tankType in ("shield", "armor", "hull", "separator", "damagePattern"):
            if tankType != "separator":
                sizerResistances.Add(bitmapLoader.getStaticBitmap("%s_big" % tankType, self.fullPanel, "icons"), wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
                col+=1

            else:
                sizerResistances.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), wx.GBPosition( row, col ), wx.GBSpan( 1, 6 ), wx.EXPAND|wx.ALIGN_CENTER)
                row+=1
                col=0

                continue
            currGColour=0

            for damageType in ("em", "thermal", "kinetic", "explosive"):

                box = wx.BoxSizer(wx.HORIZONTAL)
                sizerResistances.Add(box, wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)


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
                    lbl.SetFractionDigits(1)

                setattr(self, "labelResistance%s%s" % (tankType.capitalize(), damageType.capitalize()), lbl)
                box.Add(lbl, 0, wx.ALIGN_CENTER)

                if self._showNormalGauges == True:
                    box.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "%"), 0, wx.ALIGN_CENTER)
                col+=1
            box = wx.BoxSizer(wx.VERTICAL)
            box.SetMinSize(wx.Size(self.getTextExtentW("WWWWk"), -1))

            lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0" if tankType != "damagePattern" else "")
            box.Add(lbl, 0, wx.ALIGN_CENTER)

            setattr(self, "labelResistance%sEhp" % tankType.capitalize(), lbl)
            sizerResistances.Add(box, wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
            row+=1
            col=0


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
            setattr(self, "labelMiniTank%s" % stability.capitalize(), lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(self.miniPanel, wx.ID_ANY, " HP/S")
            setattr(self, "labelMiniTankUnit%s" % stability.capitalize(), lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

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

            gridS = wx.GridSizer(2,2,0,0)

            baseBox.Add(gridS, 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sVolleyTotal" % panel.capitalize(), lbl)
            gridS.Add(wx.StaticText(parent, wx.ID_ANY, " Volley: "), 0, wx.ALL | wx.ALIGN_RIGHT)
            gridS.Add(lbl, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sDpsTotal" % panel.capitalize(), lbl)
            gridS.Add(wx.StaticText(parent, wx.ID_ANY, " DPS: "), 0, wx.ALL | wx.ALIGN_RIGHT)
            gridS.Add(lbl, 0, wx.ALIGN_LEFT)

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



        # The custom made collapsible panel demo
        priceTPanel = TogglePanel(self.fullPanel)
        priceTPanel.SetLabel(u"Price")

        self.sizerBase.Add(priceTPanel,0, wx.EXPAND | wx.LEFT | wx.RIGHT, 3)
        priceContentPane = priceTPanel.GetContentPane()

        # Grid for the price stuff.

        gridPrice = wx.GridSizer(1, 3)
        priceTPanel.AddSizer(gridPrice)


        for type in ("ship", "fittings", "total"):
            image = "%sPrice_big" % type if type != "ship" else "ship_big"
            box = wx.BoxSizer(wx.HORIZONTAL)
            gridPrice.Add(box)

            box.Add(bitmapLoader.getStaticBitmap(image, priceContentPane, "icons"), 0, wx.ALIGN_CENTER)

            vbox = wx.BoxSizer(wx.VERTICAL)
            box.Add(vbox, 1, wx.EXPAND)

            vbox.Add(wx.StaticText(priceContentPane, wx.ID_ANY, type.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            vbox.Add(hbox)

            lbl = wx.StaticText(priceContentPane, wx.ID_ANY, "0.00")
            setattr(self, "labelPrice%s" % type, lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

            hbox.Add(wx.StaticText(priceContentPane, wx.ID_ANY, " m ISK"), 0, wx.ALIGN_LEFT)

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

# The pencil MUST fit in the hole :)

        self.fullPanel.Fit()
        self.fullSize=self.fullPanel.GetBestSize()
        self.fullSize.SetWidth( self.fullSize.GetWidth())
        self.fullPanel.SetMinSize( self.fullSize)

        self.miniPanel.Fit()
        self.miniSize=self.miniPanel.GetBestSize()
        self.miniSize.SetWidth( self.miniSize.GetWidth()+30)
        self.miniPanel.SetMinSize( self.miniSize)


    def initWithTogglePanels(self, parent):

        self.mainparent = parent

        
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        standardFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        standardFont.SetPointSize(8)
        self.SetFont(standardFont)
        # Register events
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)

        self.pickerSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.pickerSizer)

        collapsible = wx.CollapsiblePane(self, label="Stats")

        colPane=collapsible.GetPane()
        colPane.SetMinSize(wx.Size(0,0))
        colPane.SetSize(wx.Size(0,0))

        collapsible.Expand()
        collapsible.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChanged)

        self.pickerSizer.Add(collapsible, 0, wx.EXPAND)

        self.fullSize = wx.Size()

        self.fullPanel = wx.Panel(self)

        self.pickerSizer.Add(self.fullPanel, 1, wx.EXPAND)

        self.miniSize = wx.Size()

        self.miniPanel = wx.Panel(self)
        self.miniPanel.Hide()


        minBase = wx.BoxSizer(wx.VERTICAL)
        self.miniPanel.SetSizer(minBase)

        self.minSizerBase = wx.BoxSizer(wx.VERTICAL)
        minBase.Add(self.minSizerBase, 0, wx.EXPAND | wx.TOP, 15)

        self.boldFont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.boldFont.SetWeight(wx.BOLD)

        #Temp stuff - should remove it once we are done splitting initWithTogglePanel
        boldFont = self.boldFont

        #Populate the full panel first
        self.sizerBase = wx.BoxSizer(wx.VERTICAL)
        self.fullPanel.SetSizer(self.sizerBase)

### TogglePanels



        self.initResourcesPanel( self.mainparent)

        self.initResistancesPanel( self.mainparent )

        self.initRechargePanelFull( self.mainparent )
        self.initRechargePanelMini( self.mainparent )
        
        self.initFirepowerPanel( self.mainparent )

        self.initCapPanel( self.mainparent )

        self.initTargetingMiscPanel( self.mainparent )
        self.initSpeedAlignPanelMini( self.mainparent )

        self.initPricePanelMini( self.mainparent )
        self.initPricePanelFull( self.mainparent )

###

#       Final stuff refit the whole panel
#
#       The pencil MUST fit in the hole :)

        self.fullPanel.Fit()
        self.fullSize=self.fullPanel.GetBestSize()
        self.fullSize.SetWidth( self.fullSize.GetWidth())
        self.fullPanel.SetMinSize( self.fullSize)

        self.miniPanel.Fit()
        self.miniSize=self.miniPanel.GetBestSize()
        self.miniSize.SetWidth( self.miniSize.GetWidth()+30)
        self.miniPanel.SetMinSize( self.miniSize)


    def initResourcesPanel( self, parent):

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
            labelResources.SetFont(self.boldFont)
            sizer = wx.FlexGridSizer(3, 2)
            sizer.SetMinSize(wx.Size(27 + self.getTextExtentW("400/400"), 0))
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

                sizer.Add(bitmap, 0, wx.ALIGN_CENTER)
                sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL)

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
                        stats.Add(absolute, 0, wx.EXPAND)

                        if panel == "full":
                            b = wx.BoxSizer(wx.HORIZONTAL)
                            main.Add(b, 1, wx.ALIGN_CENTER)

                            b.Add(bitmap, 0, wx.ALIGN_BOTTOM)

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

                        units = {"cpu":" tf", "pg":" MW", "droneBandwidth":" mbit/s", "droneBay":u" m\u00B3"}
                        lbl = wx.StaticText(parent, wx.ID_ANY, "%s" % units[type])
                        absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                        # Gauges modif. - Darriele
                        if self._showNormalGauges == True:
                            gauge = wx.Gauge(parent, wx.ID_ANY, 100)
                            gauge.SetMinSize((80, 20))
                        else:
                            gauge = PG.PyGauge(parent, wx.ID_ANY, 100)
                            gauge.SetMinSize((self.getTextExtentW("999.9k/1.3M GJ"), 23))
                            gauge.SetFractionDigits(2)

                        setattr(self, "gauge%s%s" % (panel.capitalize(),capitalizedType), gauge)
                        stats.Add(gauge, 0, wx.ALIGN_CENTER)
                if i >0 and panel == "mini":
                    base.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)

                if i == 0 and panel == "full":
                    base.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.VERTICAL), 0, wx.EXPAND)
        

    def initResistancesPanel( self, parent):

        # Resistances
        sizerHeaderResistances = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderResistances, 0, wx.EXPAND | wx.LEFT, 3)

        # Header & EHP
        labelResistances = wx.StaticText(self.fullPanel, wx.ID_ANY, "Resistances")
        labelResistances.SetFont(self.boldFont)
        sizerHeaderResistances.Add(labelResistances, 0, wx.ALIGN_CENTER)

        sizerHeaderResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, " (Effective HP: "), 0, wx.ALIGN_CENTER)

        self.labelEhp = wx.StaticText(self.fullPanel, wx.ID_ANY, "0")
        sizerHeaderResistances.Add(self.labelEhp, 0, wx.ALIGN_CENTER)

        sizerHeaderResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, ")"), 0, wx.ALIGN_CENTER)
        sizerHeaderResistances.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

        # Display table
        col = 0
        row = 0
        sizerResistances = wx.GridBagSizer(4, 6)
        for i in xrange(6):
            sizerResistances.AddGrowableCol(i + 1)

        self.sizerBase.Add(sizerResistances, 0, wx.EXPAND | wx.LEFT, 3)

        # Add an empty label, then the rest.
        sizerResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY), wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ))
        col+=1
        for damageType in ("em", "thermal", "kinetic", "explosive"):
            sizerResistances.Add(bitmapLoader.getStaticBitmap("%s_big" % damageType, self.fullPanel, "icons"), wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
            col+=1

        sizerResistances.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "EHP"), wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
        col=0
        row+=1

        gaugeColours=( ((38,133,198),(52,86,98)), ((198,38,38),(83,65,67)), ((163,163,163),(74,90,93)), ((198,133,38),(81,83,67)) )

        for tankType in ("shield", "armor", "hull", "separator", "damagePattern"):
            if tankType != "separator":
                sizerResistances.Add(bitmapLoader.getStaticBitmap("%s_big" % tankType, self.fullPanel, "icons"), wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
                col+=1

            else:
                sizerResistances.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), wx.GBPosition( row, col ), wx.GBSpan( 1, 6 ), wx.EXPAND|wx.ALIGN_CENTER)
                row+=1
                col=0

                continue
            currGColour=0

            for damageType in ("em", "thermal", "kinetic", "explosive"):

                box = wx.BoxSizer(wx.HORIZONTAL)
                sizerResistances.Add(box, wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)


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
                    lbl.SetFractionDigits(1)

                setattr(self, "labelResistance%s%s" % (tankType.capitalize(), damageType.capitalize()), lbl)
                box.Add(lbl, 0, wx.ALIGN_CENTER)

                if self._showNormalGauges == True:
                    box.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "%"), 0, wx.ALIGN_CENTER)
                col+=1
            box = wx.BoxSizer(wx.VERTICAL)
            box.SetMinSize(wx.Size(self.getTextExtentW("WWWWk"), -1))

            lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0" if tankType != "damagePattern" else "")
            box.Add(lbl, 0, wx.ALIGN_CENTER)

            setattr(self, "labelResistance%sEhp" % tankType.capitalize(), lbl)
            sizerResistances.Add(box, wx.GBPosition( row, col ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER)
            row+=1
            col=0
        


    def initRechargePanelFull( self, parent ):

        # RechargeRates
        sizerHeaderRechargeRates = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderRechargeRates, 0, wx.EXPAND | wx.LEFT, 3)

        labelRecharge = wx.StaticText(self.fullPanel, wx.ID_ANY, "Recharge Rates")
        labelRecharge.SetFont(self.boldFont)

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
        


    def initRechargePanelMini( self, parent):

        #Mini tank display
        labelTank = wx.StaticText(self.miniPanel, wx.ID_ANY, "Tank")
        labelTank.SetFont(self.boldFont)
        self.minSizerBase.Add(labelTank, 0, wx.ALIGN_CENTER)
        miniTankSizer = wx.FlexGridSizer(3, 2)
        for i in xrange(2):
            miniTankSizer.AddGrowableCol(i + 1)

        self.minSizerBase.Add(miniTankSizer, 1, wx.EXPAND)

        miniTankSizer.Add(wx.StaticText(self.miniPanel, wx.ID_ANY, ""))

        self.minitankTypeImage = bitmapLoader.getStaticBitmap("shieldPassive_big", self.miniPanel, "icons")
        miniTankSizer.Add(self.minitankTypeImage, 0, wx.ALIGN_CENTER)


        for stability in ("reinforced", "sustained"):
            miniTankSizer.Add(bitmapLoader.getStaticBitmap("regen%s_big" % stability.capitalize(), self.miniPanel, "icons"), 0, wx.ALIGN_CENTER)
            box = wx.BoxSizer(wx.HORIZONTAL)
            miniTankSizer.Add(box, 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(self.miniPanel, wx.ID_ANY, "0.0")
            setattr(self, "labelMiniTank%s" % stability.capitalize(), lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(self.miniPanel, wx.ID_ANY, " HP/S")
            setattr(self, "labelMiniTankUnit%s" % stability.capitalize(), lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

        self.minSizerBase.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)        

    def initFirepowerPanel(self, parent):

        # Firepower
        sizerHeaderFirepower = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderFirepower, 0, wx.EXPAND | wx.LEFT, 3)

        for panel in ("full", "mini"):
            parent = getattr(self, "%sPanel" % panel)
            labelFirepower = wx.StaticText(parent, wx.ID_ANY, "Firepower")
            labelFirepower.SetFont(self.boldFont)

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

            gridS = wx.GridSizer(2,2,0,0)

            baseBox.Add(gridS, 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sVolleyTotal" % panel.capitalize(), lbl)
            gridS.Add(wx.StaticText(parent, wx.ID_ANY, " Volley: "), 0, wx.ALL | wx.ALIGN_RIGHT)
            gridS.Add(lbl, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sDpsTotal" % panel.capitalize(), lbl)
            gridS.Add(wx.StaticText(parent, wx.ID_ANY, " DPS: "), 0, wx.ALL | wx.ALIGN_RIGHT)
            gridS.Add(lbl, 0, wx.ALIGN_LEFT)

        self.minSizerBase.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)
    


    def initCapPanel(self,parent):

        # Capacitor
        for panel in ("full", "mini"):
            parent = getattr(self, "%sPanel" % panel)
            labelCap = wx.StaticText(parent, wx.ID_ANY, "Capacitor")
            labelCap.SetFont(self.boldFont)
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


    def initTargetingMiscPanel( self, parent):

        tmTPanel = TogglePanel(self.fullPanel)

        # Ugly stuff - we need to improve pyfatogglepanel class to support customized stuff in header
        tmTPanel.SetLabel(u"Targeting                        Misc")

        gridTargetingMisc = wx.GridSizer(1, 2)
        self.sizerBase.Add(tmTPanel, 0, wx.EXPAND | wx.LEFT, 3)
        ContentPanel = tmTPanel.GetContentPane()
        tmTPanel.AddSizer(gridTargetingMisc)                   
        # Targeting

        gridTargeting = wx.FlexGridSizer(4, 2)
        gridTargeting.AddGrowableCol(1)
        gridTargetingMisc.Add(gridTargeting)

        labels = (("Targets", "Targets", ""),
                  ("Range", "Range", "km"),
                  ("Scan res.", "ScanRes", "mm"),
                  ("Sensor str.", "SensorStr", ""))

        for header, labelShort, unit in labels:
            gridTargeting.Add(wx.StaticText(ContentPanel, wx.ID_ANY, "%s: " % header), 0, wx.ALIGN_LEFT)

            box = wx.BoxSizer(wx.HORIZONTAL)
            gridTargeting.Add(box, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(ContentPanel, wx.ID_ANY, "0")
            setattr(self, "label%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lblUnit = wx.StaticText(ContentPanel, wx.ID_ANY, " %s" % unit)
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
            gridMisc.Add(wx.StaticText(ContentPanel, wx.ID_ANY, "%s: " % header), 0, wx.ALIGN_LEFT)

            box = wx.BoxSizer(wx.HORIZONTAL)
            gridMisc.Add(box, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(ContentPanel, wx.ID_ANY, "0")
            setattr(self, "labelFull%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lblUnit = wx.StaticText(ContentPanel, wx.ID_ANY, " %s" % unit)
            setattr(self, "labelFullUnit%s" % labelShort, lblUnit)
            box.Add(lblUnit, 0, wx.ALIGN_LEFT)


    def initSpeedAlignPanelMini(self, parent):
        # Mini speed & align
        labelManeuverability = wx.StaticText(self.miniPanel, wx.ID_ANY, "Agility")
        labelManeuverability.SetFont(self.boldFont)
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


    def initPricePanelMini( self, parent):

        # Mini price stuff
        labelPrice = wx.StaticText(self.miniPanel, wx.ID_ANY, "Price")
        labelPrice.SetFont(self.boldFont)
        self.minSizerBase.Add(labelPrice, 0, wx.ALIGN_CENTER)

        image = "totalPrice_big"
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.minSizerBase.Add(box)

        box.Add(bitmapLoader.getStaticBitmap(image, self.miniPanel, "icons"), 0, wx.ALIGN_CENTER)

        lbl = wx.StaticText(self.miniPanel, wx.ID_ANY, "0.00")
        setattr(self, "labelMiniPriceTotal", lbl)
        box.Add(lbl, 0, wx.ALIGN_CENTER)

        box.Add(wx.StaticText(self.miniPanel, wx.ID_ANY, " m ISK"), 0, wx.ALIGN_CENTER)        


    def initPricePanelFull( self, parent):
        # TogglePanel - Price
        priceTPanel = TogglePanel(self.fullPanel)
        priceTPanel.SetLabel(u"Price")

        self.sizerBase.Add(priceTPanel,0, wx.EXPAND | wx.LEFT | wx.RIGHT, 3)
        priceContentPane = priceTPanel.GetContentPane()

        # Grid for the price stuff.

        gridPrice = wx.GridSizer(1, 3)
        priceTPanel.AddSizer(gridPrice)


        for type in ("ship", "fittings", "total"):
            image = "%sPrice_big" % type if type != "ship" else "ship_big"
            box = wx.BoxSizer(wx.HORIZONTAL)
            gridPrice.Add(box)

            box.Add(bitmapLoader.getStaticBitmap(image, priceContentPane, "icons"), 0, wx.ALIGN_CENTER)

            vbox = wx.BoxSizer(wx.VERTICAL)
            box.Add(vbox, 1, wx.EXPAND)

            vbox.Add(wx.StaticText(priceContentPane, wx.ID_ANY, type.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            vbox.Add(hbox)

            lbl = wx.StaticText(priceContentPane, wx.ID_ANY, "0.00")
            setattr(self, "labelPrice%s" % type, lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

            hbox.Add(wx.StaticText(priceContentPane, wx.ID_ANY, " m ISK"), 0, wx.ALIGN_LEFT)




