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
from gui.utils.numberFormatter import formatAmount

try:
    from collections import OrderedDict
except ImportError:
    from utils.compat import OrderedDict


class TargetingMiscViewMinimal(StatsView):
    name = "targetingMiscViewMinimal"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []

    def getHeaderText(self, fit):
        return "Targeting && Misc"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()

        self.panel = contentPanel
        self.headerPanel = headerPanel
        gridTargetingMisc = wx.FlexGridSizer(1, 3)
        contentSizer.Add(gridTargetingMisc, 0, wx.EXPAND | wx.ALL, 0)
        gridTargetingMisc.AddGrowableCol(0)
        gridTargetingMisc.AddGrowableCol(2)
        # Targeting

        gridTargeting = wx.FlexGridSizer(5, 2)
        gridTargeting.AddGrowableCol(1)

        gridTargetingMisc.Add(gridTargeting, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        labels = (("Targets", "Targets", ""),
                  ("Range", "Range", "km"),
                  ("Scan res.", "ScanRes", "mm"),
                  ("Sensor str.", "SensorStr", ""),
                  ("Drone range", "CtrlRange", "km"))

        for header, labelShort, unit in labels:
            gridTargeting.Add(wx.StaticText(contentPanel, wx.ID_ANY, "%s: " % header), 0, wx.ALIGN_LEFT)

            box = wx.BoxSizer(wx.HORIZONTAL)
            gridTargeting.Add(box, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0 %s" % unit)
            setattr(self, "label%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            self._cachedValues.append({"main": 0})

        # Misc
        gridTargetingMisc.Add(wx.StaticLine(contentPanel, wx.ID_ANY, style=wx.VERTICAL), 0, wx.EXPAND, 3)
        gridMisc = wx.FlexGridSizer(5, 2)
        gridMisc.AddGrowableCol(1)
        gridTargetingMisc.Add(gridMisc, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        labels = (("Speed", "Speed", "m/s"),
                  ("Align time", "AlignTime", "s"),
                  ("Signature", "SigRadius", "m"),
                  ("Warp Speed", "WarpSpeed", "AU/s"),
                  ("Cargo", "Cargo", u"m\u00B3"))

        for header, labelShort, unit in labels:
            gridMisc.Add(wx.StaticText(contentPanel, wx.ID_ANY, "%s: " % header), 0, wx.ALIGN_LEFT)

            box = wx.BoxSizer(wx.HORIZONTAL)
            gridMisc.Add(box, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0 %s" % unit)
            setattr(self, "labelFull%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            self._cachedValues.append({"main": 0})

    def refreshPanel(self, fit):
        # If we did anything interesting, we'd update our labels to reflect the new fit's stats here

        cargoNamesOrder = OrderedDict((
            ("fleetHangarCapacity", "Fleet hangar"),
            ("shipMaintenanceBayCapacity", "Maintenance bay"),
            ("specialAmmoHoldCapacity", "Ammo hold"),
            ("specialFuelBayCapacity", "Fuel bay"),
            ("specialShipHoldCapacity", "Ship hold"),
            ("specialSmallShipHoldCapacity", "Small ship hold"),
            ("specialMediumShipHoldCapacity", "Medium ship hold"),
            ("specialLargeShipHoldCapacity", "Large ship hold"),
            ("specialIndustrialShipHoldCapacity", "Industrial ship hold"),
            ("specialOreHoldCapacity", "Ore hold"),
            ("specialMineralHoldCapacity", "Mineral hold"),
            ("specialMaterialBayCapacity", "Material bay"),
            ("specialGasHoldCapacity", "Gas hold"),
            ("specialSalvageHoldCapacity", "Salvage hold"),
            ("specialCommandCenterHoldCapacity", "Command center hold"),
            ("specialPlanetaryCommoditiesHoldCapacity", "Planetary goods hold"),
            ("specialQuafeHoldCapacity", "Quafe hold")
        ))

        cargoValues = {
            "main": lambda: fit.ship.getModifiedItemAttr("capacity"),
            "fleetHangarCapacity": lambda: fit.ship.getModifiedItemAttr("fleetHangarCapacity"),
            "shipMaintenanceBayCapacity": lambda: fit.ship.getModifiedItemAttr("shipMaintenanceBayCapacity"),
            "specialAmmoHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialAmmoHoldCapacity"),
            "specialFuelBayCapacity": lambda: fit.ship.getModifiedItemAttr("specialFuelBayCapacity"),
            "specialShipHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialShipHoldCapacity"),
            "specialSmallShipHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialSmallShipHoldCapacity"),
            "specialMediumShipHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialMediumShipHoldCapacity"),
            "specialLargeShipHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialLargeShipHoldCapacity"),
            "specialIndustrialShipHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialIndustrialShipHoldCapacity"),
            "specialOreHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialOreHoldCapacity"),
            "specialMineralHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialMineralHoldCapacity"),
            "specialMaterialBayCapacity": lambda: fit.ship.getModifiedItemAttr("specialMaterialBayCapacity"),
            "specialGasHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialGasHoldCapacity"),
            "specialSalvageHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialSalvageHoldCapacity"),
            "specialCommandCenterHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialCommandCenterHoldCapacity"),
            "specialPlanetaryCommoditiesHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialPlanetaryCommoditiesHoldCapacity"),
            "specialQuafeHoldCapacity": lambda: fit.ship.getModifiedItemAttr("specialQuafeHoldCapacity")
        }

        stats = (("labelTargets", {"main": lambda: fit.maxTargets}, 3, 0, 0, ""),
                 ("labelRange", {"main": lambda: fit.maxTargetRange / 1000}, 3, 0, 0, "km"),
                 ("labelScanRes", {"main": lambda: fit.ship.getModifiedItemAttr("scanResolution")}, 3, 0, 0, "mm"),
                 ("labelSensorStr", {"main": lambda: fit.scanStrength}, 3, 0, 0, ""),
                 ("labelCtrlRange", {"main": lambda: fit.extraAttributes["droneControlRange"] / 1000}, 3, 0, 0, "km"),
                 ("labelFullSpeed", {"main": lambda: fit.maxSpeed}, 3, 0, 0, "m/s"),
                 ("labelFullAlignTime", {"main": lambda: fit.alignTime}, 3, 0, 0, "s"),
                 ("labelFullSigRadius", {"main": lambda: fit.ship.getModifiedItemAttr("signatureRadius")}, 3, 0, 9, ""),
                 ("labelFullWarpSpeed", {"main": lambda: fit.warpSpeed}, 3, 0, 0, "AU/s"),
                 ("labelFullCargo", cargoValues, 4, 0, 9, u"m\u00B3"))

        counter = 0
        RADII = [("Pod", 25), ("Interceptor", 33), ("Frigate", 38),
                 ("Destroyer", 83), ("Cruiser", 130),
                 ("Battlecruiser", 265), ("Battleship", 420),
                 ("Carrier", 3000)]
        for labelName, valueDict, prec, lowest, highest, unit in stats:
            label = getattr(self, labelName)
            newValues = {}
            for valueAlias, value in valueDict.items():
                value = value() if fit is not None else 0
                value = value if value is not None else 0
                newValues[valueAlias] = value
            if self._cachedValues[counter] != newValues:
                mainValue = newValues["main"]
                otherValues = dict((k, newValues[k]) for k in filter(lambda k: k != "main", newValues))
                if labelName == "labelFullCargo":
                    # Get sum of all cargoholds except for maintenance bay
                    additionalCargo = sum(otherValues.values())
                    if additionalCargo > 0:
                        label.SetLabel("%s+%s %s" % (formatAmount(mainValue, prec, lowest, highest),
                                                     formatAmount(additionalCargo, prec, lowest, highest),
                                                     unit))
                    else:
                        label.SetLabel("%s %s" % (formatAmount(mainValue, prec, lowest, highest), unit))
                else:
                    label.SetLabel("%s %s" % (formatAmount(mainValue, prec, lowest, highest), unit))
                # Tooltip stuff
                if fit:
                    if labelName == "labelScanRes":
                        lockTime = "%s\n" % "Lock Times".center(30)
                        for size, radius in RADII:
                            left = "%.1fs" % fit.calculateLockTime(radius)
                            right = "%s [%d]" % (size, radius)
                            lockTime += "%5s\t%s\n" % (left, right)
                        label.SetToolTip(wx.ToolTip(lockTime))
                    elif labelName == "labelFullWarpSpeed":
                        maxWarpDistance = "Max Warp Distance: %.1f AU" % fit.maxWarpDistance
                        if fit.ship.getModifiedItemAttr("warpScrambleStatus"):
                            warpScrambleStatus = "Warp Core Strength: %.1f" % (fit.ship.getModifiedItemAttr("warpScrambleStatus") * -1)
                        else:
                            warpScrambleStatus = "Warp Core Strength: %.1f" % 0
                        label.SetToolTip(wx.ToolTip("%s\n%s" % (maxWarpDistance, warpScrambleStatus)))
                    elif labelName == "labelSensorStr":
                        if fit.jamChance > 0:
                            label.SetToolTip(wx.ToolTip("Type: %s\n%.1f%% Chance of Jam" % (fit.scanType, fit.jamChance)))
                        else:
                            label.SetToolTip(wx.ToolTip("Type: %s" % fit.scanType))
                    elif labelName == "labelFullAlignTime":
                        alignTime = "Align:\t%.3fs" % mainValue
                        mass = 'Mass:\t{:,.0f}kg'.format(fit.ship.getModifiedItemAttr("mass"))
                        agility = "Agility:\t%.3fx" % (fit.ship.getModifiedItemAttr("agility") or 0)
                        label.SetToolTip(wx.ToolTip("%s\n%s\n%s" % (alignTime, mass, agility)))
                    elif labelName == "labelFullCargo":
                        tipLines = [u"Cargohold: {:,.2f}m\u00B3 / {:,.2f}m\u00B3".format(fit.cargoBayUsed, newValues["main"])]
                        for attrName, tipAlias in cargoNamesOrder.items():
                            if newValues[attrName] > 0:
                                tipLines.append(u"{}: {:,.2f}m\u00B3".format(tipAlias, newValues[attrName]))
                        label.SetToolTip(wx.ToolTip(u"\n".join(tipLines)))
                    else:
                        label.SetToolTip(wx.ToolTip("%.1f" % mainValue))
                else:
                    label.SetToolTip(wx.ToolTip(""))
                self._cachedValues[counter] = newValues
            elif labelName == "labelFullWarpSpeed":
                if fit:
                    maxWarpDistance = "Max Warp Distance: %.1f AU" % fit.maxWarpDistance
                    if fit.ship.getModifiedItemAttr("warpScrambleStatus"):
                        warpScrambleStatus = "Warp Core Strength: %.1f" % (fit.ship.getModifiedItemAttr("warpScrambleStatus") * -1)
                    else:
                        warpScrambleStatus = "Warp Core Strength: %.1f" % 0
                    label.SetToolTip(wx.ToolTip("%s\n%s" % (maxWarpDistance, warpScrambleStatus)))
                else:
                    label.SetToolTip(wx.ToolTip(""))
            elif labelName == "labelSensorStr":
                if fit:
                    if fit.jamChance > 0:
                        label.SetToolTip(wx.ToolTip("Type: %s\n%.1f%% Chance of Jam" % (fit.scanType, fit.jamChance)))
                    else:
                        label.SetToolTip(wx.ToolTip("Type: %s" % fit.scanType))
                else:
                    label.SetToolTip(wx.ToolTip(""))
            elif labelName == "labelFullCargo":
                if fit:
                    cachedCargo = self._cachedValues[counter]
                    # if you add stuff to cargo, the capacity doesn't change and thus it is still cached
                    # This assures us that we force refresh of cargo tooltip
                    tipLines = [u"Cargohold: {:,.2f}m\u00B3 / {:,.2f}m\u00B3".format(fit.cargoBayUsed, cachedCargo["main"])]
                    for attrName, tipAlias in cargoNamesOrder.items():
                        if cachedCargo[attrName] > 0:
                            tipLines.append(u"{}: {:,.2f}m\u00B3".format(tipAlias, cachedCargo[attrName]))
                    label.SetToolTip(wx.ToolTip(u"\n".join(tipLines)))
                else:
                    label.SetToolTip(wx.ToolTip(""))

            # forces update of probe size, since this stat is used by both sig radius and sensor str
            if labelName == "labelFullSigRadius":
                if fit:
                    label.SetToolTip(wx.ToolTip("Probe Size: %.3f" % (fit.probeSize or 0)))
                else:
                    label.SetToolTip(wx.ToolTip(""))

            counter += 1
        self.panel.Layout()
        self.headerPanel.Layout()


TargetingMiscViewMinimal.register()
