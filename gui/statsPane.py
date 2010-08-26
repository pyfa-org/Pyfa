#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
from gui import bitmapLoader
import gui.mainFrame

class StatsPane(wx.Panel):
    def collapseChanged(self, event):
        collapsed = event.Collapsed
        if collapsed:
            self.pickerSizer.Replace(self.fullPanel, self.minPanel)
            self.SetMinSize(self.minSize)
        else:
            self.pickerSizer.Replace(self.minPanel, self.fullPanel)
            self.SetMinSize(self.fullSize)

        self.fullPanel.Show(not collapsed)
        self.minPanel.Show(collapsed)
        gui.mainFrame.MainFrame.getInstance().statsSizer.Layout()

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

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

        self.minSize = wx.Size()
        self.minSize.SetWidth(100)
        self.minPanel = wx.Panel(self)
        self.minPanel.Hide()
        self.minPanel.SetMinSize(self.minSize)

        minBase = wx.BoxSizer(wx.VERTICAL)
        self.minPanel.SetSizer(minBase)

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

        # Turret slots, Launcher slots & calibration
        sizerHardResources = wx.FlexGridSizer(3, 2)
        for i in xrange(3):
            sizerHardResources.AddGrowableCol(i + 1)

        sizerResources.Add(sizerHardResources, 1, wx.ALIGN_CENTER)

        for panel in ("full", "min"):
            parent = getattr(self, "%sPanel" % panel)
            # Resources header
            labelResources = wx.StaticText(parent, wx.ID_ANY, "Resources")
            labelResources.SetFont(boldFont)
            if panel == "min":
                self.minSizerBase.Add(labelResources, 0, wx.ALIGN_CENTER)
            else:
                sizerHeaderResources.Add(labelResources, 0, wx.ALIGN_CENTER)
                sizerHeaderResources.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

            for type in ("turret", "launcher"):
                bitmap = bitmapLoader.getStaticBitmap("%s_big" % type, parent, "icons")
                box = wx.BoxSizer(wx.HORIZONTAL)
                if panel == "min":
                    self.minSizerBase.Add(bitmap, 0, wx.ALIGN_CENTER)
                    self.minSizerBase.Add(box, 0, wx.ALIGN_CENTER)
                else:
                    sizerHardResources.Add(bitmap, 0, wx.ALIGN_CENTER)
                    sizerHardResources.Add(box, 0, wx.ALIGN_CENTER)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sAvailable%sHardpoints" % (panel, type), lbl)
                box.Add(lbl, 0, wx.ALIGN_LEFT)

                box.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_LEFT)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sTotal%sHardpoints" % (panel, type), lbl)
                box.Add(lbl, 0, wx.ALIGN_LEFT)


        # Calibration points
        sizerHardResources.Add(bitmapLoader.getStaticBitmap("calibration_big", self.fullPanel, "icons"))

        box = wx.BoxSizer(wx.HORIZONTAL)
        sizerHardResources.Add(box, 0, wx.ALIGN_CENTER)

        self.labelAvailableCalibrationPoints = wx.StaticText(self.fullPanel, wx.ID_ANY, "0")
        box.Add(self.labelAvailableCalibrationPoints, 0, wx.ALIGN_LEFT)

        box.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "/"), 0, wx.ALIGN_LEFT)

        self.labelTotalCalibrationPoints = wx.StaticText(self.fullPanel, wx.ID_ANY, "0")
        box.Add(self.labelTotalCalibrationPoints, 0, wx.ALIGN_LEFT)

        sizerResources.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY, style=wx.VERTICAL), 0, wx.EXPAND)

        #PG, Cpu & drone stuff
        for group in (("cpu", "pg"), ("droneBay", "droneBandwidth")):
            main = wx.BoxSizer(wx.VERTICAL)
            sizerResources.Add(main, 0, wx.ALIGN_CENTER)
            for type in group:
                capitalizedType = type[0].capitalize() + type[1:]

                base = wx.BoxSizer(wx.HORIZONTAL)
                main.Add(base, 0, wx.EXPAND)

                base.Add(bitmapLoader.getStaticBitmap(type + "_big", self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)

                stats = wx.BoxSizer(wx.VERTICAL)
                base.Add(stats, 0, wx.EXPAND)

                absolute =  wx.BoxSizer(wx.HORIZONTAL)
                stats.Add(absolute)

                lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0")
                setattr(self, "labelAvailable%s" % capitalizedType, lbl)
                absolute.Add(lbl, 0, wx.ALIGN_CENTER)

                absolute.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "/"), 0, wx.ALIGN_CENTER)

                lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0")
                setattr(self, "labelTotal%s" % capitalizedType, lbl)
                absolute.Add(lbl, 0, wx.ALIGN_CENTER)

                gauge = wx.Gauge(self.fullPanel, wx.ID_ANY, 100)
                gauge.SetMinSize((100, -1))
                setattr(self, "gauge%s" % capitalizedType, gauge)
                stats.Add(gauge)

            if "cpu" in group:
                sizerResources.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY, style=wx.VERTICAL), 0, wx.ALIGN_CENTER)

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

        for tankType in ("damagePattern", "shield", "armor", "hull"):
            sizerResistances.Add(bitmapLoader.getStaticBitmap("%s_big" % tankType, self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)

            for damageType in ("em", "thermal", "kinetic", "explosive"):
                box = wx.BoxSizer(wx.HORIZONTAL)
                sizerResistances.Add(box, 1, wx.ALIGN_CENTER)

                lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.00")
                setattr(self, "labelResistance%s%s" % (tankType, damageType), lbl)
                box.Add(lbl, 0, wx.ALIGN_CENTER)

                box.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "%"), 0, wx.ALIGN_CENTER)


            lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0" if tankType != "damagePattern" else "")

            setattr(self, "labelResistance%sEhp" % tankType, lbl)
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
                    tankTypeCap = tankType[0].capitalize() + tankType[1:]
                    lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.0")
                    setattr(self, "labelTank%s%s" % (stability.capitalize(), tankTypeCap), lbl)

                    box = wx.BoxSizer(wx.HORIZONTAL)
                    box.Add(lbl, 1, wx.ALIGN_CENTER)
                    box.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, " HP/s"), 0, wx.ALIGN_CENTER)

                    sizerTankStats.Add(box, 1, wx.ALIGN_CENTER)

        # Firepower
        sizerHeaderFirepower = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderFirepower, 0, wx.EXPAND | wx.LEFT, 3)

        labelFirepower = wx.StaticText(self.fullPanel, wx.ID_ANY, "Firepower")
        labelFirepower.SetFont(boldFont)

        sizerHeaderFirepower.Add(labelFirepower, 0, wx.ALIGN_CENTER)
        sizerHeaderFirepower.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

        sizerFirepower = wx.FlexGridSizer(1, 3)
        for i in xrange(3):
            sizerFirepower.AddGrowableCol(i)

        self.sizerBase.Add(sizerFirepower, 0, wx.EXPAND | wx.LEFT, 3)

        for damageType, image in (("weapon", "turret") , ("drone", "droneBay")):
            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            sizerFirepower.Add(baseBox, 0, wx.ALIGN_CENTER)

            baseBox.Add(bitmapLoader.getStaticBitmap("%s_big" % image, self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)

            box = wx.BoxSizer(wx.VERTICAL)
            baseBox.Add(box, 0, wx.ALIGN_CENTER)

            box.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, damageType.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 1, wx.ALIGN_CENTER)

            lbl = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.0")
            setattr(self, "labelDps%s" % damageType, lbl)

            hbox.Add(lbl, 0, wx.ALIGN_CENTER)
            hbox.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, " DPS"), 0, wx.ALIGN_CENTER)

        baseBox = wx.BoxSizer(wx.HORIZONTAL)
        sizerFirepower.Add(baseBox, 0, wx.ALIGN_CENTER)

        baseBox.Add(bitmapLoader.getStaticBitmap("volley_big", self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)

        box = wx.BoxSizer(wx.VERTICAL)
        baseBox.Add(box, 1, wx.ALIGN_CENTER)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 1, wx.ALIGN_LEFT)

        self.labelVolleyTotal = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.0")
        hbox.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "Volley: "), 0, wx.ALIGN_LEFT)
        hbox.Add(self.labelVolleyTotal, 0, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 1, wx.ALIGN_CENTER)

        self.labelDpsTotal = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.0")
        hbox.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "Total DPS: "), 0, wx.ALIGN_LEFT)
        hbox.Add(self.labelDpsTotal, 0, wx.ALIGN_CENTER)

        # Capacitor
        sizerHeaderCapacitor = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(sizerHeaderCapacitor, 0, wx.EXPAND | wx.LEFT, 3)

        labelCapacitor = wx.StaticText(self.fullPanel, wx.ID_ANY, "Capacitor")
        labelCapacitor.SetFont(boldFont)

        sizerHeaderCapacitor.Add(labelCapacitor, 0, wx.ALIGN_CENTER)
        sizerHeaderCapacitor.Add(wx.StaticLine(self.fullPanel, wx.ID_ANY), 1, wx.ALIGN_CENTER)

        sizerCapacitor = wx.GridSizer(1, 2)
        self.sizerBase.Add(sizerCapacitor, 0, wx.EXPAND  | wx.LEFT, 3)

        # Capacitor capacity and time
        baseBox = wx.BoxSizer(wx.HORIZONTAL)
        sizerCapacitor.Add(baseBox, 1, wx.ALIGN_CENTER)

        baseBox.Add(bitmapLoader.getStaticBitmap("capacitorInfo_big", self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)

        box = wx.BoxSizer(wx.VERTICAL)
        baseBox.Add(box, 0, wx.ALIGN_CENTER)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 1, wx.ALIGN_CENTER)

        hbox.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "Capacity: "), 0, wx.ALIGN_CENTER)
        self.labelCapacitorCapacity = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.0")
        hbox.Add(self.labelCapacitorCapacity, 0, wx.ALIGN_CENTER)
        hbox.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, " GJ"), 0, wx.ALIGN_CENTER)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 1, wx.ALIGN_LEFT)

        hbox.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "Lasts "), 0, wx.ALIGN_LEFT)
        self.labelCapacitorTime = wx.StaticText(self.fullPanel, wx.ID_ANY, "0s")
        hbox.Add(self.labelCapacitorTime, 0, wx.ALIGN_LEFT)

        # Capacitor balance
        baseBox = wx.BoxSizer(wx.HORIZONTAL)
        sizerCapacitor.Add(baseBox, 1, wx.ALIGN_CENTER)

        baseBox.Add(bitmapLoader.getStaticBitmap("capacitorRecharge_big", self.fullPanel, "icons"), 0, wx.ALIGN_CENTER)

        box = wx.BoxSizer(wx.VERTICAL)
        baseBox.Add(box, 0, wx.ALIGN_CENTER)

        # Recharge
        chargeSizer = wx.FlexGridSizer(2, 3)
        box.Add(chargeSizer)

        chargeSizer.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "+ "), 0, wx.ALIGN_CENTER)
        self.labelCapacitorRecharge = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.0")
        chargeSizer.Add(self.labelCapacitorRecharge, 0, wx.ALIGN_CENTER)
        chargeSizer.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, " GJ/s"), 0, wx.ALIGN_CENTER)

        # Discharge
        chargeSizer.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, "- "), 0, wx.ALIGN_CENTER)
        self.labelCapacitorDischarge = wx.StaticText(self.fullPanel, wx.ID_ANY, "0.0")
        chargeSizer.Add(self.labelCapacitorDischarge, 0, wx.ALIGN_CENTER)
        chargeSizer.Add(wx.StaticText(self.fullPanel, wx.ID_ANY, " GJ/s"), 0, wx.ALIGN_CENTER)

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
            setattr(self, "label%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lblUnit = wx.StaticText(self.fullPanel, wx.ID_ANY, " %s" % unit)
            setattr(self, "labelUnit%s" % labelShort, lblUnit)
            box.Add(lblUnit, 0, wx.ALIGN_LEFT)

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
