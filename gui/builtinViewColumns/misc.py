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

from service.fit import Fit
from service.market import Market
import gui.mainFrame
from gui.viewColumn import ViewColumn
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from gui.utils.listFormatter import formatList
from eos.utils.spoolSupport import SpoolType, SpoolOptions
import eos.config


class Miscellanea(ViewColumn):
    name = "Miscellanea"

    def __init__(self, fittingView, params=None):
        if params is None:
            params = {"showIcon": True, "displayName": False}

        ViewColumn.__init__(self, fittingView)
        if params["showIcon"]:
            self.imageId = fittingView.imageList.GetImageIndex("column_misc", "gui")
            self.bitmap = BitmapLoader.getBitmap("column_misc", "gui")
            self.mask = wx.LIST_MASK_IMAGE
        else:
            self.imageId = -1

        if params["displayName"] or self.imageId == -1:
            self.columnText = _("Misc data")
            self.mask |= wx.LIST_MASK_TEXT
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.fittingView = fittingView

    def getText(self, stuff):
        return self.__getData(stuff)[0]

    def getToolTip(self, mod):
        return self.__getData(mod)[1]

    def getImageId(self, mod):
        return -1

    def getParameters(self):
        return ("displayName", bool, False), ("showIcon", bool, True)

    def __getData(self, stuff):
        item = stuff.item
        if item is None:
            return "", None
        itemGroup = item.group.name
        itemCategory = item.category.name

        if itemGroup == "Ship Modifiers":
            return "", None
        elif itemGroup == "Booster":
            stuff.getModifiedItemAttr("boosterDuration")
            text = "{0} min".format(formatAmount(stuff.getModifiedItemAttr("boosterDuration") / 1000 / 60, 3, 0, 3))
            return text, "Booster Duration"
        elif itemGroup in ("Super Weapon", "Structure Doomsday Weapon"):
            volleyParams = stuff.getVolleyParameters(ignoreState=True)
            dmg = sum(dt.total for dt in volleyParams.values())
            duration = (max(volleyParams) - min(volleyParams)) / 1000
            if dmg <= 0:
                text = ""
                tooltip = ""
            elif duration > 0:
                text = "{} over {}s".format(
                    formatAmount(dmg, 3, 0, 6),
                    formatAmount((duration), 0, 0, 0))
                tooltip = "Raw damage done over time"
            else:
                text = "{} dmg".format(formatAmount(dmg, 3, 0, 6))
                tooltip = "Raw damage done"
            return text, tooltip

            pass
        elif itemGroup in ("Energy Weapon", "Hybrid Weapon", "Projectile Weapon", "Combat Drone", "Fighter Drone"):
            trackingSpeed = stuff.getModifiedItemAttr("trackingSpeed")
            optimalSig = stuff.getModifiedItemAttr("optimalSigRadius")
            if not trackingSpeed or not optimalSig:
                return "", None
            normalizedTracking = trackingSpeed * 40000 / optimalSig
            text = "{0}".format(formatAmount(normalizedTracking, 3, 0, 3))
            tooltip = "Tracking speed"
            return text, tooltip
        elif itemGroup == "Precursor Weapon":
            info = []
            trackingSpeed = stuff.getModifiedItemAttr("trackingSpeed")
            if trackingSpeed:
                text = "{0}".format(formatAmount(trackingSpeed, 3, 0, 3))
                tooltip = "tracking speed"
                info.append((text, tooltip))

            defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
            spoolTime = stuff.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False))[1]
            if spoolTime:
                text = "{0}s".format(formatAmount(spoolTime, 3, 0, 3))
                tooltip = "spool up time"
                info.append((text, tooltip))
            if not info:
                return "", None
            text = ' | '.join(i[0] for i in info)
            tooltip = ' and '.join(i[1] for i in info).capitalize()
            return text, tooltip
        elif itemGroup == "Vorton Projector":
            cloudSize = stuff.getModifiedItemAttr("aoeCloudSize")
            aoeVelocity = stuff.getModifiedItemAttr("aoeVelocity")
            if not cloudSize or not aoeVelocity:
                return "", None
            text = "{0}{1} | {2}{3}".format(formatAmount(cloudSize, 3, 0, 3), "m",
                                            formatAmount(aoeVelocity, 3, 0, 3), "m/s")
            tooltip = "Explosion radius and explosion velocity"
            return text, tooltip
        elif itemCategory == "Subsystem":
            slots = ("hi", "med", "low")
            info = []
            for slot in slots:
                n = int(stuff.getModifiedItemAttr("%sSlotModifier" % slot))
                if n > 0:
                    info.append("{0}{1}".format(n, slot[0].upper()))
            return "+ " + ", ".join(info), "Slot Modifiers"
        elif (
            itemGroup in ("Energy Neutralizer", "Structure Energy Neutralizer") or
            (itemGroup in ("Structure Burst Projector", "Burst Projectors") and "doomsdayAOENeut" in item.effects)
        ):
            neutAmount = stuff.getModifiedItemAttr("energyNeutralizerAmount")
            cycleParams = stuff.getCycleParameters()
            if cycleParams is None:
                return "", None
            cycleTime = cycleParams.averageTime
            if not neutAmount or not cycleTime:
                return "", None
            capPerSec = float(-neutAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(capPerSec, 3, 0, 3))
            tooltip = "Energy neutralization per second"
            return text, tooltip
        elif itemGroup == "Energy Nosferatu":
            neutAmount = stuff.getModifiedItemAttr("powerTransferAmount")
            cycleParams = stuff.getCycleParameters()
            if cycleParams is None:
                return "", None
            cycleTime = cycleParams.averageTime
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
        elif itemGroup in ("Warp Scrambler", "Warp Core Stabilizer", "Structure Warp Scrambler"):
            scramStr = stuff.getModifiedItemAttr("warpScrambleStrength")
            if not scramStr:
                return "", None
            text = "{0}".format(formatAmount(-scramStr, 3, 0, 3, forceSign=True))
            tooltip = "Warp core strength modification"
            return text, tooltip
        elif (
            itemGroup in ("Stasis Web", "Stasis Webifying Drone", "Structure Stasis Webifier") or
            (itemGroup in ("Structure Burst Projector", "Burst Projectors") and "doomsdayAOEWeb" in item.effects)
        ):
            speedFactor = stuff.getModifiedItemAttr("speedFactor")
            if not speedFactor:
                return "", None
            text = "{0}%".format(formatAmount(speedFactor, 3, 0, 3))
            tooltip = "Speed reduction"
            return text, tooltip
        elif (
            itemGroup == "Target Painter" or
            (itemGroup == "Structure Disruption Battery" and "structureModuleEffectTargetPainter" in item.effects) or
            (itemGroup in ("Structure Burst Projector", "Burst Projectors") and "doomsdayAOEPaint" in item.effects)
        ):
            sigRadBonus = stuff.getModifiedItemAttr("signatureRadiusBonus")
            if not sigRadBonus:
                return "", None
            text = "{0}%".format(formatAmount(sigRadBonus, 3, 0, 3, forceSign=True))
            tooltip = "Signature radius increase"
            return text, tooltip
        elif (
            itemGroup == "Sensor Dampener" or
            (itemGroup == "Structure Disruption Battery" and "structureModuleEffectRemoteSensorDampener" in item.effects) or
            (itemGroup in ("Structure Burst Projector", "Burst Projectors") and "doomsdayAOEDamp" in item.effects)
        ):
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
        elif (
            itemGroup in ("Weapon Disruptor", "Structure Disruption Battery") or
            (itemGroup in ("Structure Burst Projector", "Burst Projectors") and "doomsdayAOETrack" in item.effects)
        ):
            # Weapon disruption now covers both tracking and guidance (missile) disruptors
            # First get the attributes for tracking disruptors
            optimalRangeBonus = stuff.getModifiedItemAttr("maxRangeBonus")
            falloffRangeBonus = stuff.getModifiedItemAttr("falloffBonus")
            trackingSpeedBonus = stuff.getModifiedItemAttr("trackingSpeedBonus")

            trackingDisruptorAttributes = {
                "optimal range": optimalRangeBonus,
                "falloff range": falloffRangeBonus,
                "tracking speed": trackingSpeedBonus}

            isTrackingDisruptor = any([x is not None and x != 0 for x in list(trackingDisruptorAttributes.values())])

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

            isGuidanceDisruptor = any([x is not None and x != 0 for x in list(guidanceDisruptorAttributes.values())])

            if not isTrackingDisruptor and not isGuidanceDisruptor:
                return "", None

            texts = []
            ttSegments = []

            for status, attributes in ((isTrackingDisruptor, trackingDisruptorAttributes), (isGuidanceDisruptor, guidanceDisruptorAttributes)):
                if not status:
                    continue
                display = max(list(attributes.values()), key=lambda x: abs(x))
                texts.append("{0}%".format(formatAmount(display, 3, 0, 3, forceSign=True)))
                ttEntries = []
                for attributeName, attributeValue in list(attributes.items()):
                    if abs(attributeValue) == abs(display):
                        ttEntries.append(attributeName)
                ttSegments.append("{0} disruption".format(formatList(ttEntries)).capitalize())
            return ' | '.join(texts), '\n'.join(ttSegments)
        elif itemGroup in (
            "Gyrostabilizer",
            "Magnetic Field Stabilizer",
            "Heat Sink",
            "Ballistic Control system",
            "Structure Weapon Upgrade",
            "Entropic Radiation Sink",
            "Vorton Projector Upgrade"
        ):
            attrMap = {
                "Gyrostabilizer": ("damageMultiplier", "speedMultiplier", "Projectile weapon"),
                "Magnetic Field Stabilizer": ("damageMultiplier", "speedMultiplier", "Hybrid weapon"),
                "Heat Sink": ("damageMultiplier", "speedMultiplier", "Energy weapon"),
                "Ballistic Control system": ("missileDamageMultiplierBonus", "speedMultiplier", "Missile"),
                "Structure Weapon Upgrade": ("missileDamageMultiplierBonus", "speedMultiplier", "Missile"),
                "Entropic Radiation Sink": ("damageMultiplier", "speedMultiplier", "Precursor weapon"),
                "Vorton Projector Upgrade": ("damageMultiplier", "speedMultiplier", "Vorton projector")}
            dmgAttr, rofAttr, weaponName = attrMap[itemGroup]
            dmg = stuff.getModifiedItemAttr(dmgAttr)
            rof = stuff.getModifiedItemAttr(rofAttr)
            if not dmg or not rof:
                return "", None
            texts = []
            tooltips = []
            cumulative = (dmg / rof - 1) * 100
            texts.append("{}%".format(formatAmount(cumulative, 3, 0, 3, forceSign=True)))
            tooltips.append("{} DPS boost".format(weaponName))
            droneDmg = stuff.getModifiedItemAttr("droneDamageBonus")
            if droneDmg:
                texts.append("{}%".format(formatAmount(droneDmg, 3, 0, 3, forceSign=True)))
                tooltips.append("drone DPS boost".format(weaponName))
            return ' | '.join(texts), ' and '.join(tooltips)
        elif itemGroup == "Drone Damage Modules":
            dmg = stuff.getModifiedItemAttr("droneDamageBonus")
            if not dmg:
                return
            text = "{}%".format(formatAmount(dmg, 3, 0, 3, forceSign=True))
            tooltip = "Drone DPS boost"
            return text, tooltip
        elif (
            itemGroup in ("ECM", "Burst Jammer", "Structure ECM Battery") or
            (itemGroup in ("Structure Burst Projector", "Burst Projectors") and "doomsdayAOEECM" in item.effects)
        ):
            grav = stuff.getModifiedItemAttr("scanGravimetricStrengthBonus")
            ladar = stuff.getModifiedItemAttr("scanLadarStrengthBonus")
            radar = stuff.getModifiedItemAttr("scanRadarStrengthBonus")
            magnet = stuff.getModifiedItemAttr("scanMagnetometricStrengthBonus")
            displayMax = max(grav, ladar, radar, magnet)
            displayMin = min(grav, ladar, radar, magnet)
            if grav is None or ladar is None or radar is None or magnet is None or displayMax is None:
                return "", None

            if displayMax == displayMin or displayMin is None:
                text = "{0}".format(
                    formatAmount(displayMax, 3, 0, 3),
                )
            else:
                text = "{0} | {1}".format(
                    formatAmount(displayMax, 3, 0, 3),
                    formatAmount(displayMin, 3, 0, 3),
                )
            tooltip = "ECM Jammer Strength:\n{0} Gravimetric | {1} Ladar | {2} Magnetometric | {3} Radar".format(
                formatAmount(grav, 3, 0, 3),
                formatAmount(ladar, 3, 0, 3),
                formatAmount(magnet, 3, 0, 3),
                formatAmount(radar, 3, 0, 3),
            )
            return text, tooltip
        elif itemGroup in ("Remote Sensor Booster", "Sensor Booster", "Signal Amplifier", "Structure Signal Amplifier"):
            textLines = []
            tooltipLines = []
            scanResBonus = stuff.getModifiedItemAttr("scanResolutionBonus")
            if scanResBonus:
                textLines.append("{}%".format(formatAmount(scanResBonus, 3, 0, 3)))
                tooltipLines.append("{}% scan resolution".format(formatAmount(scanResBonus, 3, 0, 3)))
            lockRangeBonus = stuff.getModifiedItemAttr("maxTargetRangeBonus")
            if lockRangeBonus:
                textLines.append("{}%".format(formatAmount(lockRangeBonus, 3, 0, 3)))
                tooltipLines.append("{}% lock range".format(formatAmount(lockRangeBonus, 3, 0, 3)))
            gravBonus = stuff.getModifiedItemAttr("scanGravimetricStrengthPercent")
            if gravBonus:
                textLines.append("{}%".format(formatAmount(gravBonus, 3, 0, 3)))
                tooltipLines.append("{}% sensor strength".format(formatAmount(gravBonus, 3, 0, 3)))
            if not textLines:
                return "", None
            text = " | ".join(textLines)
            tooltip = "Applied bonuses:\n{}".format(" | ".join(tooltipLines))
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
            text = "{0}s".format(formatAmount(float(recalibration) / 1000, 3, 0, 3))
            tooltip = "Sensor recalibration time"
            return text, tooltip
        elif itemGroup == "Remote Armor Repairer":
            rps = stuff.getRemoteReps(ignoreState=True).armor
            if not rps:
                return "", None
            text = "{0}/s".format(formatAmount(rps, 3, 0, 3, forceSign=True))
            tooltip = "Armor repaired per second"
            return text, tooltip
        elif itemGroup == "Mutadaptive Remote Armor Repairer":
            defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
            spoolOptDefault = SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False)
            spoolOptPre = SpoolOptions(SpoolType.SPOOL_SCALE, 0, True)
            spoolOptFull = SpoolOptions(SpoolType.SPOOL_SCALE, 1, True)
            rps = stuff.getRemoteReps(spoolOptions=spoolOptDefault, ignoreState=True).armor
            rpsPre = stuff.getRemoteReps(spoolOptions=spoolOptPre, ignoreState=True).armor
            rpsFull = stuff.getRemoteReps(spoolOptions=spoolOptFull, ignoreState=True).armor
            if not rps:
                return "", None
            text = []
            tooltip = []
            text.append("{}/s".format(formatAmount(rps, 3, 0, 3, forceSign=True)))
            tooltip.append("Armor repaired per second")
            spoolTime = stuff.getSpoolData(spoolOptDefault)[1]
            if spoolTime:
                text.append("{}s".format(formatAmount(spoolTime, 3, 0, 3)))
                tooltip.append("spool up time")
            text = " | ".join(text)
            tooltip = " and ".join(tooltip)
            spoolTimePre = stuff.getSpoolData(spoolOptPre)[1]
            spoolTimeFull = stuff.getSpoolData(spoolOptFull)[1]
            if spoolTimePre != spoolTimeFull:
                tooltip = "{}\nSpool up: {}-{} over {}s".format(
                    tooltip,
                    formatAmount(rpsPre, 3, 0, 3),
                    formatAmount(rpsFull, 3, 0, 3),
                    formatAmount(spoolTimeFull - spoolTimePre, 3, 0, 3))
            return text, tooltip
        elif itemGroup == "Remote Shield Booster":
            rps = stuff.getRemoteReps(ignoreState=True).shield
            if not rps:
                return "", None
            text = "{0}/s".format(formatAmount(rps, 3, 0, 3, forceSign=True))
            tooltip = "Shield transferred per second"
            return text, tooltip
        elif itemGroup == "Remote Capacitor Transmitter":
            rps = stuff.getRemoteReps(ignoreState=True).capacitor
            if not rps:
                return "", None
            text = "{0}/s".format(formatAmount(rps, 3, 0, 3, forceSign=True))
            tooltip = "Energy transferred per second"
            return text, tooltip
        elif itemGroup == "Remote Hull Repairer":
            rps = stuff.getRemoteReps(ignoreState=True).hull
            if not rps:
                return "", None
            text = "{0}/s".format(formatAmount(rps, 3, 0, 3, forceSign=True))
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
            lockRangeBonus = stuff.getModifiedItemAttr("maxTargetRangeBonus")
            scanResBonus = stuff.getModifiedItemAttr("scanResolutionBonus")
            falloffRangeBonus = stuff.getModifiedItemAttr("falloffBonus")
            optimalRangeBonus = stuff.getModifiedItemAttr("maxRangeBonus")
            trackingSpeedBonus = stuff.getModifiedItemAttr("trackingSpeedBonus")
            grav = stuff.getModifiedItemAttr("scanGravimetricStrengthBonus")
            ladar = stuff.getModifiedItemAttr("scanLadarStrengthBonus")
            radar = stuff.getModifiedItemAttr("scanRadarStrengthBonus")
            magnet = stuff.getModifiedItemAttr("scanMagnetometricStrengthBonus")
            if sigRadBonus:
                text = "{0}%".format(formatAmount(sigRadBonus, 3, 0, 3, forceSign=True))
                tooltip = "Signature radius increase"
                return text, tooltip
            if lockRangeBonus or scanResBonus:
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
            if falloffRangeBonus or optimalRangeBonus or trackingSpeedBonus:
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
        elif itemGroup in ("Frequency Mining Laser", "Strip Miner", "Mining Laser", "Gas Cloud Scoops", "Mining Drone", "Gas Cloud Harvesters"):
            yps = stuff.getMiningYPS(ignoreState=True)
            if not yps:
                return "", None
            yph = yps * 3600
            wps = stuff.getMiningWPS(ignoreState=True)
            wph = wps * 3600
            textParts = []
            textParts.append(formatAmount(yps, 3, 0, 3))
            tipLines = []
            tipLines.append("{} m\u00B3 mining yield per second ({} m\u00B3 per hour)".format(
                formatAmount(yps, 3, 0, 3), formatAmount(yph, 3, 0, 3)))
            if wps > 0:
                textParts.append(formatAmount(wps, 3, 0, 3))
                tipLines.append("{} m\u00B3 mining waste per second ({} m\u00B3 per hour)".format(
                    formatAmount(wps, 3, 0, 3), formatAmount(wph, 3, 0, 3)))
            text = '{} m\u00B3/s'.format('+'.join(textParts))
            tooltip = '\n'.join(tipLines)
            return text, tooltip
        elif itemGroup == "Logistic Drone":
            rpsData = stuff.getRemoteReps(ignoreState=True)
            rrType = None
            rps = None
            if rpsData.shield:
                rps = rpsData.shield
                rrType = 'Shield'
            elif rpsData.armor:
                rps = rpsData.armor
                rrType = 'Armor'
            elif rpsData.hull:
                rps = rpsData.hull
                rrType = 'Hull'
            if not rrType or not rps:
                return "", None
            text = "{}/s".format(formatAmount(rps, 3, 0, 3))
            tooltip = "{} HP repaired per second\n{} HP/s per drone".format(rrType, formatAmount(rps / stuff.amount, 3, 0, 3))
            return text, tooltip
        elif itemGroup == "Energy Neutralizer Drone":
            neutAmount = stuff.getModifiedItemAttr("energyNeutralizerAmount")
            cycleTime = stuff.getModifiedItemAttr("energyNeutralizerDuration")
            if not neutAmount or not cycleTime:
                return "", None
            capPerSec = float(-neutAmount) * 1000 / cycleTime
            text = "{0}/s".format(formatAmount(capPerSec, 3, 0, 3))
            tooltip = "Energy neutralization per second"
            return text, tooltip
        elif itemGroup in ("Micro Jump Drive", "Micro Jump Field Generators"):
            cycleTime = stuff.getModifiedItemAttr("duration") / 1000
            text = "{0}s".format(formatAmount(cycleTime, 3, 0, 3))
            tooltip = "Spoolup time"
            return text, tooltip
        elif itemGroup in ("Siege Module", "Cynosural Field Generator"):
            amt = stuff.getModifiedItemAttr("consumptionQuantity")
            if amt:
                typeID = stuff.getModifiedItemAttr("consumptionType")
                item = Market.getInstance().getItem(typeID)
                text = "{0} units".format(formatAmount(amt, 3, 0, 3))
                return text, item.name
            else:
                return "", None
        elif itemGroup in (
                "Ancillary Armor Repairer",
                "Ancillary Shield Booster",
                "Capacitor Booster",
                "Ancillary Remote Armor Repairer",
                "Ancillary Remote Shield Booster",
        ):
            if "Armor" in itemGroup or "Shield" in itemGroup:
                boosted_attribute = "HP"
                reload_time = stuff.getModifiedItemAttr("reloadTime", 0) / 1000
            elif "Capacitor" in itemGroup:
                boosted_attribute = "Cap"
                reload_time = 10
            else:
                boosted_attribute = ""
                reload_time = 0

            cycles = max(stuff.numShots, 0)
            cycleTime = max(stuff.rawCycleTime, 0)

            # Get HP or boosted amount
            stuff_hp = max(stuff.hpBeforeReload, 0)
            armor_hp = stuff.getModifiedItemAttr("armorDamageAmount", 0)
            capacitor_hp = stuff.getModifiedChargeAttr("capacitorBonus", 0)
            shield_hp = stuff.getModifiedItemAttr("shieldBonus", 0)
            hp = max(stuff_hp, armor_hp * cycles, capacitor_hp * cycles, shield_hp * cycles, 0)

            nonChargedMap = {
                "Ancillary Remote Armor Repairer": ("armor", "Armor repaired per second"),
                "Ancillary Remote Shield Booster": ("shield", "Shield transferred per second")}
            if not cycles and itemGroup in nonChargedMap:
                rps = stuff.getRemoteReps(ignoreState=True)
                rps = getattr(rps, nonChargedMap[itemGroup][0])
                if not rps:
                    return "", None
                text = "{0}/s".format(formatAmount(rps, 3, 0, 3, forceSign=True))
                tooltip = nonChargedMap[itemGroup][1]
                return text, tooltip

            if not hp or not cycleTime or not cycles:
                return "", None

            fit = Fit.getInstance().getFit(self.fittingView.getActiveFit())
            ehpTotal = fit.ehp
            hpTotal = fit.hp
            try:
                useEhp = self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective
            except KeyError:
                useEhp = False
            tooltip = "{0} restored over duration using charges (plus reload)".format(boosted_attribute)

            if useEhp and boosted_attribute == "HP" and "Remote" not in itemGroup:
                if "Ancillary Armor Repairer" in itemGroup:
                    hpRatio = ehpTotal["armor"] / hpTotal["armor"]
                else:
                    hpRatio = ehpTotal["shield"] / hpTotal["shield"]
                tooltip = "E{0}".format(tooltip)
            else:
                hpRatio = 1

            if "Ancillary" in itemGroup and "Armor" in itemGroup:
                hpRatio *= stuff.getModifiedItemAttr("chargedArmorDamageMultiplier", 1)

            ehp = hp * hpRatio

            duration = cycles * cycleTime / 1000
            for number_of_cycles in {5, 10, 25}:
                tooltip = "{0}\n{1} charges lasts {2} seconds ({3} cycles)".format(
                    tooltip,
                    formatAmount(number_of_cycles * cycles, 3, 0, 3),
                    formatAmount((duration + reload_time) * number_of_cycles, 3, 0, 3),
                    formatAmount(number_of_cycles, 3, 0, 3)
                )
            text = "{0} / {1}s (+{2}s)".format(
                formatAmount(ehp, 3, 0, 9),
                formatAmount(duration, 3, 0, 3),
                formatAmount(reload_time, 3, 0, 3)
            )

            return text, tooltip
        elif itemGroup == "Armor Resistance Shift Hardener":
            itemArmorResistanceShiftHardenerEM = (1 - stuff.getModifiedItemAttr("armorEmDamageResonance")) * 100
            itemArmorResistanceShiftHardenerTherm = (1 - stuff.getModifiedItemAttr("armorThermalDamageResonance")) * 100
            itemArmorResistanceShiftHardenerKin = (1 - stuff.getModifiedItemAttr("armorKineticDamageResonance")) * 100
            itemArmorResistanceShiftHardenerExp = (1 - stuff.getModifiedItemAttr("armorExplosiveDamageResonance")) * 100

            text = "{0}% | {1}% | {2}% | {3}%".format(
                formatAmount(itemArmorResistanceShiftHardenerEM, 3, 0, 3),
                formatAmount(itemArmorResistanceShiftHardenerTherm, 3, 0, 3),
                formatAmount(itemArmorResistanceShiftHardenerKin, 3, 0, 3),
                formatAmount(itemArmorResistanceShiftHardenerExp, 3, 0, 3),
            )
            tooltip = "Resistances shifted to damage profile:\n{0}% EM | {1}% Therm | {2}% Kin | {3}% Exp".format(
                formatAmount(itemArmorResistanceShiftHardenerEM, 3, 0, 3),
                formatAmount(itemArmorResistanceShiftHardenerTherm, 3, 0, 3),
                formatAmount(itemArmorResistanceShiftHardenerKin, 3, 0, 3),
                formatAmount(itemArmorResistanceShiftHardenerExp, 3, 0, 3),
            )
            return text, tooltip
        elif itemGroup in ("Cargo Scanner", "Ship Scanner", "Survey Scanner"):
            duration = stuff.getModifiedItemAttr("duration")
            if not duration:
                return "", None
            text = "{}s".format(formatAmount(duration / 1000, 3, 0, 0))
            tooltip = "Scan duration"
            return text, tooltip
        elif itemGroup == "Command Burst":
            textSections = []
            tooltipSections = []
            buffMap = {}
            for seq in (1, 2, 3, 4):
                buffId = stuff.getModifiedChargeAttr(f'warfareBuff{seq}ID')
                if not buffId:
                    continue
                buffValue = stuff.getModifiedItemAttr(f'warfareBuff{seq}Value')
                buffMap[buffId] = buffValue
                if buffId == 10:  # Shield Burst: Shield Harmonizing: Shield Resistance
                    # minus buff value because ingame shows positive value
                    textSections.append(f"{formatAmount(-buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("shield resistance")
                elif buffId == 11:  # Shield Burst: Active Shielding: Repair Duration/Capacitor
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("shield RR duration & capacictor use")
                elif buffId == 12:  # Shield Burst: Shield Extension: Shield HP
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("shield HP")
                elif buffId == 13:  # Armor Burst: Armor Energizing: Armor Resistance
                    # minus buff value because ingame shows positive value
                    textSections.append(f"{formatAmount(-buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("armor resistance")
                elif buffId == 14:  # Armor Burst: Rapid Repair: Repair Duration/Capacitor
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("armor RR duration & capacitor use")
                elif buffId == 15:  # Armor Burst: Armor Reinforcement: Armor HP
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("armor HP")
                elif buffId == 16:  # Information Burst: Sensor Optimization: Scan Resolution
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("scan resolution")
                elif buffId == 26:  # Information Burst: Sensor Optimization: Targeting Range
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("targeting range")
                elif buffId == 17:  # Information Burst: Electronic Superiority: EWAR Range and Strength
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("electronic warfare modules range & strength")
                elif buffId == 18:  # Information Burst: Electronic Hardening: Sensor Strength
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("sensor strength")
                elif buffId == 19:  # Information Burst: Electronic Hardening: RSD/RWD Resistance
                    textSections.append(f"{formatAmount(-buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("sensor dampener & weapon disruption resistance")
                elif buffId == 20:  # Skirmish Burst: Evasive Maneuvers: Signature Radius
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("signature radius")
                elif buffId == 60:  # Skirmish Burst: Evasive Maneuvers: Agility
                    # minus the buff value because we want Agility as shown ingame, not inertia modifier
                    textSections.append(f"{formatAmount(-buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("agility")
                elif buffId == 21:  # Skirmish Burst: Interdiction Maneuvers: Tackle Range
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("warp disruption & stasis web range")
                elif buffId == 22:  # Skirmish Burst: Rapid Deployment: AB/MWD Speed Increase
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("AB/MWD speed increase")
                elif buffId == 23:  # Mining Burst: Mining Laser Field Enhancement: Mining/Survey Range
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("mining/survey module range")
                elif buffId == 24:  # Mining Burst: Mining Laser Optimization: Mining Capacitor/Duration
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("mining module duration & capacitor use")
                elif buffId == 25:  # Mining Burst: Mining Equipment Preservation: Crystal Volatility
                    textSections.append(f"{formatAmount(buffValue, 3, 0, 3, forceSign=True)}%")
                    tooltipSections.append("mining crystal volatility")
            if not textSections:
                return '', None
            text = ' | '.join(textSections)
            tooltip = '{} bonus'.format(' | '.join(tooltipSections))
            if tooltip:
                tooltip = tooltip[0].capitalize() + tooltip[1:]
            return text, tooltip
        elif stuff.charge is not None:
            chargeGroup = stuff.charge.group.name
            if chargeGroup.endswith("Rocket") or chargeGroup.endswith("Missile") or chargeGroup.endswith("Torpedo"):
                cloudSize = stuff.getModifiedChargeAttr("aoeCloudSize")
                aoeVelocity = stuff.getModifiedChargeAttr("aoeVelocity")
                if not cloudSize or not aoeVelocity:
                    return "", None
                text = "{0}{1} | {2}{3}".format(formatAmount(cloudSize, 3, 0, 3), "m",
                                                formatAmount(aoeVelocity, 3, 0, 3), "m/s")
                tooltip = "Explosion radius and explosion velocity"
                return text, tooltip
            elif chargeGroup in ("Bomb", "Guided Bomb"):
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
                text = "{}".format(formatAmount(scanStr, 4, 0, 3))
                tooltip = "Scan strength at {} AU scan range".format(formatAmount(baseRange, 3, 0, 0))
                return text, tooltip
            else:
                return "", None
        else:
            return "", None


Miscellanea.register()
