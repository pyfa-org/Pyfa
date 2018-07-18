import inspect
import os
import platform
import re
import sys
import traceback
import json
import eos.db

from math import log
from service.fit import Fit
from service.market import Market
from eos.enum import Enum
from eos.saveddata.module import Hardpoint, Slot, Module
from eos.saveddata.drone import Drone
from eos.effectHandlerHelpers import HandledList
from eos.db import gamedata_session, getItemsByCategory, getCategory, getAttributeInfo, getGroup
from eos.gamedata import Category, Group, Item, Traits, Attribute, Effect, ItemEffect
from logbook import Logger
pyfalog = Logger(__name__)
eos.db.saveddata_meta.create_all()


class RigSize(Enum):
    # Matches to item attribute "rigSize" on ship and rig items
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    CAPITAL = 4


class EfsPort():
    wepTestSet = {}

    @staticmethod
    def attrDirectMap(values, target, source):
        for val in values:
            target[val] = source.itemModifiedAttributes[val]

    @staticmethod
    def getT2MwdSpeed(fit, sFit):
        fitID = fit.ID
        propID = None
        shipHasMedSlots = fit.ship.itemModifiedAttributes["medSlots"] > 0
        shipPower = fit.ship.itemModifiedAttributes["powerOutput"]
        # Monitors have a 99% reduction to prop mod power requirements
        if fit.ship.name == "Monitor":
            shipPower *= 100
        rigSize = fit.ship.itemModifiedAttributes["rigSize"]
        if not shipHasMedSlots:
            return None

        filterVal = Item.groupID == getGroup("Propulsion Module").ID
        propMods = gamedata_session.query(Item).options().filter(filterVal).all()
        mapPropData = lambda propName: \
                      next(map(lambda propMod: {"id": propMod.typeID, "powerReq": propMod.attributes["power"].value},
                               (filter(lambda mod: mod.name == propName, propMods))))
        mwd5mn = mapPropData("5MN Microwarpdrive II")
        mwd50mn = mapPropData("50MN Microwarpdrive II")
        mwd500mn = mapPropData("500MN Microwarpdrive II")
        mwd50000mn = mapPropData("50000MN Microwarpdrive II")
        if rigSize == RigSize.SMALL or rigSize is None:
            propID = mwd5mn["id"] if shipPower > mwd5mn["powerReq"] else None
        elif rigSize == RigSize.MEDIUM:
            propID = mwd50mn["id"] if shipPower > mwd50mn["powerReq"] else mwd5mn["id"]
        elif rigSize == RigSize.LARGE:
            propID = mwd500mn["id"] if shipPower > mwd500mn["powerReq"] else mwd50mn["id"]
        elif rigSize == RigSize.CAPITAL:
            propID = mwd50000mn["id"] if shipPower > mwd50000mn["powerReq"] else mwd500mn["id"]

        if propID is None:
            return None
        sFit.appendModule(fitID, propID)
        sFit.recalc(fit)
        fit = eos.db.getFit(fitID)
        mwdPropSpeed = fit.maxSpeed
        mwdPosition = list(filter(lambda mod: mod.item and mod.item.ID == propID, fit.modules))[0].position
        sFit.removeModule(fitID, mwdPosition)
        sFit.recalc(fit)
        fit = eos.db.getFit(fitID)
        return mwdPropSpeed

    @staticmethod
    def getPropData(fit, sFit):
        fitID = fit.ID
        propGroupId = getGroup("Propulsion Module").ID
        propMods = filter(lambda mod: mod.item and mod.item.groupID == propGroupId, fit.modules)
        activePropWBloomFilter = lambda mod: mod.state > 0 and "signatureRadiusBonus" in mod.item.attributes
        propWithBloom = next(filter(activePropWBloomFilter, propMods), None)
        if propWithBloom is not None:
            oldPropState = propWithBloom.state
            propWithBloom.state = 0
            sFit.recalc(fit)
            fit = eos.db.getFit(fitID)
            sp = fit.maxSpeed
            sig = fit.ship.itemModifiedAttributes["signatureRadius"]
            propWithBloom.state = oldPropState
            sFit.recalc(fit)
            fit = eos.db.getFit(fitID)
            return {"usingMWD": True, "unpropedSpeed": sp, "unpropedSig": sig}
        return {
            "usingMWD": False,
            "unpropedSpeed": fit.maxSpeed,
            "unpropedSig": fit.ship.itemModifiedAttributes["signatureRadius"]
        }

    @staticmethod
    def getOutgoingProjectionData(fit):
        # This is a subset of module groups capable of projection and a superset of those currently used by efs
        modGroupNames = [
            "Remote Shield Booster", "Warp Scrambler", "Stasis Web", "Remote Capacitor Transmitter",
            "Energy Nosferatu", "Energy Neutralizer", "Burst Jammer", "ECM", "Sensor Dampener",
            "Weapon Disruptor", "Remote Armor Repairer", "Target Painter", "Remote Hull Repairer",
            "Burst Projectors", "Warp Disrupt Field Generator", "Armor Resistance Shift Hardener",
            "Target Breaker", "Micro Jump Drive", "Ship Modifiers", "Stasis Grappler",
            "Ancillary Remote Shield Booster", "Ancillary Remote Armor Repairer",
            "Titan Phenomena Generator", "Non-Repeating Hardeners"
        ]
        modGroupIds = list(map(lambda s: getGroup(s).ID, modGroupNames))
        modGroupData = dict(map(lambda name, gid: (name, {"name": name, "id": gid}),
                                    modGroupNames, modGroupIds))
        projectedMods = list(filter(lambda mod: mod.item and mod.item.groupID in modGroupIds, fit.modules))
        projections = []
        for mod in projectedMods:
            stats = {}
            if mod.item.groupID in [modGroupData["Stasis Web"]["id"], modGroupData["Stasis Grappler"]["id"]]:
                stats["type"] = "Stasis Web"
                stats["optimal"] = mod.itemModifiedAttributes["maxRange"]
                EfsPort.attrDirectMap(["duration", "speedFactor"], stats, mod)
            elif mod.item.groupID == modGroupData["Weapon Disruptor"]["id"]:
                stats["type"] = "Weapon Disruptor"
                stats["optimal"] = mod.itemModifiedAttributes["maxRange"]
                stats["falloff"] = mod.itemModifiedAttributes["falloffEffectiveness"]
                EfsPort.attrDirectMap([
                    "trackingSpeedBonus", "maxRangeBonus", "falloffBonus", "aoeCloudSizeBonus",
                    "aoeVelocityBonus", "missileVelocityBonus", "explosionDelayBonus"
                ], stats, mod)
            elif mod.item.groupID == modGroupData["Energy Nosferatu"]["id"]:
                stats["type"] = "Energy Nosferatu"
                EfsPort.attrDirectMap(["powerTransferAmount", "energyNeutralizerSignatureResolution"], stats, mod)
            elif mod.item.groupID == modGroupData["Energy Neutralizer"]["id"]:
                stats["type"] = "Energy Neutralizer"
                EfsPort.attrDirectMap([
                    "energyNeutralizerSignatureResolution", "entityCapacitorLevelModifierSmall",
                    "entityCapacitorLevelModifierMedium", "entityCapacitorLevelModifierLarge",
                    "energyNeutralizerAmount"
                ], stats, mod)
            elif mod.item.groupID in [modGroupData["Remote Shield Booster"]["id"],
                                      modGroupData["Ancillary Remote Shield Booster"]["id"]]:
                stats["type"] = "Remote Shield Booster"
                EfsPort.attrDirectMap(["shieldBonus"], stats, mod)
            elif mod.item.groupID in [modGroupData["Remote Armor Repairer"]["id"],
                                      modGroupData["Ancillary Remote Armor Repairer"]["id"]]:
                stats["type"] = "Remote Armor Repairer"
                EfsPort.attrDirectMap(["armorDamageAmount"], stats, mod)
            elif mod.item.groupID == modGroupData["Warp Scrambler"]["id"]:
                stats["type"] = "Warp Scrambler"
                EfsPort.attrDirectMap(["activationBlockedStrenght", "warpScrambleStrength"], stats, mod)
            elif mod.item.groupID == modGroupData["Target Painter"]["id"]:
                stats["type"] = "Target Painter"
                EfsPort.attrDirectMap(["signatureRadiusBonus"], stats, mod)
            elif mod.item.groupID == modGroupData["Sensor Dampener"]["id"]:
                stats["type"] = "Sensor Dampener"
                EfsPort.attrDirectMap(["maxTargetRangeBonus", "scanResolutionBonus"], stats, mod)
            elif mod.item.groupID == modGroupData["ECM"]["id"]:
                stats["type"] = "ECM"
                EfsPort.attrDirectMap([
                    "scanGravimetricStrengthBonus", "scanMagnetometricStrengthBonus",
                    "scanRadarStrengthBonus", "scanLadarStrengthBonus",
                ], stats, mod)
            elif mod.item.groupID == modGroupData["Burst Jammer"]["id"]:
                stats["type"] = "Burst Jammer"
                mod.itemModifiedAttributes["maxRange"] = mod.itemModifiedAttributes["ecmBurstRange"]
                EfsPort.attrDirectMap([
                    "scanGravimetricStrengthBonus", "scanMagnetometricStrengthBonus",
                    "scanRadarStrengthBonus", "scanLadarStrengthBonus",
                ], stats, mod)
            elif mod.item.groupID == modGroupData["Micro Jump Drive"]["id"]:
                stats["type"] = "Micro Jump Drive"
                mod.itemModifiedAttributes["maxRange"] = 0
                EfsPort.attrDirectMap(["moduleReactivationDelay"], stats, mod)
            if mod.itemModifiedAttributes["maxRange"] is None:
                pyfalog.error("Projected module {0} has no maxRange".format(mod.item.name))
            stats["optimal"] = mod.itemModifiedAttributes["maxRange"] or 0
            stats["falloff"] = mod.itemModifiedAttributes["falloffEffectiveness"] or 0
            EfsPort.attrDirectMap(["duration", "capacitorNeed"], stats, mod)
            projections.append(stats)
        return projections

    @staticmethod
    def getModuleNames(fit):
        moduleNames = []
        highSlotNames = []
        midSlotNames = []
        lowSlotNames = []
        rigSlotNames = []
        miscSlotNames = []  # subsystems ect
        for mod in fit.modules:
            if mod.slot == 3:
                modSlotNames = highSlotNames
            elif mod.slot == 2:
                modSlotNames = midSlotNames
            elif mod.slot == 1:
                modSlotNames = lowSlotNames
            elif mod.slot == 4:
                modSlotNames = rigSlotNames
            elif mod.slot == 5:
                modSlotNames = miscSlotNames
            try:
                if mod.item is not None:
                    if mod.charge is not None:
                        modSlotNames.append(mod.item.name + ":  " + mod.charge.name)
                    else:
                        modSlotNames.append(mod.item.name)
                else:
                    modSlotNames.append("Empty Slot")
            except:
                pyfalog.error("Could not find name for module {0}".format(vars(mod)))
        for modInfo in [
            ["High Slots:"], highSlotNames, ["", "Med Slots:"], midSlotNames,
            ["", "Low Slots:"], lowSlotNames, ["", "Rig Slots:"], rigSlotNames
        ]:
            moduleNames.extend(modInfo)

        if len(miscSlotNames) > 0:
            moduleNames.append("")
            moduleNames.append("Subsystems:")
            moduleNames.extend(miscSlotNames)
        droneNames = []
        fighterNames = []
        for drone in fit.drones:
            if drone.amountActive > 0:
                droneNames.append("%s x%s" % (drone.item.name, drone.amount))
        for fighter in fit.fighters:
            if fighter.amountActive > 0:
                fighterNames.append("%s x%s" % (fighter.item.name, fighter.amountActive))
        if len(droneNames) > 0:
            moduleNames.append("")
            moduleNames.append("Drones:")
            moduleNames.extend(droneNames)
        if len(fighterNames) > 0:
            moduleNames.append("")
            moduleNames.append("Fighters:")
            moduleNames.extend(fighterNames)
        if len(fit.implants) > 0:
            moduleNames.append("")
            moduleNames.append("Implants:")
            for implant in fit.implants:
                moduleNames.append(implant.item.name)
        if len(fit.boosters) > 0:
            moduleNames.append("")
            moduleNames.append("Boosters:")
            for booster in fit.boosters:
                moduleNames.append(booster.item.name)
        if len(fit.commandFits) > 0:
            moduleNames.append("")
            moduleNames.append("Command Fits:")
            for commandFit in fit.commandFits:
                moduleNames.append(commandFit.name)
        if len(fit.projectedModules) > 0:
            moduleNames.append("")
            moduleNames.append("Projected Modules:")
            for mod in fit.projectedModules:
                moduleNames.append(mod.item.name)

        if fit.character.name != "All 5":
            moduleNames.append("")
            moduleNames.append("Character:")
            moduleNames.append(fit.character.name)

        return moduleNames

    @staticmethod
    def getFighterAbilityData(fighterAttr, fighter, baseRef):
        baseRefDam = baseRef + "Damage"
        abilityName = "RegularAttack" if baseRef == "fighterAbilityAttackMissile" else "MissileAttack"
        rangeSuffix = "RangeOptimal" if baseRef == "fighterAbilityAttackMissile" else "Range"
        reductionRef = baseRef if baseRef == "fighterAbilityAttackMissile" else baseRefDam
        damageReductionFactor = log(fighterAttr[reductionRef + "ReductionFactor"]) / log(fighterAttr[reductionRef + "ReductionSensitivity"])
        damTypes = ["EM", "Therm", "Exp", "Kin"]
        abBaseDamage = sum(map(lambda damType: fighterAttr[baseRefDam + damType], damTypes))
        abDamage = abBaseDamage * fighterAttr[baseRefDam + "Multiplier"]
        return {
            "name": abilityName, "volley": abDamage * fighter.amountActive, "explosionRadius": fighterAttr[baseRef + "ExplosionRadius"],
            "explosionVelocity": fighterAttr[baseRef + "ExplosionVelocity"], "optimal": fighterAttr[baseRef + rangeSuffix],
            "damageReductionFactor": damageReductionFactor, "rof": fighterAttr[baseRef + "Duration"],
        }

    @staticmethod
    def getWeaponSystemData(fit):
        weaponSystems = []
        groups = {}
        for mod in fit.modules:
            if mod.dps > 0:
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
            maxVelocity = 0
            explosionDelay = 0
            damageReductionFactor = 0
            explosionRadius = 0
            explosionVelocity = 0
            aoeFieldRange = 0
            if stats.hardpoint == Hardpoint.TURRET:
                tracking = stats.itemModifiedAttributes["trackingSpeed"]
                typeing = "Turret"
                name = stats.item.name + ", " + stats.charge.name
            # Bombs share most attributes with missiles despite not needing the hardpoint
            elif stats.hardpoint == Hardpoint.MISSILE or "Bomb Launcher" in stats.item.name:
                maxVelocity = stats.chargeModifiedAttributes["maxVelocity"]
                explosionDelay = stats.chargeModifiedAttributes["explosionDelay"]
                damageReductionFactor = stats.chargeModifiedAttributes["aoeDamageReductionFactor"]
                explosionRadius = stats.chargeModifiedAttributes["aoeCloudSize"]
                explosionVelocity = stats.chargeModifiedAttributes["aoeVelocity"]
                typeing = "Missile"
                name = stats.item.name + ", " + stats.charge.name
            elif stats.hardpoint == Hardpoint.NONE:
                aoeFieldRange = stats.itemModifiedAttributes["empFieldRange"]
                # This also covers non-bomb weapons with dps values and no hardpoints, most notably targeted doomsdays.
                typeing = "SmartBomb"
                name = stats.item.name
            statDict = {
                "dps": stats.dps * n, "capUse": stats.capUse * n, "falloff": stats.falloff,
                "type": typeing, "name": name, "optimal": stats.maxRange,
                "numCharges": stats.numCharges, "numShots": stats.numShots, "reloadTime": stats.reloadTime,
                "cycleTime": stats.cycleTime, "volley": stats.volley * n, "tracking": tracking,
                "maxVelocity": maxVelocity, "explosionDelay": explosionDelay, "damageReductionFactor": damageReductionFactor,
                "explosionRadius": explosionRadius, "explosionVelocity": explosionVelocity, "aoeFieldRange": aoeFieldRange
            }
            weaponSystems.append(statDict)
        for drone in fit.drones:
            if drone.dps[0] > 0 and drone.amountActive > 0:
                droneAttr = drone.itemModifiedAttributes
                # Drones are using the old tracking formula for trackingSpeed. This updates it to match turrets.
                newTracking = droneAttr["trackingSpeed"] / (droneAttr["optimalSigRadius"] / 40000)
                statDict = {
                    "dps": drone.dps[0], "cycleTime": drone.cycleTime, "type": "Drone",
                    "optimal": drone.maxRange, "name": drone.item.name, "falloff": drone.falloff,
                    "maxSpeed": droneAttr["maxVelocity"], "tracking": newTracking,
                    "volley": drone.dps[1]
                }
                weaponSystems.append(statDict)
        for fighter in fit.fighters:
            if fighter.dps[0] > 0 and fighter.amountActive > 0:
                fighterAttr = fighter.itemModifiedAttributes
                abilities = []
                if "fighterAbilityAttackMissileDamageEM" in fighterAttr:
                    baseRef = "fighterAbilityAttackMissile"
                    ability = EfsPort.getFighterAbilityData(fighterAttr, fighter, baseRef)
                    abilities.append(ability)
                if "fighterAbilityMissilesDamageEM" in fighterAttr:
                    baseRef = "fighterAbilityMissiles"
                    ability = EfsPort.getFighterAbilityData(fighterAttr, fighter, baseRef)
                    abilities.append(ability)
                statDict = {
                    "dps": fighter.dps[0], "type": "Fighter", "name": fighter.item.name,
                    "maxSpeed": fighterAttr["maxVelocity"], "abilities": abilities,
                    "ehp": fighterAttr["shieldCapacity"] / 0.8875 * fighter.amountActive,
                    "volley": fighter.dps[1], "signatureRadius": fighterAttr["signatureRadius"]
                }
                weaponSystems.append(statDict)
        return weaponSystems

    @staticmethod
    def getTestSet(setType):
        def getT2ItemsWhere(additionalFilter, mustBeOffensive=False, category="Module"):
            # Used to obtain a smaller subset of items while still containing examples of each group.
            T2_META_LEVEL = 5
            metaLevelAttrID = getAttributeInfo("metaLevel").attributeID
            categoryID = getCategory(category).categoryID
            result = gamedata_session.query(Item).join(ItemEffect, Group, Attribute).\
                      filter(
                          additionalFilter,
                          Attribute.attributeID == metaLevelAttrID,
                          Attribute.value == T2_META_LEVEL,
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
                    filter(Item.groupID == mod.itemModifiedAttributes["chargeGroup1"]).all())
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
                if attr[damageType] is not None:
                    totalDamage += attr[damageType]
            return totalDamage

        def getCurrentMultipliers(tf):
            fitMultipliers = {}
            getDroneMulti = lambda d: sumDamage(d.itemModifiedAttributes) * d.itemModifiedAttributes["damageMultiplier"]
            fitMultipliers["drones"] = list(map(getDroneMulti, tf.drones))

            getFitTurrets = lambda f: filter(lambda mod: mod.hardpoint == Hardpoint.TURRET, f.modules)
            getTurretMulti = lambda mod: mod.itemModifiedAttributes["damageMultiplier"] / mod.cycleTime
            fitMultipliers["turrets"] = list(map(getTurretMulti, getFitTurrets(tf)))

            getFitLaunchers = lambda f: filter(lambda mod: mod.hardpoint == Hardpoint.MISSILE, f.modules)
            getLauncherMulti = lambda mod: sumDamage(mod.chargeModifiedAttributes) / mod.cycleTime
            fitMultipliers["launchers"] = list(map(getLauncherMulti, getFitLaunchers(tf)))
            return fitMultipliers

        multipliers = {"turret": 1, "launcher": 1, "droneBandwidth": 1}
        drones = EfsPort.getTestSet("drone")
        launchers = EfsPort.getTestSet("launcher")
        turrets = EfsPort.getTestSet("turret")
        for weaponTypeSet in [turrets, launchers, drones]:
            for mod in weaponTypeSet:
                mod.owner = fit
        turrets = list(filter(lambda mod: mod.itemModifiedAttributes["damageMultiplier"], turrets))
        launchers = list(filter(lambda mod: sumDamage(mod.chargeModifiedAttributes), launchers))
        # Since the effect modules are fairly opaque a mock test fit is used to test the impact of traits.
        # standin class used to prevent . notation causing issues internally
        class standin():
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
            if effect._Effect__effectModule is not None:
                effect.handler(tf, tf.ship, [])
        # Factor in mode effects for T3 Destroyers
        if fit.mode is not None:
            for effect in fit.mode.item.effects.values():
                if effect._Effect__effectModule is not None:
                    effect.handler(tf, fit.mode, [])
        if fit.ship.item.groupID == getGroup("Strategic Cruiser").ID:
            subSystems = list(filter(lambda mod: mod.slot == Slot.SUBSYSTEM and mod.item, fit.modules))
            for sub in subSystems:
                for effect in sub.item.effects.values():
                    if effect._Effect__effectModule is not None:
                        effect.handler(tf, sub, [])
        postTraitMultipliers = getCurrentMultipliers(tf)
        getMaxRatio = lambda dictA, dictB, key: max(map(lambda a, b: b / a, dictA[key], dictB[key]))
        multipliers["turret"] = round(getMaxRatio(preTraitMultipliers, postTraitMultipliers, "turrets"), 6)
        multipliers["launcher"] = round(getMaxRatio(preTraitMultipliers, postTraitMultipliers, "launchers"), 6)
        multipliers["droneBandwidth"] = round(getMaxRatio(preTraitMultipliers, postTraitMultipliers, "drones"), 6)
        Fit.getInstance().recalc(fit)
        return multipliers

    @staticmethod
    def getShipSize(groupID):
        # Size groupings are somewhat arbitrary but allow for a more managable number of top level groupings in a tree structure.
        frigateGroupNames = ["Frigate", "Shuttle", "Corvette", "Assault Frigate", "Covert Ops", "Interceptor",
                             "Stealth Bomber", "Electronic Attack Ship", "Expedition Frigate", "Logistics Frigate"]
        destroyerGroupNames = ["Destroyer", "Interdictor", "Tactical Destroyer", "Command Destroyer"]
        cruiserGroupNames = ["Cruiser", "Heavy Assault Cruiser", "Logistics", "Force Recon Ship",
                             "Heavy Interdiction Cruiser", "Combat Recon Ship", "Strategic Cruiser"]
        bcGroupNames = ["Combat Battlecruiser", "Command Ship", "Attack Battlecruiser"]
        bsGroupNames = ["Battleship", "Elite Battleship", "Black Ops", "Marauder"]
        capitalGroupNames = ["Titan", "Dreadnought", "Freighter", "Carrier", "Supercarrier",
                             "Capital Industrial Ship", "Jump Freighter", "Force Auxiliary"]
        indyGroupNames = ["Industrial", "Deep Space Transport", "Blockade Runner",
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
    def exportEfs(fit, groupID):
        includeShipTypeData = groupID > 0
        fitID = fit.ID
        if includeShipTypeData:
            fitName = fit.name
        else:
            fitName = fit.ship.name + ": " + fit.name
        pyfalog.info("Creating Eve Fleet Simulator data for: " + fit.name)
        sFit = Fit.getInstance()
        sFit.recalc(fit)
        fit = eos.db.getFit(fitID)
        fitModAttr = fit.ship.itemModifiedAttributes
        propData = EfsPort.getPropData(fit, sFit)
        mwdPropSpeed = fit.maxSpeed
        if includeShipTypeData:
            mwdPropSpeed = EfsPort.getT2MwdSpeed(fit, sFit)
        projections = EfsPort.getOutgoingProjectionData(fit)
        moduleNames = EfsPort.getModuleNames(fit)
        weaponSystems = EfsPort.getWeaponSystemData(fit)

        turretSlots = fitModAttr["turretSlotsLeft"] if fitModAttr["turretSlotsLeft"] is not None else 0
        launcherSlots = fitModAttr["launcherSlotsLeft"] if fitModAttr["launcherSlotsLeft"] is not None else 0
        droneBandwidth = fitModAttr["droneBandwidth"] if fitModAttr["droneBandwidth"] is not None else 0
        weaponBonusMultipliers = EfsPort.getWeaponBonusMultipliers(fit)
        effectiveTurretSlots = round(turretSlots * weaponBonusMultipliers["turret"], 2)
        effectiveLauncherSlots = round(launcherSlots * weaponBonusMultipliers["launcher"], 2)
        effectiveDroneBandwidth = round(droneBandwidth * weaponBonusMultipliers["droneBandwidth"], 2)
        # Assume a T2 siege module for dreads
        if groupID == getGroup("Dreadnought").ID:
            effectiveTurretSlots *= 9.4
            effectiveLauncherSlots *= 15
        hullResonance = {
            "exp": fitModAttr["explosiveDamageResonance"], "kin": fitModAttr["kineticDamageResonance"],
            "therm": fitModAttr["thermalDamageResonance"], "em": fitModAttr["emDamageResonance"]
        }
        armorResonance = {
            "exp": fitModAttr["armorExplosiveDamageResonance"], "kin": fitModAttr["armorKineticDamageResonance"],
            "therm": fitModAttr["armorThermalDamageResonance"], "em": fitModAttr["armorEmDamageResonance"]
        }
        shieldResonance = {
            "exp": fitModAttr["shieldExplosiveDamageResonance"], "kin": fitModAttr["shieldKineticDamageResonance"],
            "therm": fitModAttr["shieldThermalDamageResonance"], "em": fitModAttr["shieldEmDamageResonance"]
        }
        resonance = {"hull": hullResonance, "armor": armorResonance, "shield": shieldResonance}
        shipSize = EfsPort.getShipSize(fit.ship.item.groupID)

        try:
            dataDict = {
                "name": fitName, "ehp": fit.ehp, "droneDPS": fit.droneDPS,
                "droneVolley": fit.droneVolley, "hp": fit.hp, "maxTargets": fit.maxTargets,
                "maxSpeed": fit.maxSpeed, "weaponVolley": fit.weaponVolley, "totalVolley": fit.totalVolley,
                "maxTargetRange": fit.maxTargetRange, "scanStrength": fit.scanStrength,
                "weaponDPS": fit.weaponDPS, "alignTime": fit.alignTime, "signatureRadius": fitModAttr["signatureRadius"],
                "weapons": weaponSystems, "scanRes": fitModAttr["scanResolution"],
                "capUsed": fit.capUsed, "capRecharge": fit.capRecharge,
                "rigSlots": fitModAttr["rigSlots"], "lowSlots": fitModAttr["lowSlots"],
                "midSlots": fitModAttr["medSlots"], "highSlots": fitModAttr["hiSlots"],
                "turretSlots": fitModAttr["turretSlotsLeft"], "launcherSlots": fitModAttr["launcherSlotsLeft"],
                "powerOutput": fitModAttr["powerOutput"], "cpuOutput": fitModAttr["cpuOutput"],
                "rigSize": fitModAttr["rigSize"], "effectiveTurrets": effectiveTurretSlots,
                "effectiveLaunchers": effectiveLauncherSlots, "effectiveDroneBandwidth": effectiveDroneBandwidth,
                "resonance": resonance, "typeID": fit.shipID, "groupID": groupID, "shipSize": shipSize,
                "droneControlRange": fitModAttr["droneControlRange"], "mass": fitModAttr["mass"],
                "moduleNames": moduleNames, "projections": projections,
                "unpropedSpeed": propData["unpropedSpeed"], "unpropedSig": propData["unpropedSig"],
                "usingMWD": propData["usingMWD"], "mwdPropSpeed": mwdPropSpeed
            }
        except TypeError:
            pyfalog.error("Error parsing fit:" + str(fit))
            pyfalog.error(TypeError)
            dataDict = {"name": fitName + "Fit could not be correctly parsed"}
        export = json.dumps(dataDict, skipkeys=True)
        return export
