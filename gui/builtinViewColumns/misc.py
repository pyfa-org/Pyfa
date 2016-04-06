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


import gui.mainFrame
from gui.viewColumn import ViewColumn
from gui.bitmapLoader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from gui.utils.listFormatter import formatList
from service.fit import Fit, Market

import wx

class Miscellanea(ViewColumn):
    name = "Miscellanea"
    def __init__(self, fittingView, params = None):
        if params == None:
            params = {"showIcon": True,
                      "displayName": False}
        ViewColumn.__init__(self, fittingView)
        if params["showIcon"]:
            self.imageId = fittingView.imageList.GetImageIndex("column_misc", "gui")
            self.bitmap = BitmapLoader.getBitmap("column_misc", "gui")
            self.mask = wx.LIST_MASK_IMAGE
        else:
            self.imageId = -1

        if params["displayName"] or self.imageId == -1:
            self.columnText = "Misc data"
            self.mask |= wx.LIST_MASK_TEXT
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getText(self, stuff):
        text = self.__getData(stuff)[0]
        return text

    def getToolTip(self, mod):
        text = self.__getData(mod)[1]
        return text

    def getImageId(self, mod):
        return -1

    def getParameters(self):
        return (("displayName", bool, False),
                ("showIcon", bool, True))

    def __getData(self, stuff):
        item = stuff.item
        if item is None:
            return "", None
        itemGroup = item.group.name
        itemCategory = item.category.name

        if itemGroup == "Ship Modifiers":
            return "", None
        elif itemGroup in ("Energy Weapon", "Hybrid Weapon", "Projectile Weapon", "Combat Drone", "Fighter Drone"):
            trackingSpeed = stuff.getModifiedItemAttr("trackingSpeed")
            if not trackingSpeed:
                return "", None
            text = "{0}".format(formatAmount(trackingSpeed, 3, 0, 3))
            tooltip = "Tracking speed"
            return text, tooltip
        elif itemCategory == "Subsystem":
            slots = ("hi", "med", "low")
            info = []
            for slot in slots:
                n = int(stuff.getModifiedItemAttr("%sSlotModifier"%slot))
                if n > 0:
                    info.append("{0}{1}".format(n, slot[0].upper()))
            return "+ "+", ".join(info), "Slot Modifiers"
        elif itemGroup == "Energy Neutralizer":
            neutAmount = stuff.getModifiedItemAttr("energyDestabilizationAmount")
            cycleTime = stuff.cycleTime
            if not neutAmount or not cycleTime:
                return "", None
            capPerSec = float(-neutAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(capPerSec, 3, 0, 3))
            tooltip = "Energy neutralization per second"
            return text, tooltip
        elif itemGroup == "Energy Nosferatu":
            neutAmount = stuff.getModifiedItemAttr("powerTransferAmount")
            cycleTime = stuff.cycleTime
            if not neutAmount or not cycleTime:
                return "", None
            capPerSec = float(-neutAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(capPerSec, 3, 0, 3))
            tooltip = "Energy neutralization per second"
            return text, tooltip
        elif itemGroup == "Salvager":
            chance = stuff.getModifiedItemAttr("accessDifficultyBonus")
            if not chance:
                return "", None
            text = "{0}%".format(formatAmount(chance, 3, 0, 3))
            tooltip = "Item retrieval chance"
            return text, tooltip
        elif itemGroup == "Data Miners":
            strength = stuff.getModifiedItemAttr("virusStrength")
            coherence = stuff.getModifiedItemAttr("virusCoherence")
            if not strength or not coherence:
                return "", None
            text = "{0} | {1}".format(formatAmount(strength, 3, 0, 3), formatAmount(coherence, 3, 0, 3))
            tooltip = "Virus strength and coherence"
            return text, tooltip
        elif itemGroup in ("Warp Scrambler", "Warp Core Stabilizer"):
            scramStr = stuff.getModifiedItemAttr("warpScrambleStrength")
            if not scramStr:
                return "", None
            text = "{0}".format(formatAmount(-scramStr, 3, 0, 3, forceSign=True))
            tooltip = "Warp core strength modification"
            return text, tooltip
        elif itemGroup in ("Stasis Web", "Stasis Webifying Drone"):
            speedFactor = stuff.getModifiedItemAttr("speedFactor")
            if not speedFactor:
                return "", None
            text = "{0}%".format(formatAmount(speedFactor, 3, 0, 3))
            tooltip = "Speed reduction"
            return text, tooltip
        elif itemGroup == "Target Painter":
            sigRadBonus = stuff.getModifiedItemAttr("signatureRadiusBonus")
            if not sigRadBonus:
                return "", None
            text = "{0}%".format(formatAmount(sigRadBonus, 3, 0, 3, forceSign=True))
            tooltip = "Signature radius increase"
            return text, tooltip
        elif itemGroup == "Sensor Dampener":
            lockRangeBonus = stuff.getModifiedItemAttr("maxTargetRangeBonus")
            scanResBonus = stuff.getModifiedItemAttr("scanResolutionBonus")
            if lockRangeBonus is None or scanResBonus is None:
                return "", None
            display = 0
            for bonus in (lockRangeBonus, scanResBonus):
                if abs(bonus) > abs(display):
                    display = bonus
            if not display:
                return "", None
            text = "{0}%".format(formatAmount(display, 3, 0, 3, forceSign=True))
            ttEntries = []
            if display == lockRangeBonus:
                ttEntries.append("lock range")
            if display == scanResBonus:
                ttEntries.append("scan resolution")
            tooltip = "{0} dampening".format(formatList(ttEntries)).capitalize()
            return text, tooltip
        elif itemGroup == "Weapon Disruptor":
            # Weapon disruption now covers both tracking and guidance (missile) disruptors
            # First get the attributes for tracking disruptors
            optimalRangeBonus = stuff.getModifiedItemAttr("maxRangeBonus")
            falloffRangeBonus = stuff.getModifiedItemAttr("falloffBonus")
            trackingSpeedBonus = stuff.getModifiedItemAttr("trackingSpeedBonus")

            trackingDisruptorAttributes = {
                "optimal range": optimalRangeBonus,
                "falloff range": falloffRangeBonus,
                "tracking speed": trackingSpeedBonus}

            isTrackingDisruptor = any(map(lambda x: x is not None and x != 0, trackingDisruptorAttributes.values()))

            # Then get the attributes for guidance disruptors
            explosionVelocityBonus = stuff.getModifiedItemAttr("aoeVelocityBonus")
            explosionRadiusBonus = stuff.getModifiedItemAttr("aoeCloudSizeBonus")

            flightTimeBonus = stuff.getModifiedItemAttr("explosionDelayBonus")
            missileVelocityBonus = stuff.getModifiedItemAttr("missileVelocityBonus")

            guidanceDisruptorAttributes = {
                "explosion velocity": explosionVelocityBonus,
                "explosion radius": explosionRadiusBonus,
                "flight time": flightTimeBonus,
                "missile velocity": missileVelocityBonus}

            isGuidanceDisruptor = any(map(lambda x: x is not None and x != 0, guidanceDisruptorAttributes.values()))

            if isTrackingDisruptor:
                attributes = trackingDisruptorAttributes
            elif isGuidanceDisruptor:
                attributes = guidanceDisruptorAttributes
            else:
                return "", None

            display = max(attributes.values(), key=lambda x: abs(x))

            text = "{0}%".format(formatAmount(display, 3, 0, 3, forceSign=True))

            ttEntries = []
            for attributeName, attributeValue in attributes.items():
                if attributeValue == display:
                    ttEntries.append(attributeName)

            tooltip = "{0} disruption".format(formatList(ttEntries)).capitalize()
            return text, tooltip
        elif itemGroup in ("ECM", "Burst Jammer", "Burst Projectors"):
            grav = stuff.getModifiedItemAttr("scanGravimetricStrengthBonus")
            ladar = stuff.getModifiedItemAttr("scanLadarStrengthBonus")
            radar = stuff.getModifiedItemAttr("scanRadarStrengthBonus")
            magnet = stuff.getModifiedItemAttr("scanMagnetometricStrengthBonus")
            if grav is None or ladar is None or radar is None or magnet is None:
                return "", None
            display = max(grav, ladar, radar, magnet)
            if not display:
                return "", None
            text = "{0}".format(formatAmount(display, 3, 0, 3))
            ttEntries = []
            if display == grav:
                ttEntries.append("gravimetric")
            if display == ladar:
                ttEntries.append("ladar")
            if display == magnet:
                ttEntries.append("magnetometric")
            if display == radar:
                ttEntries.append("radar")
            plu = "" if len(ttEntries) == 1 else "s"
            tooltip = "{0} strength{1}".format(formatList(ttEntries), plu).capitalize()
            return text, tooltip
        elif itemGroup in ("Remote Sensor Booster", "Sensor Booster", "Signal Amplifier"):
            scanResBonus = stuff.getModifiedItemAttr("scanResolutionBonus")
            lockRangeBonus = stuff.getModifiedItemAttr("maxTargetRangeBonus")
            if scanResBonus is None or lockRangeBonus is None:
                return "", None
            display = 0
            for bonus in (scanResBonus, lockRangeBonus):
                if abs(bonus) > abs(display):
                    display = bonus
            if not display:
                return "", None
            text = "{0}%".format(formatAmount(display, 3, 0, 3, forceSign=True))
            ttEntries = []
            if display == lockRangeBonus:
                ttEntries.append("lock range")
            if display == scanResBonus:
                ttEntries.append("scan resolution")
            tooltip = "{0} bonus".format(formatList(ttEntries)).capitalize()
            return text, tooltip
        elif itemGroup in ("Projected ECCM", "ECCM", "Sensor Backup Array"):
            grav = stuff.getModifiedItemAttr("scanGravimetricStrengthPercent")
            ladar = stuff.getModifiedItemAttr("scanLadarStrengthPercent")
            radar = stuff.getModifiedItemAttr("scanRadarStrengthPercent")
            magnet = stuff.getModifiedItemAttr("scanMagnetometricStrengthPercent")
            if grav is None or ladar is None or radar is None or magnet is None:
                return "", None
            display = max(grav, ladar, radar, magnet)
            if not display:
                return "", None
            text = "{0}%".format(formatAmount(display, 3, 0, 3, forceSign=True))
            ttEntries = []
            if display == grav:
                ttEntries.append("gravimetric")
            if display == ladar:
                ttEntries.append("ladar")
            if display == magnet:
                ttEntries.append("magnetometric")
            if display == radar:
                ttEntries.append("radar")
            plu = "" if len(ttEntries) == 1 else "s"
            tooltip = "{0} strength{1} bonus".format(formatList(ttEntries), plu).capitalize()
            return text, tooltip
        elif itemGroup == "Cloaking Device":
            recalibration = stuff.getModifiedItemAttr("cloakingTargetingDelay")
            if recalibration is None:
                return "", None
            text = "{0}s".format(formatAmount(float(recalibration)/1000, 3, 0, 3))
            tooltip = "Sensor recalibration time"
            return text, tooltip
        elif itemGroup == "Remote Armor Repairer":
            repAmount = stuff.getModifiedItemAttr("armorDamageAmount")
            cycleTime = stuff.getModifiedItemAttr("duration")
            if not repAmount or not cycleTime:
                return "", None
            repPerSec = float(repAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(repPerSec, 3, 0, 3, forceSign=True))
            tooltip = "Armor repaired per second"
            return text, tooltip
        elif itemGroup == "Remote Shield Booster":
            repAmount = stuff.getModifiedItemAttr("shieldBonus")
            cycleTime = stuff.cycleTime
            if not repAmount or not cycleTime:
                return "", None
            repPerSec = float(repAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(repPerSec, 3, 0, 3, forceSign=True))
            tooltip = "Shield transferred per second"
            return text, tooltip
        elif itemGroup == "Remote Capacitor Transmitter":
            repAmount = stuff.getModifiedItemAttr("powerTransferAmount")
            cycleTime = stuff.cycleTime
            if not repAmount or not cycleTime:
                return "", None
            repPerSec = float(repAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(repPerSec, 3, 0, 3, forceSign=True))
            tooltip = "Energy transferred per second"
            return text, tooltip
        elif itemGroup == "Remote Hull Repairer":
            repAmount = stuff.getModifiedItemAttr("structureDamageAmount")
            cycleTime = stuff.cycleTime
            if not repAmount or not cycleTime:
                return "", None
            repPerSec = float(repAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(repPerSec, 3, 0, 3, forceSign=True))
            tooltip = "Structure repaired per second"
            return text, tooltip
        elif itemGroup == "Gang Coordinator":
            command = stuff.getModifiedItemAttr("commandBonus") or stuff.getModifiedItemAttr("commandBonusHidden")
            if not command:
                return "", None
            text = "{0}%".format(formatAmount(command, 3, 0, 3, forceSign=True))
            tooltip = "Gang bonus strength"
            return text, tooltip
        elif itemGroup == "Electronic Warfare Drone":
            sigRadBonus = stuff.getModifiedItemAttr("signatureRadiusBonus")
            lockRangeMult = stuff.getModifiedItemAttr("maxTargetRangeMultiplier")
            scanResMult = stuff.getModifiedItemAttr("scanResolutionMultiplier")
            falloffRangeMult = stuff.getModifiedItemAttr("fallofMultiplier")
            optimalRangeMult = stuff.getModifiedItemAttr("maxRangeMultiplier")
            trackingSpeedMult = stuff.getModifiedItemAttr("trackingSpeedMultiplier")
            grav = stuff.getModifiedItemAttr("scanGravimetricStrengthBonus")
            ladar = stuff.getModifiedItemAttr("scanLadarStrengthBonus")
            radar = stuff.getModifiedItemAttr("scanRadarStrengthBonus")
            magnet = stuff.getModifiedItemAttr("scanMagnetometricStrengthBonus")
            if sigRadBonus:
                text = "{0}%".format(formatAmount(sigRadBonus, 3, 0, 3, forceSign=True))
                tooltip = "Signature radius increase"
                return text, tooltip
            if lockRangeMult is not None and scanResMult is not None:
                lockRangeBonus = (lockRangeMult - 1) * 100
                scanResBonus = (scanResMult - 1) * 100
                display = 0
                for bonus in (lockRangeBonus, scanResBonus):
                    if abs(bonus) > abs(display):
                        display = bonus
                if not display:
                    return "", None
                text = "{0}%".format(formatAmount(display, 3, 0, 3, forceSign=True))
                ttEntries = []
                if display == lockRangeBonus:
                    ttEntries.append("lock range")
                if display == scanResBonus:
                    ttEntries.append("scan resolution")
                tooltip = "{0} dampening".format(formatList(ttEntries)).capitalize()
                return text, tooltip
            if falloffRangeMult is not None and optimalRangeMult is not None and trackingSpeedMult is not None:
                falloffRangeBonus = (falloffRangeMult - 1) * 100
                optimalRangeBonus = (optimalRangeMult - 1) * 100
                trackingSpeedBonus = (trackingSpeedMult - 1) * 100
                display = 0
                for bonus in (falloffRangeBonus, optimalRangeBonus, trackingSpeedBonus):
                    if abs(bonus) > abs(display):
                        display = bonus
                if not display:
                    return "", None
                text = "{0}%".format(formatAmount(display, 3, 0, 3), forceSign=True)
                ttEntries = []
                if display == optimalRangeBonus:
                    ttEntries.append("optimal range")
                if display == falloffRangeBonus:
                    ttEntries.append("falloff range")
                if display == trackingSpeedBonus:
                    ttEntries.append("tracking speed")
                tooltip = "{0} disruption".format(formatList(ttEntries)).capitalize()
                return text, tooltip
            if grav is not None and ladar is not None and radar is not None and magnet is not None:
                display = max(grav, ladar, radar, magnet)
                if not display:
                    return "", None
                text = "{0}".format(formatAmount(display, 3, 0, 3))
                ttEntries = []
                if display == grav:
                    ttEntries.append("gravimetric")
                if display == ladar:
                    ttEntries.append("ladar")
                if display == magnet:
                    ttEntries.append("magnetometric")
                if display == radar:
                    ttEntries.append("radar")
                plu = "" if len(ttEntries) == 1 else "s"
                tooltip = "{0} strength{1}".format(formatList(ttEntries), plu).capitalize()
                return text, tooltip
            else:
                return "", None
        elif itemGroup == "Fighter Bomber":
            optimalSig = stuff.getModifiedItemAttr("optimalSigRadius")
            if not optimalSig:
                return "", None
            text = "{0}m".format(formatAmount(optimalSig, 3, 0, 3))
            tooltip = "Optimal signature radius"
            return text, tooltip
        elif itemGroup in ("Frequency Mining Laser", "Strip Miner", "Mining Laser", "Gas Cloud Harvester"):
            miningAmount = stuff.getModifiedItemAttr("specialtyMiningAmount") or stuff.getModifiedItemAttr("miningAmount")
            cycleTime = stuff.cycleTime
            if not miningAmount or not cycleTime:
                return "", None
            minePerSec = float(miningAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(minePerSec, 3, 0, 3))
            tooltip = "Yield per second"
            return text, tooltip
        elif itemGroup == "Logistic Drone":
            armorAmount = stuff.getModifiedItemAttr("armorDamageAmount")
            shieldAmount = stuff.getModifiedItemAttr("shieldBonus")
            hullAmount = stuff.getModifiedItemAttr("structureDamageAmount")
            repAmount = armorAmount or shieldAmount or hullAmount
            cycleTime = stuff.getModifiedItemAttr("duration")
            if not repAmount or not cycleTime:
                return "", None
            repPerSec = float(repAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(repPerSec, 3, 0, 3))
            ttEntries = []
            if hullAmount is not None and repAmount == hullAmount:
                ttEntries.append("structure")
            if armorAmount is not None and repAmount == armorAmount:
                ttEntries.append("armor")
            if shieldAmount is not None and repAmount == shieldAmount:
                ttEntries.append("shield")
            tooltip = "{0} repaired per second".format(formatList(ttEntries)).capitalize()
            return text, tooltip
        elif itemGroup == "Energy Neutralizer Drone":
            neutAmount = stuff.getModifiedItemAttr("energyDestabilizationAmount")
            cycleTime = stuff.getModifiedItemAttr("duration")
            if not neutAmount or not cycleTime:
                return "", None
            capPerSec = float(-neutAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(capPerSec, 3, 0, 3))
            tooltip = "Energy neutralization per second"
            return text, tooltip
        elif itemGroup == "Mining Drone":
            miningAmount = stuff.getModifiedItemAttr("miningAmount")
            cycleTime = stuff.getModifiedItemAttr("duration")
            if not miningAmount or not cycleTime:
                return "", None
            minePerSec = float(miningAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(minePerSec, 3, 0, 3))
            tooltip = "Yield per second"
            return text, tooltip
        elif itemGroup == "Micro Jump Drive":
            cycleTime = stuff.getModifiedItemAttr("duration") / 1000
            text = "{0}s".format(cycleTime)
            tooltip = "Spoolup time"
            return text, tooltip
        elif itemGroup in ("Siege Module", "Cynosural Field"):
            amt = stuff.getModifiedItemAttr("consumptionQuantity")
            if amt:
                typeID = stuff.getModifiedItemAttr("consumptionType")
                item = Market.getInstance().getItem(typeID)
                text = "{0} units".format(formatAmount(amt, 3, 0, 3))
                return text, item.name
            else:
                return "", None
        elif itemGroup in ("Ancillary Armor Repairer", "Ancillary Shield Booster"):
            hp = stuff.hpBeforeReload
            cycles = stuff.numShots
            cycleTime = stuff.rawCycleTime
            if not hp or not cycleTime or not cycles:
                return "", None
            fit = Fit.getInstance().getFit(self.mainFrame.getActiveFit())
            ehpTotal = fit.ehp
            hpTotal = fit.hp
            useEhp = self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective
            tooltip = "HP restored over duration using charges"
            if useEhp:
                if itemGroup == "Ancillary Armor Repairer":
                    hpRatio = ehpTotal["armor"] / hpTotal["armor"]
                else:
                    hpRatio = ehpTotal["shield"] / hpTotal["shield"]
                tooltip = "E{0}".format(tooltip)
            else:
                hpRatio = 1
            ehp = hp * hpRatio
            duration = cycles * cycleTime / 1000
            text = "{0} / {1}s".format(formatAmount(ehp, 3, 0, 9), formatAmount(duration, 3, 0, 3))

            return text, tooltip
        elif stuff.charge is not None:
            chargeGroup = stuff.charge.group.name
            if chargeGroup in ("Rocket", "Advanced Rocket", "Light Missile", "Advanced Light Missile", "FoF Light Missile",
                               "Heavy Assault Missile", "Advanced Heavy Assault Missile", "Heavy Missile", "Advanced Heavy Missile", "FoF Heavy Missile",
                               "Torpedo", "Advanced Torpedo", "Cruise Missile", "Advanced Cruise Missile", "FoF Cruise Missile",
                               "XL Torpedo", "XL Cruise Missile"):
                cloudSize = stuff.getModifiedChargeAttr("aoeCloudSize")
                aoeVelocity = stuff.getModifiedChargeAttr("aoeVelocity")
                if not cloudSize or not aoeVelocity:
                    return "", None
                text = "{0}{1} | {2}{3}".format(formatAmount(cloudSize, 3, 0, 3), "m",
                                                formatAmount(aoeVelocity, 3, 0, 3), "m/s")
                tooltip = "Explosion radius and explosion velocity"
                return text, tooltip
            elif chargeGroup == "Bomb":
                cloudSize = stuff.getModifiedChargeAttr("aoeCloudSize")
                if not cloudSize:
                    return "", None
                text = "{0}{1}".format(formatAmount(cloudSize, 3, 0, 3), "m")
                tooltip = "Explosion radius"
                return text, tooltip
            elif chargeGroup in ("Scanner Probe",):
                scanStr = stuff.getModifiedChargeAttr("baseSensorStrength")
                baseRange = stuff.getModifiedChargeAttr("baseScanRange")
                if not scanStr or not baseRange:
                    return "", None
                strTwoAu = scanStr / (2.0 / baseRange)
                text = "{0}".format(formatAmount(strTwoAu, 3, 0, 3))
                tooltip = "Scan strength with 2 AU scan range"
                return text, tooltip
            else:
                return "", None
        else:
            return "", None

Miscellanea.register()
