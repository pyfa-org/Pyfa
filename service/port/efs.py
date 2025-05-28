import json
from math import log
from numbers import Number

from logbook import Logger

import eos.db
from config import getVersion
from service.fit import Fit
from service.market import Market
from eos.const import FittingModuleState, FittingHardpoint, FittingSlot
from service.const import PortEftRigSize
from eos.saveddata.module import Module
from eos.saveddata.drone import Drone
from eos.effectHandlerHelpers import HandledList
from eos.db import gamedata_session, getCategory, getAttributeInfo, getGroup
from eos.gamedata import Attribute, Effect, Group, Item, ItemEffect
from eos.utils.spoolSupport import SpoolType, SpoolOptions
from gui.fitCommands.calc.module.localAdd import CalcAddLocalModuleCommand
from gui.fitCommands.calc.module.localRemove import CalcRemoveLocalModulesCommand
from gui.fitCommands.calc.module.changeCharges import CalcChangeModuleChargesCommand
from gui.fitCommands.helpers import ModuleInfo


pyfalog = Logger(__name__)
pyfaVersion = getVersion()


class EfsPort:
    wepTestSet = {}
    version = 0.06

    @staticmethod
    def attrDirectMap(values, target, source):
        for val in values:
            target[val] = source.getModifiedItemAttr(val)

    @staticmethod
    def getT2MwdSpeed(fit, sFit):
        fitID = fit.ID
        propID = None
        shipHasMedSlots = fit.ship.getModifiedItemAttr("medSlots") > 0
        shipPower = fit.ship.getModifiedItemAttr("powerOutput")
        # Monitors have a 99% reduction to prop mod power requirements
        if fit.ship.typeName == "Monitor":
            shipPower *= 100
        rigSize = fit.ship.getModifiedItemAttr("rigSize")
        if not shipHasMedSlots:
            return None

        filterVal = Item.groupID == getGroup("Propulsion Module").ID
        propMods = gamedata_session.query(Item).options().filter(filterVal).all()
        mapPropData = lambda propName: \
                      next(map(lambda propMod: {"id": propMod.typeID, "powerReq": propMod.attributes["power"].value},
                               (filter(lambda mod: mod.typeName == propName, propMods))))
        mwd5mn = mapPropData("5MN Microwarpdrive II")
        mwd50mn = mapPropData("50MN Microwarpdrive II")
        mwd500mn = mapPropData("500MN Microwarpdrive II")
        mwd50000mn = mapPropData("50000MN Microwarpdrive II")
        if rigSize == PortEftRigSize.SMALL or rigSize is None:
            propID = mwd5mn["id"] if shipPower > mwd5mn["powerReq"] else None
        elif rigSize == PortEftRigSize.MEDIUM:
            propID = mwd50mn["id"] if shipPower > mwd50mn["powerReq"] else mwd5mn["id"]
        elif rigSize == PortEftRigSize.LARGE:
            propID = mwd500mn["id"] if shipPower > mwd500mn["powerReq"] else mwd50mn["id"]
        elif rigSize == PortEftRigSize.CAPITAL:
            propID = mwd50000mn["id"] if shipPower > mwd50000mn["powerReq"] else mwd500mn["id"]

        if propID is None:
            return None
        cmd = CalcAddLocalModuleCommand(fitID, ModuleInfo(itemID=propID))
        cmd.Do()
        if cmd.needsGuiRecalc:
            sFit.recalc(fit)
        fit = eos.db.getFit(fitID)
        mwdPropSpeed = fit.maxSpeed
        mwdPosition = list(filter(lambda mod: mod.item and mod.item.ID == propID, fit.modules))[0].position
        cmd = CalcRemoveLocalModulesCommand(fitID, [mwdPosition])
        cmd.Do()
        if cmd.needsGuiRecalc:
            sFit.recalc(fit)
        fit = eos.db.getFit(fitID)
        return mwdPropSpeed

    @staticmethod
    def getPropData(fit, sFit):
        propMods = filter(lambda mod: mod.item and mod.item.group.name == "Propulsion Module", fit.modules)
        activePropWBloomFilter = lambda mod: mod.state > 0 and "signatureRadiusBonus" in mod.item.attributes
        propWithBloom = next(filter(activePropWBloomFilter, propMods), None)
        if propWithBloom is not None:
            oldPropState = propWithBloom.state
            propWithBloom.state = FittingModuleState.ONLINE
            sFit.recalc(fit)
            sp = fit.maxSpeed
            sig = fit.ship.getModifiedItemAttr("signatureRadius")
            propWithBloom.state = oldPropState
            sFit.recalc(fit)
            return {"usingMWD": True, "unpropedSpeed": sp, "unpropedSig": sig}
        return {
            "usingMWD": False,
            "unpropedSpeed": fit.maxSpeed,
            "unpropedSig": fit.ship.getModifiedItemAttr("signatureRadius")
        }

    @staticmethod
    def getModsInGroups(fit, modGroupNames):
        matchingMods = list(filter(lambda mod: mod.item and mod.item.group.name in modGroupNames, fit.modules))
        # Sort mods to prevent the order needlessly changing as pyfa updates.
        matchingMods.sort(key=lambda mod: mod.item.ID)
        matchingMods.sort(key=lambda mod: mod.item.group.ID)
        return matchingMods

    # Note this also includes data for any cap boosters as they "repair" cap.
    @staticmethod
    def getRepairData(fit, sFit):
        modGroupNames = [
            "Shield Booster", "Armor Repair Unit",
            "Ancillary Shield Booster", "Ancillary Armor Repairer",
            "Hull Repair Unit", "Capacitor Booster",
        ]
        repairMods = EfsPort.getModsInGroups(fit, modGroupNames)
        repairs = [];
        for mod in repairMods:
            stats = {}
            EfsPort.attrDirectMap(["duration", "capacitorNeed"], stats, mod)
            if mod.item.group.name in ["Armor Repair Unit", "Ancillary Armor Repairer"]:
                stats["type"] = "Armor Repairer"
                EfsPort.attrDirectMap(["armorDamageAmount"], stats, mod)
                if mod.item.group.name == "Ancillary Armor Repairer":
                    stats["numShots"] = mod.numShots
                    EfsPort.attrDirectMap(["reloadTime", "chargedArmorDamageMultiplier"], stats, mod)
            elif mod.item.group.name in ["Shield Booster", "Ancillary Shield Booster"]:
                stats["type"] = "Shield Booster"
                EfsPort.attrDirectMap(["shieldBonus"], stats, mod)
                if mod.item.group.name == "Ancillary Shield Booster":
                    stats["numShots"] = mod.numShots
                    EfsPort.attrDirectMap(["reloadTime"], stats, mod)
                    c = mod.charge
                    if c:
                        sFit.recalc(fit)
                        CalcChangeModuleChargesCommand(
                            fit.ID,
                            projected=False,
                            chargeMap={mod.position: None},
                            recalc=False).Do()
                        sFit.recalc(fit)
                        stats["unloadedCapacitorNeed"] = mod.getModifiedItemAttr("capacitorNeed")
                        CalcChangeModuleChargesCommand(
                            fit.ID,
                            projected=False,
                            chargeMap={mod.position: c.typeID},
                            recalc=False).Do()
                        sFit.recalc(fit)
            elif mod.item.group.name == "Capacitor Booster":
                # The capacitorNeed is negative, which provides the boost.
                stats["type"] = "Capacitor Booster"
                stats["numShots"] = mod.numShots
                EfsPort.attrDirectMap(["reloadTime"], stats, mod)
            repairs.append(stats)
        return repairs

    @staticmethod
    def getOutgoingProjectionData(fit):
        # This is a subset of module groups capable of projection and a superset of those currently used by efs
        modGroupNames = [
            "Remote Shield Booster", "Warp Scrambler", "Stasis Web", "Remote Capacitor Transmitter",
            "Energy Nosferatu", "Energy Neutralizer", "Burst Jammer", "ECM", "Sensor Dampener",
            "Weapon Disruptor", "Remote Armor Repairer", "Target Painter", "Remote Hull Repairer",
            "Burst Projectors", "Warp Disrupt Field Generator", "Armor Resistance Shift Hardener",
            "Micro Jump Drive", "Ship Modifiers", "Stasis Grappler", "Ancillary Remote Shield Booster",
            "Ancillary Remote Armor Repairer", "Titan Phenomena Generator", "Non-Repeating Hardeners",
            "Mutadaptive Remote Armor Repairer"
        ]
        projectedMods = EfsPort.getModsInGroups(fit, modGroupNames)
        projections = []
        for mod in projectedMods:
            maxRangeDefault = 0
            falloffDefault = 0
            stats = {}
            if mod.item.group.name in ["Stasis Web", "Stasis Grappler"]:
                stats["type"] = "Stasis Web"
                stats["optimal"] = mod.getModifiedItemAttr("maxRange")
                EfsPort.attrDirectMap(["duration", "speedFactor"], stats, mod)
            elif mod.item.group.name == "Weapon Disruptor":
                stats["type"] = "Weapon Disruptor"
                stats["optimal"] = mod.getModifiedItemAttr("maxRange")
                stats["falloff"] = mod.getModifiedItemAttr("falloffEffectiveness")
                EfsPort.attrDirectMap([
                    "trackingSpeedBonus", "maxRangeBonus", "falloffBonus", "aoeCloudSizeBonus",
                    "aoeVelocityBonus", "missileVelocityBonus", "explosionDelayBonus"
                ], stats, mod)
            elif mod.item.group.name == "Energy Nosferatu":
                stats["type"] = "Energy Nosferatu"
                EfsPort.attrDirectMap(["powerTransferAmount", "energyNeutralizerSignatureResolution"], stats, mod)
            elif mod.item.group.name == "Energy Neutralizer":
                stats["type"] = "Energy Neutralizer"
                EfsPort.attrDirectMap([
                    "energyNeutralizerSignatureResolution", "entityCapacitorLevelModifierSmall",
                    "entityCapacitorLevelModifierMedium", "entityCapacitorLevelModifierLarge",
                    "energyNeutralizerAmount"
                ], stats, mod)
            elif mod.item.group.name in ["Remote Shield Booster", "Ancillary Remote Shield Booster"]:
                stats["type"] = "Remote Shield Booster"
                EfsPort.attrDirectMap(["shieldBonus"], stats, mod)
            elif mod.item.group.name in [
                    "Remote Armor Repairer", "Ancillary Remote Armor Repairer", "Mutadaptive Remote Armor Repairer"
            ]:
                stats["type"] = "Remote Armor Repairer"
                EfsPort.attrDirectMap(["armorDamageAmount"], stats, mod)
            elif mod.item.group.name in ["Remote Capacitor Transmitter"]:
                stats["type"] = "Remote Capacitor Transmitter"
                EfsPort.attrDirectMap(["powerTransferAmount"], stats, mod)
            elif mod.item.group.name == "Warp Scrambler":
                stats["type"] = "Warp Scrambler"
                EfsPort.attrDirectMap(["activationBlockedStrenght", "warpScrambleStrength"], stats, mod)
            elif mod.item.group.name == "Warp Disrupt Field Generator":
                maxRangeDefault = mod.getModifiedItemAttr("warpScrambleRange")
                stats["type"] = "Warp Scrambler"
                EfsPort.attrDirectMap(["activationBlockedStrenght", "warpScrambleStrength"], stats, mod)
                if maxRangeDefault >= 30000:
                    # We want this to be 0 for disruption scripts as we have no other way to tell scrams from points.
                    stats["activationBlockedStrenght"] = 0
            elif mod.item.group.name == "Target Painter":
                stats["type"] = "Target Painter"
                EfsPort.attrDirectMap(["signatureRadiusBonus"], stats, mod)
            elif mod.item.group.name == "Sensor Dampener":
                stats["type"] = "Sensor Dampener"
                EfsPort.attrDirectMap(["maxTargetRangeBonus", "scanResolutionBonus"], stats, mod)
            elif mod.item.group.name == "ECM":
                stats["type"] = "ECM"
                EfsPort.attrDirectMap([
                    "scanGravimetricStrengthBonus", "scanMagnetometricStrengthBonus",
                    "scanRadarStrengthBonus", "scanLadarStrengthBonus",
                ], stats, mod)
            elif mod.item.group.name == "Burst Jammer":
                stats["type"] = "Burst Jammer"
                maxRangeDefault = mod.getModifiedItemAttr("ecmBurstRange")
                EfsPort.attrDirectMap([
                    "scanGravimetricStrengthBonus", "scanMagnetometricStrengthBonus",
                    "scanRadarStrengthBonus", "scanLadarStrengthBonus",
                ], stats, mod)
            elif mod.item.group.name == "Micro Jump Drive":
                stats["type"] = "Micro Jump Drive"
                EfsPort.attrDirectMap(["moduleReactivationDelay"], stats, mod)
            else:
                pyfalog.error("Projected module {0} lacks efs export implementation".format(mod.item.typeName))
            if mod.getModifiedItemAttr("maxRange", None) is None:
                pyfalog.error("Projected module {0} has no maxRange".format(mod.item.typeName))

            # Burst jammer maxRange is 0 if the value is retrieved using mod.getModifiedItemAttr("maxRange")
            # Despite it is correct, it still pulls 0.0.
            stats["optimal"] = mod.getModifiedItemAttr("maxRange", maxRangeDefault) if mod.item.group.name != "Burst Jammer" else mod.maxRange
            stats["falloff"] = mod.getModifiedItemAttr("falloffEffectiveness", falloffDefault)
            EfsPort.attrDirectMap(["duration", "capacitorNeed"], stats, mod)
            projections.append(stats)
        return projections

    # Note that unless padTypeIDs is True all 0s will be removed from modTypeIDs in the return.
    # They always are added initially for the sake of brevity, as this option may not be retained long term.
    @staticmethod
    def getModuleInfo(fit, padTypeIDs=False):
        moduleNames = []
        modTypeIDs = []
        moduleNameSets = {FittingSlot.LOW: [], FittingSlot.MED: [], FittingSlot.HIGH: [], FittingSlot.RIG: [], FittingSlot.SUBSYSTEM: []}
        modTypeIDSets = {FittingSlot.LOW: [], FittingSlot.MED: [], FittingSlot.HIGH: [], FittingSlot.RIG: [], FittingSlot.SUBSYSTEM: []}
        for mod in fit.modules:
            try:
                if mod.item is not None:
                    if mod.charge is not None:
                        modTypeIDSets[mod.slot].append([mod.item.typeID, mod.charge.typeID])
                        moduleNameSets[mod.slot].append(mod.item.typeName + ":  " + mod.charge.typeName)
                    else:
                        modTypeIDSets[mod.slot].append(mod.item.typeID)
                        moduleNameSets[mod.slot].append(mod.item.typeName)
                else:
                    modTypeIDSets[mod.slot].append(0)
                    moduleNameSets[mod.slot].append("Empty Slot")
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                pyfalog.error("Could not find name for module {0}".format(vars(mod)))

        for modInfo in [
            ["High Slots:"], moduleNameSets[FittingSlot.HIGH], ["", "Med Slots:"], moduleNameSets[FittingSlot.MED],
            ["", "Low Slots:"], moduleNameSets[FittingSlot.LOW], ["", "Rig Slots:"], moduleNameSets[FittingSlot.RIG]
        ]:
            moduleNames.extend(modInfo)
        if len(moduleNameSets[FittingSlot.SUBSYSTEM]) > 0:
            moduleNames.extend(["", "Subsystems:"])
            moduleNames.extend(moduleNameSets[FittingSlot.SUBSYSTEM])

        for slotType in [FittingSlot.HIGH, FittingSlot.MED, FittingSlot.LOW, FittingSlot.RIG, FittingSlot.SUBSYSTEM]:
            if slotType is not FittingSlot.SUBSYSTEM or len(modTypeIDSets[slotType]) > 0:
                modTypeIDs.extend([0, 0] if slotType is not FittingSlot.HIGH else [0])
                modTypeIDs.extend(modTypeIDSets[slotType])

        droneNames = []
        droneIDs = []
        fighterNames = []
        fighterIDs = []
        for drone in fit.drones:
            if drone.amountActive > 0:
                droneIDs.append(drone.item.typeID)
                droneNames.append("%s x%s" % (drone.item.typeName, drone.amount))
        for fighter in fit.fighters:
            if fighter.amount > 0:
                fighterIDs.append(fighter.item.typeID)
                fighterNames.append("%s x%s" % (fighter.item.typeName, fighter.amount))
        if len(droneNames) > 0:
            modTypeIDs.extend([0, 0])
            modTypeIDs.extend(droneIDs)
            moduleNames.extend(["", "Drones:"])
            moduleNames.extend(droneNames)
        if len(fighterNames) > 0:
            modTypeIDs.extend([0, 0])
            modTypeIDs.extend(fighterIDs)
            moduleNames.extend(["", "Fighters:"])
            moduleNames.extend(fighterNames)
        if len(fit.implants) > 0:
            modTypeIDs.extend([0, 0])
            moduleNames.extend(["", "Implants:"])
            for implant in fit.implants:
                modTypeIDs.append(implant.item.typeID)
                moduleNames.append(implant.item.typeName)
        if len(fit.boosters) > 0:
            modTypeIDs.extend([0, 0])
            moduleNames.extend(["", "Boosters:"])
            for booster in fit.boosters:
                modTypeIDs.append(booster.item.typeID)
                moduleNames.append(booster.item.typeName)
        if len(fit.commandFits) > 0:
            modTypeIDs.extend([0, 0])
            moduleNames.extend(["", "Command Fits:"])
            for commandFit in fit.commandFits:
                modTypeIDs.append(commandFit.ship.item.typeID)
                moduleNames.append(commandFit.name)
        if len(fit.projectedModules) > 0:
            modTypeIDs.extend([0, 0])
            moduleNames.extend(["", "Projected Modules:"])
            for mod in fit.projectedModules:
                modTypeIDs.append(mod.item.typeID)
                moduleNames.append(mod.item.typeName)

        if fit.character.name != "All 5":
            modTypeIDs.extend([0, 0, 0])
            moduleNames.extend(["", "Character:"])
            moduleNames.append(fit.character.name)
        if padTypeIDs is not True:
            modTypeIDsUnpadded = [mod for mod in modTypeIDs if mod != 0]
            modTypeIDs = modTypeIDsUnpadded
        return {"moduleNames": moduleNames, "modTypeIDs": modTypeIDs}

    @staticmethod
    def getFighterAbilityData(fighterAttr, fighter, baseRef):
        baseRefDam = baseRef + "Damage"
        abilityName = "RegularAttack" if baseRef == "fighterAbilityAttackMissile" else "MissileAttack"
        rangeSuffix = "RangeOptimal" if baseRef == "fighterAbilityAttackMissile" else "Range"
        reductionRef = baseRef if baseRef == "fighterAbilityAttackMissile" else baseRefDam
        damageReductionFactor = log(fighterAttr(reductionRef + "ReductionFactor")) / log(fighterAttr(reductionRef + "ReductionSensitivity"))
        damTypes = ["EM", "Therm", "Exp", "Kin"]
        abBaseDamage = sum(map(lambda damType: fighterAttr(baseRefDam + damType), damTypes))
        abDamage = abBaseDamage * fighterAttr(baseRefDam + "Multiplier")
        return {
            "name": abilityName, "volley": abDamage * fighter.amount, "explosionRadius": fighterAttr(baseRef + "ExplosionRadius"),
            "explosionVelocity": fighterAttr(baseRef + "ExplosionVelocity"), "optimal": fighterAttr(baseRef + rangeSuffix),
            "damageReductionFactor": damageReductionFactor, "rof": fighterAttr(baseRef + "Duration"),
        }

    @staticmethod
    def getWeaponSystemData(fit):
        weaponSystems = []
        groups = {}
        # Export at maximum spool for consistency, spoolup data is exported anyway.
        defaultSpoolValue = 1
        spoolOptions = SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, True)
        for mod in fit.modules:
            if mod.getDps(spoolOptions=spoolOptions).total > 0:
                # Group weapon + ammo combinations that occur more than once
                keystr = str(mod.itemID) + "-" + str(mod.chargeID)
                if keystr in groups:
                    groups[keystr][1] += 1
                else:
                    groups[keystr] = [mod, 1]
        for wepGroup in groups.values():
            stats = wepGroup[0]
            n = wepGroup[1]
            tracking = 0
            optimalSigRadius = 0
            maxVelocity = 0
            explosionDelay = 0
            damageReductionFactor = 0
            explosionRadius = 0
            explosionVelocity = 0
            aoeFieldRange = 0
            typeing = 'None'
            if stats.charge:
                name = stats.item.typeName + ", " + stats.charge.typeName
            else:
                name = stats.item.typeName
            if stats.hardpoint == FittingHardpoint.TURRET:
                tracking = stats.getModifiedItemAttr("trackingSpeed")
                optimalSigRadius = stats.getModifiedItemAttr('optimalSigRadius')
                typeing = "Turret"
            # Bombs share most attributes with missiles despite not needing the hardpoint
            elif stats.hardpoint == FittingHardpoint.MISSILE or "Bomb Launcher" in stats.item.typeName:
                maxVelocity = stats.getModifiedChargeAttr("maxVelocity")
                explosionDelay = stats.getModifiedChargeAttr("explosionDelay")
                damageReductionFactor = stats.getModifiedChargeAttr("aoeDamageReductionFactor")
                explosionRadius = stats.getModifiedChargeAttr("aoeCloudSize")
                explosionVelocity = stats.getModifiedChargeAttr("aoeVelocity")
                typeing = "Missile"
            # AoE DDs can be treated like missiles with a damageReductionFactor of 0
            elif stats.item.group.name == 'Super Weapon' and stats.maxRange:
                explosionRadius = stats.getModifiedItemAttr("signatureRadius")
                typeing = "Missile"
            elif stats.hardpoint == FittingHardpoint.NONE:
                aoeFieldRange = stats.getModifiedItemAttr("empFieldRange")
                # This also covers non-bomb weapons with dps values and no hardpoints, most notably targeted doomsdays.
                typeing = "SmartBomb"
            # Targeted DDs are the only non drone/fighter weapon without an explicit max range
            if stats.item.group.name == 'Super Weapon' and stats.maxRange is None:
                maxRange = 300000
            else:
                maxRange = stats.maxRange

            dps = stats.getDps(spoolOptions=spoolOptions)
            dps_spread_dict = {'em': dps.em, 'therm': dps.thermal, 'kin': dps.kinetic, 'exp': dps.explosive, 'pure': dps.pure}
            dps_spread_dict.update((x, y*n) for x, y in dps_spread_dict.items())

            statDict = {
                "dps": stats.getDps(spoolOptions=spoolOptions).total * n, "capUse": stats.capUse * n, "falloff": stats.falloff,
                "type": typeing, "name": name, "optimal": maxRange,
                "numCharges": stats.numCharges, "numShots": stats.numShots, "reloadTime": stats.reloadTime,
                "cycleTime": stats.getCycleParameters().averageTime, "volley": stats.getVolley(spoolOptions=spoolOptions).total * n, "tracking": tracking,
                "maxVelocity": maxVelocity, "explosionDelay": explosionDelay, "damageReductionFactor": damageReductionFactor,
                "explosionRadius": explosionRadius, "explosionVelocity": explosionVelocity, "aoeFieldRange": aoeFieldRange,
                "damageMultiplierBonusMax": stats.getModifiedItemAttr("damageMultiplierBonusMax"),
                "damageMultiplierBonusPerCycle": stats.getModifiedItemAttr("damageMultiplierBonusPerCycle"),
                "dps_spread": dps_spread_dict, "optimalSigRadius": optimalSigRadius
            }
            weaponSystems.append(statDict)
        for drone in fit.drones:
            if drone.getDps().total > 0 and drone.amountActive > 0:
                droneAttr = drone.getModifiedItemAttr
                # Drones are using the old tracking formula for trackingSpeed. This updates it to match turrets.
                newTracking = droneAttr("trackingSpeed") / (droneAttr("optimalSigRadius") / 40000)
                statDict = {
                    "dps": drone.getDps().total, "cycleTime": drone.getCycleParameters().averageTime, "type": "Drone",
                    "optimal": drone.maxRange, "name": drone.item.typeName, "falloff": drone.falloff,
                    "maxSpeed": droneAttr("maxVelocity"), "tracking": newTracking,
                    "volley": drone.getVolley().total
                }
                weaponSystems.append(statDict)
        for fighter in fit.fighters:
            if fighter.getDps().total > 0 and fighter.amount > 0:
                fighterAttr = fighter.getModifiedItemAttr
                abilities = []
                if "fighterAbilityAttackMissileDamageEM" in fighter.item.attributes.keys():
                    baseRef = "fighterAbilityAttackMissile"
                    ability = EfsPort.getFighterAbilityData(fighterAttr, fighter, baseRef)
                    abilities.append(ability)
                if "fighterAbilityMissilesDamageEM" in fighter.item.attributes.keys():
                    baseRef = "fighterAbilityMissiles"
                    ability = EfsPort.getFighterAbilityData(fighterAttr, fighter, baseRef)
                    abilities.append(ability)
                statDict = {
                    "dps": fighter.getDps().total, "type": "Fighter", "name": fighter.item.typeName,
                    "maxSpeed": fighterAttr("maxVelocity"), "abilities": abilities,
                    "ehp": fighterAttr("shieldCapacity") / 0.8875 * fighter.amount,
                    "volley": fighter.getVolley().total, "signatureRadius": fighterAttr("signatureRadius")
                }
                weaponSystems.append(statDict)
        return weaponSystems

    @staticmethod
    def getTestSet(setType):
        def getT2ItemsWhere(additionalFilter, mustBeOffensive=False, category="Module"):
            # Used to obtain a smaller subset of items while still containing examples of each group.
            T2_META_LEVEL = 5
            categoryID = getCategory(category).categoryID
            result = gamedata_session.query(Item).join(ItemEffect, Group, Attribute).\
                      filter(
                          additionalFilter,
                          Item.metaLevel == T2_META_LEVEL,
                          Group.categoryID == categoryID,
                      ).all()
            if mustBeOffensive:
                result = filter(lambda t: t.offensive is True, result)
            return list(result)

        def getChargeType(item, setType):
            if setType == "turret":
                return str(item.attributes["chargeGroup1"].value) + "-" + str(item.attributes["chargeSize"].value)
            return str(item.attributes["chargeGroup1"].value)

        if setType in EfsPort.wepTestSet.keys():
            return EfsPort.wepTestSet[setType]
        else:
            EfsPort.wepTestSet[setType] = []
        modSet = EfsPort.wepTestSet[setType]

        if setType == "drone":
            ilist = getT2ItemsWhere(True, True, "Drone")
            for item in ilist:
                drone = Drone(item)
                drone.amount = 1
                drone.amountActive = 1
                drone.itemModifiedAttributes.parent = drone
                modSet.append(drone)
            return modSet

        turretFittedEffectID = gamedata_session.query(Effect).filter(Effect.name == "turretFitted").first().effectID
        launcherFittedEffectID = gamedata_session.query(Effect).filter(Effect.name == "launcherFitted").first().effectID
        if setType == "launcher":
            effectFilter = ItemEffect.effectID == launcherFittedEffectID
            reqOff = False
        else:
            effectFilter = ItemEffect.effectID == turretFittedEffectID
            reqOff = True
        ilist = getT2ItemsWhere(effectFilter, reqOff)
        previousChargeTypes = []
        # Get modules from item list
        for item in ilist:
            chargeType = getChargeType(item, setType)
            # Only add turrets if we don"t already have one with the same size and ammo type.
            if setType == "launcher" or chargeType not in previousChargeTypes:
                previousChargeTypes.append(chargeType)
                mod = Module(item)
                modSet.append(mod)

        sMkt = Market.getInstance()
        # Due to typed missile damage bonuses we"ll need to add extra launchers to cover all four types.
        additionalLaunchers = []
        for mod in modSet:
            clist = list(gamedata_session.query(Item).options().
                    filter(Item.groupID == mod.getModifiedItemAttr("chargeGroup1")).all())
            mods = [mod]
            charges = [clist[0]]
            if setType == "launcher":
                # We don"t want variations of missiles we already have
                prevCharges = list(sMkt.getVariationsByItems(charges))
                testCharges = []
                for charge in clist:
                    if charge not in prevCharges:
                        testCharges.append(charge)
                        prevCharges += sMkt.getVariationsByItems([charge])
                for c in testCharges:
                    charges.append(c)
                    additionalLauncher = Module(mod.item)
                    mods.append(additionalLauncher)
            for i in range(len(mods)):
                mods[i].charge = charges[i]
                mods[i].reloadForce = True
                mods[i].state = 2
                if setType == "launcher" and i > 0:
                    additionalLaunchers.append(mods[i])
        modSet += additionalLaunchers
        return modSet

    @staticmethod
    def getWeaponBonusMultipliers(fit):
        def sumDamage(attr):
            totalDamage = 0
            for damageType in ["emDamage", "thermalDamage", "kineticDamage", "explosiveDamage"]:
                if attr(damageType) is not None:
                    totalDamage += attr(damageType)
            return totalDamage

        def getCurrentMultipliers(tf):
            fitMultipliers = {}
            getDroneMulti = lambda d: sumDamage(d.getModifiedItemAttr) * d.getModifiedItemAttr("damageMultiplier")
            fitMultipliers["drones"] = list(map(getDroneMulti, tf.drones))

            getFitTurrets = lambda f: filter(lambda mod: mod.hardpoint == FittingHardpoint.TURRET, f.modules)
            getTurretMulti = lambda mod: mod.getModifiedItemAttr("damageMultiplier") / mod.getCycleParameters().averageTime
            fitMultipliers["turrets"] = list(map(getTurretMulti, getFitTurrets(tf)))

            getFitLaunchers = lambda f: filter(lambda mod: mod.hardpoint == FittingHardpoint.MISSILE, f.modules)
            getLauncherMulti = lambda mod: sumDamage(mod.getModifiedChargeAttr) / mod.getCycleParameters().averageTime
            fitMultipliers["launchers"] = list(map(getLauncherMulti, getFitLaunchers(tf)))
            return fitMultipliers

        multipliers = {"turret": 1, "launcher": 1, "droneBandwidth": 1}
        drones = EfsPort.getTestSet("drone")
        launchers = EfsPort.getTestSet("launcher")
        turrets = EfsPort.getTestSet("turret")
        for weaponTypeSet in [turrets, launchers, drones]:
            for mod in weaponTypeSet:
                mod.owner = fit
        turrets = list(filter(lambda mod: mod.getModifiedItemAttr("damageMultiplier"), turrets))
        launchers = list(filter(lambda mod: sumDamage(mod.getModifiedChargeAttr), launchers))

        # Since the effect modules are fairly opaque a mock test fit is used to test the impact of traits.
        # standin class used to prevent . notation causing issues when used as an arg
        class standin:
            pass
        tf = standin()
        tf.modules = HandledList(turrets + launchers)
        tf.character = fit.character
        tf.ship = fit.ship
        tf.drones = HandledList(drones)
        tf.fighters = HandledList([])
        tf.boosters = HandledList([])
        tf.extraAttributes = fit.extraAttributes
        tf.mode = fit.mode
        preTraitMultipliers = getCurrentMultipliers(tf)
        for effect in fit.ship.item.effects.values():
            if effect.isImplemented:
                effect.handler(tf, tf.ship, [], None, effect=effect)
        # Factor in mode effects for T3 Destroyers
        if fit.mode is not None:
            for effect in fit.mode.item.effects.values():
                if effect.isImplemented:
                    effect.handler(tf, fit.mode, [], None, effect=effect)
        if fit.ship.item.groupID == getGroup("Strategic Cruiser").ID:
            subSystems = list(filter(lambda mod: mod.slot == FittingSlot.SUBSYSTEM and mod.item, fit.modules))
            for sub in subSystems:
                for effect in sub.item.effects.values():
                    if effect.isImplemented:
                        effect.handler(tf, sub, [], None, effect=effect)
        postTraitMultipliers = getCurrentMultipliers(tf)
        getMaxRatio = lambda dictA, dictB, key: max(map(lambda a, b: b / a, dictA[key], dictB[key]))
        multipliers["turret"] = round(getMaxRatio(preTraitMultipliers, postTraitMultipliers, "turrets"), 6)
        multipliers["launcher"] = round(getMaxRatio(preTraitMultipliers, postTraitMultipliers, "launchers"), 6)
        multipliers["droneBandwidth"] = round(getMaxRatio(preTraitMultipliers, postTraitMultipliers, "drones"), 6)
        Fit.getInstance().recalc(fit)
        return multipliers

    @staticmethod
    def getShipSize(groupID):
        # Size groupings are somewhat arbitrary but allow for a more manageable number of top level groupings in a tree structure.
        frigateGroupNames = ["Frigate", "Shuttle", "Corvette", "Assault Frigate", "Covert Ops", "Interceptor",
                             "Stealth Bomber", "Electronic Attack Ship", "Expedition Frigate", "Logistics Frigate"]
        destroyerGroupNames = ["Destroyer", "Interdictor", "Tactical Destroyer", "Command Destroyer"]
        cruiserGroupNames = ["Cruiser", "Heavy Assault Cruiser", "Logistics", "Force Recon Ship",
                             "Heavy Interdiction Cruiser", "Combat Recon Ship", "Strategic Cruiser"]
        bcGroupNames = ["Combat Battlecruiser", "Command Ship", "Attack Battlecruiser"]
        bsGroupNames = ["Battleship", "Elite Battleship", "Black Ops", "Marauder"]
        capitalGroupNames = ["Titan", "Dreadnought", "Freighter", "Carrier", "Supercarrier",
                             "Capital Industrial Ship", "Jump Freighter", "Force Auxiliary"]
        indyGroupNames = ["Hauler", "Deep Space Transport", "Blockade Runner",
                          "Mining Barge", "Exhumer", "Industrial Command Ship"]
        miscGroupNames = ["Capsule", "Prototype Exploration Ship"]
        shipSizes = [
            {"name": "Frigate", "groupIDs": map(lambda s: getGroup(s).ID, frigateGroupNames)},
            {"name": "Destroyer", "groupIDs": map(lambda s: getGroup(s).ID, destroyerGroupNames)},
            {"name": "Cruiser", "groupIDs": map(lambda s: getGroup(s).ID, cruiserGroupNames)},
            {"name": "Battlecruiser", "groupIDs": map(lambda s: getGroup(s).ID, bcGroupNames)},
            {"name": "Battleship", "groupIDs": map(lambda s: getGroup(s).ID, bsGroupNames)},
            {"name": "Capital", "groupIDs": map(lambda s: getGroup(s).ID, capitalGroupNames)},
            {"name": "Industrial", "groupIDs": map(lambda s: getGroup(s).ID, indyGroupNames)},
            {"name": "Misc", "groupIDs": map(lambda s: getGroup(s).ID, miscGroupNames)}
        ]
        for size in shipSizes:
            if groupID in size["groupIDs"]:
                return size["name"]
        sizeNotFoundMsg = "ShipSize not found for groupID: " + str(groupID)
        return sizeNotFoundMsg

    @staticmethod
    def exportEfs(fit, typeNotFitFlag, callback):
        sFit = Fit.getInstance()
        includeShipTypeData = typeNotFitFlag > 0
        if includeShipTypeData:
            fitName = fit.name
        else:
            fitName = fit.ship.name + ": " + fit.name
        pyfalog.info("Creating Eve Fleet Simulator data for: " + fit.name)
        fitModAttr = fit.ship.getModifiedItemAttr
        propData = EfsPort.getPropData(fit, sFit)
        mwdPropSpeed = fit.maxSpeed
        if includeShipTypeData:
            mwdPropSpeed = EfsPort.getT2MwdSpeed(fit, sFit)
        projections = EfsPort.getOutgoingProjectionData(fit)
        modInfo = EfsPort.getModuleInfo(fit)
        moduleNames = modInfo["moduleNames"]
        modTypeIDs = modInfo["modTypeIDs"]
        weaponSystems = EfsPort.getWeaponSystemData(fit)


        turretSlots = fitModAttr("turretSlotsLeft") if fitModAttr("turretSlotsLeft") is not None else 0
        launcherSlots = fitModAttr("launcherSlotsLeft") if fitModAttr("launcherSlotsLeft") is not None else 0
        droneBandwidth = fitModAttr("droneBandwidth") if fitModAttr("droneBandwidth") is not None else 0
        weaponBonusMultipliers = EfsPort.getWeaponBonusMultipliers(fit)
        effectiveTurretSlots = round(turretSlots * weaponBonusMultipliers["turret"], 2)
        effectiveLauncherSlots = round(launcherSlots * weaponBonusMultipliers["launcher"], 2)
        effectiveDroneBandwidth = round(droneBandwidth * weaponBonusMultipliers["droneBandwidth"], 2)
        # Assume a T2 siege module for dreads
        if fit.ship.item.group.name == "Dreadnought":
            effectiveTurretSlots *= 9.4
            effectiveLauncherSlots *= 15
        hullResonance = {
            "exp": fitModAttr("explosiveDamageResonance"), "kin": fitModAttr("kineticDamageResonance"),
            "therm": fitModAttr("thermalDamageResonance"), "em": fitModAttr("emDamageResonance")
        }
        armorResonance = {
            "exp": fitModAttr("armorExplosiveDamageResonance"), "kin": fitModAttr("armorKineticDamageResonance"),
            "therm": fitModAttr("armorThermalDamageResonance"), "em": fitModAttr("armorEmDamageResonance")
        }
        shieldResonance = {
            "exp": fitModAttr("shieldExplosiveDamageResonance"), "kin": fitModAttr("shieldKineticDamageResonance"),
            "therm": fitModAttr("shieldThermalDamageResonance"), "em": fitModAttr("shieldEmDamageResonance")
        }

        resonance = {"hull": hullResonance, "armor": armorResonance, "shield": shieldResonance}
        shipSize = EfsPort.getShipSize(fit.ship.item.groupID)
        # Export at maximum spool for consistency, spoolup data is exported anyway.
        defaultSpoolValue = 1
        spoolOptions = SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, True)

        cargoIDs = []
        for cargo in fit.cargo:
            cargoIDs.append(cargo.itemID)

        repairs = EfsPort.getRepairData(fit, sFit)

        def roundNumbers(data, digits):
            if isinstance(data, str):
                return
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], Number):
                        data[key] = round(data[key], digits)
                    else:
                        roundNumbers(data[key], digits)
            if isinstance(data, list) or isinstance(data, tuple):
                for val in data:
                    roundNumbers(val, digits)
            if isinstance(data, Number):
                rounded = round(data, digits)
                if data != rounded:
                    pyfalog.error("Error rounding numbers for EFS export, export may be inconsistent."
                                  "This suggests the format has been broken somewhere.")
            return

        try:
            dataDict = {
                "name": fitName, "ehp": fit.ehp, "droneDPS": fit.getDroneDps().total,
                "droneVolley": fit.getDroneVolley().total, "hp": fit.hp, "maxTargets": fit.maxTargets,
                "maxSpeed": fit.maxSpeed, "weaponVolley": fit.getWeaponVolley(spoolOptions=spoolOptions).total,
                "totalVolley": fit.getTotalVolley(spoolOptions=spoolOptions).total, "maxTargetRange": fit.maxTargetRange,
                "scanStrength": fit.scanStrength, "weaponDPS": fit.getWeaponDps(spoolOptions=spoolOptions).total,
                "alignTime": fit.alignTime, "signatureRadius": fitModAttr("signatureRadius"), "weapons": weaponSystems,
                "scanRes": fitModAttr("scanResolution"), "capUsed": fit.capUsed, "capRecharge": fit.capRecharge,
                "capacitorCapacity": fitModAttr("capacitorCapacity"), "rechargeRate": fitModAttr("rechargeRate"),
                "rigSlots": fitModAttr("rigSlots"), "lowSlots": fitModAttr("lowSlots"),
                "midSlots": fitModAttr("medSlots"), "highSlots": fitModAttr("hiSlots"),
                "turretSlots": fitModAttr("turretSlotsLeft"), "launcherSlots": fitModAttr("launcherSlotsLeft"),
                "powerOutput": fitModAttr("powerOutput"), "cpuOutput": fitModAttr("cpuOutput"),
                "rigSize": fitModAttr("rigSize"), "effectiveTurrets": effectiveTurretSlots,
                "effectiveLaunchers": effectiveLauncherSlots, "effectiveDroneBandwidth": effectiveDroneBandwidth,
                "resonance": resonance, "typeID": fit.shipID, "groupID": fit.ship.item.groupID, "shipSize": shipSize,
                "droneControlRange": fitModAttr("droneControlRange"), "mass": fitModAttr("mass"),
                "shieldrechargetime": fitModAttr("shieldRechargeRate"), 'shipinertia': fitModAttr("agility"),
                "energyWarfareResistance": fitModAttr("energyWarfareResistance"),
                "unpropedSpeed": propData["unpropedSpeed"], "unpropedSig": propData["unpropedSig"],
                "usingMWD": propData["usingMWD"], "mwdPropSpeed": mwdPropSpeed, "projections": projections,
                "repairs": repairs, "modTypeIDs": modTypeIDs, "moduleNames": moduleNames, "cargoItemIDs": cargoIDs,
                "pyfaVersion": pyfaVersion, "efsExportVersion": EfsPort.version
            }
            # Recursively round any numbers in dicts to 6 decimal places.
            # This prevents meaningless rounding errors from changing the output whenever pyfa changes.
            roundNumbers(dataDict, 6)
        except TypeError as e:
            pyfalog.error("Error parsing fit:" + str(fit))
            pyfalog.error(e)
            dataDict = {"name": fitName + "Fit could not be correctly parsed"}
        export = json.dumps(dataDict, skipkeys=True)

        if callback:
            callback(export)
        else:
            return export
