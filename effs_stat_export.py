import inspect
import os
import platform
import re
import sys
import traceback
from math import log

import eos.db

eos.db.saveddata_meta.create_all()

import json
from service.fit import Fit

def attrDirectMap(values, target, source):
    for val in values:
        target[val] = source.itemModifiedAttributes[val]

def getT2MwdSpeed(fit, fitL):
    fitID = fit.ID
    propID = None
    rigSize = fit.ship.itemModifiedAttributes['rigSize']
    if rigSize == 1 and fit.ship.itemModifiedAttributes['medSlots'] > 0:
        propID = 440
    elif rigSize == 2 and fit.ship.itemModifiedAttributes['medSlots'] > 0:
        propID = 12076
    elif rigSize == 3 and fit.ship.itemModifiedAttributes['medSlots'] > 0:
        propID = 12084
    elif rigSize == 4 and fit.ship.itemModifiedAttributes['medSlots'] > 0:
        if fit.ship.itemModifiedAttributes['powerOutput'] > 60000:
            propID = 41253
        else:
            propID = 12084
    elif rigSize == None and fit.ship.itemModifiedAttributes['medSlots'] > 0:
        propID = 440
    if propID:
        fitL.appendModule(fitID, propID)
        fitL.recalc(fit)
        fit = eos.db.getFit(fitID)
        mwdPropSpeed = fit.maxSpeed
        mwdPosition = list(filter(lambda mod: mod.item and mod.item.ID == propID, fit.modules))[0].position
        fitL.removeModule(fitID, mwdPosition)
        fitL.recalc(fit)
        fit = eos.db.getFit(fitID)
        return mwdPropSpeed

def getPropData(fit, fitL):
    fitID = fit.ID
    propMods = list(filter(lambda mod: mod.item and mod.item.groupID in [46], fit.modules))
    possibleMWD = list(filter(lambda mod: 'signatureRadiusBonus' in mod.item.attributes, propMods))
    if len(possibleMWD) > 0 and possibleMWD[0].state > 0:
        mwd = possibleMWD[0]
        oldMwdState = mwd.state
        mwd.state = 0
        fitL.recalc(fit)
        fit = eos.db.getFit(fitID)
        sp = fit.maxSpeed
        sig = fit.ship.itemModifiedAttributes['signatureRadius']
        mwd.state = oldMwdState
        fitL.recalc(fit)
        fit = eos.db.getFit(fitID)
        return {'usingMWD': True, 'unpropedSpeed': sp, 'unpropedSig': sig}
    return {'usingMWD': False, 'unpropedSpeed': fit.maxSpeed, 'unpropedSig': fit.ship.itemModifiedAttributes['signatureRadius']}

def getOutgoingProjectionData(fit):
    # This is a subset of module groups capable of projection and a superset of those currently used by efs
    projectedModGroupIds = [
        41, 52, 65, 67, 68, 71, 80, 201, 208, 291, 325, 379, 585,
        842, 899, 1150, 1154, 1189, 1306, 1672, 1697, 1698, 1815, 1894
    ]
    projectedMods = list(filter(lambda mod: mod.item and mod.item.groupID in projectedModGroupIds, fit.modules))
    projections = []
    for mod in projectedMods:
        stats = {}
        if mod.item.groupID == 65 or mod.item.groupID == 1672:
            stats['type'] = 'Stasis Web'
            stats['optimal'] = mod.itemModifiedAttributes['maxRange']
            attrDirectMap(['duration', 'speedFactor'], stats, mod)
        elif mod.item.groupID == 291:
            stats['type'] = 'Weapon Disruptor'
            stats['optimal'] = mod.itemModifiedAttributes['maxRange']
            stats['falloff'] = mod.itemModifiedAttributes['falloffEffectiveness']
            attrDirectMap([
                'trackingSpeedBonus', 'maxRangeBonus', 'falloffBonus', 'aoeCloudSizeBonus',\
                'aoeVelocityBonus', 'missileVelocityBonus', 'explosionDelayBonus'\
            ], stats, mod)
        elif mod.item.groupID == 68:
            stats['type'] = 'Energy Nosferatu'
            attrDirectMap(['powerTransferAmount', 'energyNeutralizerSignatureResolution'], stats, mod)
        elif mod.item.groupID == 71:
            stats['type'] = 'Energy Neutralizer'
            attrDirectMap([
                'energyNeutralizerSignatureResolution','entityCapacitorLevelModifierSmall',\
                'entityCapacitorLevelModifierMedium', 'entityCapacitorLevelModifierLarge',\
                'energyNeutralizerAmount'\
            ], stats, mod)
        elif mod.item.groupID == 41 or mod.item.groupID == 1697:
            stats['type'] = 'Remote Shield Booster'
            attrDirectMap(['shieldBonus'], stats, mod)
        elif mod.item.groupID == 325 or mod.item.groupID == 1698:
            stats['type'] = 'Remote Armor Repairer'
            attrDirectMap(['armorDamageAmount'], stats, mod)
        elif mod.item.groupID == 52:
            stats['type'] = 'Warp Scrambler'
            attrDirectMap(['activationBlockedStrenght', 'warpScrambleStrength'], stats, mod)
        elif mod.item.groupID == 379:
            stats['type'] = 'Target Painter'
            attrDirectMap(['signatureRadiusBonus'], stats, mod)
        elif mod.item.groupID == 208:
            stats['type'] = 'Sensor Dampener'
            attrDirectMap(['maxTargetRangeBonus', 'scanResolutionBonus'], stats, mod)
        elif mod.item.groupID == 201:
            stats['type'] = 'ECM'
            attrDirectMap([
                'scanGravimetricStrengthBonus', 'scanMagnetometricStrengthBonus',\
                'scanRadarStrengthBonus', 'scanLadarStrengthBonus',\
            ], stats, mod)
        elif mod.item.groupID == 80:
            stats['type'] = 'Burst Jammer'
            mod.itemModifiedAttributes['maxRange'] = mod.itemModifiedAttributes['ecmBurstRange']
            attrDirectMap([
                'scanGravimetricStrengthBonus', 'scanMagnetometricStrengthBonus',\
                'scanRadarStrengthBonus', 'scanLadarStrengthBonus',\
            ], stats, mod)
        elif mod.item.groupID == 1189:
            stats['type'] = 'Micro Jump Drive'
            mod.itemModifiedAttributes['maxRange'] = 0
            attrDirectMap(['moduleReactivationDelay'], stats, mod)
        if mod.itemModifiedAttributes['maxRange'] == None:
            print(mod.item.name)
            print(mod.itemModifiedAttributes.items())
            raise ValueError('Projected module lacks a maxRange')
        stats['optimal'] = mod.itemModifiedAttributes['maxRange']
        stats['falloff'] = mod.itemModifiedAttributes['falloffEffectiveness'] or 0
        attrDirectMap(['duration', 'capacitorNeed'], stats, mod)
        projections.append(stats)
    return projections

def getModuleNames(fit):
    moduleNames = []
    highSlotNames = []
    midSlotNames = []
    lowSlotNames = []
    rigSlotNames = []
    miscSlotNames = [] #subsystems ect
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
            if mod.item != None:
                if mod.charge != None:
                    modSlotNames.append(mod.item.name + ':  ' + mod.charge.name)
                else:
                    modSlotNames.append(mod.item.name)
            else:
                modSlotNames.append('Empty Slot')
        except:
            print(vars(mod))
            print('could not find name for module')
            print(fit.modules)
    for modInfo in [['High Slots:'], highSlotNames, ['', 'Med Slots:'], midSlotNames, ['', 'Low Slots:'], lowSlotNames, ['', 'Rig Slots:'], rigSlotNames]:
        moduleNames.extend(modInfo)
    if len(miscSlotNames) > 0:
        moduleNames.append('')
        moduleNames.append('Subsystems:')
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
        moduleNames.append('')
        moduleNames.append('Drones:')
        moduleNames.extend(droneNames)
    if len(fighterNames) > 0:
        moduleNames.append('')
        moduleNames.append('Fighters:')
        moduleNames.extend(fighterNames)
    if len(fit.implants) > 0:
        moduleNames.append('')
        moduleNames.append('Implants:')
        for implant in fit.implants:
            moduleNames.append(implant.item.name)
    if len(fit.commandFits) > 0:
        moduleNames.append('')
        moduleNames.append('Command Fits:')
        for commandFit in fit.commandFits:
            moduleNames.append(commandFit.name)
    return moduleNames

def getWeaponSystemData(fit):
    weaponSystems = []
    groups = {}
    for mod in fit.modules:
        if mod.dps > 0:
            keystr = str(mod.itemID) + '-' + str(mod.chargeID)
            if keystr in groups:
                groups[keystr][1] += 1
            else:
                groups[keystr] = [mod, 1]
    for wepGroup in groups:
        stats = groups[wepGroup][0]
        c = groups[wepGroup][1]
        tracking = 0
        maxVelocity = 0
        explosionDelay = 0
        damageReductionFactor = 0
        explosionRadius = 0
        explosionVelocity = 0
        aoeFieldRange = 0
        if stats.hardpoint == 2:
            tracking = stats.itemModifiedAttributes['trackingSpeed']
            typeing = 'Turret'
            name = stats.item.name + ', ' + stats.charge.name
        elif stats.hardpoint == 1 or 'Bomb Launcher' in stats.item.name:
            maxVelocity = stats.chargeModifiedAttributes['maxVelocity']
            explosionDelay = stats.chargeModifiedAttributes['explosionDelay']
            damageReductionFactor = stats.chargeModifiedAttributes['aoeDamageReductionFactor']
            explosionRadius = stats.chargeModifiedAttributes['aoeCloudSize']
            explosionVelocity = stats.chargeModifiedAttributes['aoeVelocity']
            typeing = 'Missile'
            name = stats.item.name + ', ' + stats.charge.name
        elif stats.hardpoint == 0:
            aoeFieldRange = stats.itemModifiedAttributes['empFieldRange']
            typeing = 'SmartBomb'
            name = stats.item.name
        statDict = {'dps': stats.dps * c, 'capUse': stats.capUse * c, 'falloff': stats.falloff,\
                    'type': typeing, 'name': name, 'optimal': stats.maxRange,\
                    'numCharges': stats.numCharges, 'numShots': stats.numShots, 'reloadTime': stats.reloadTime,\
                    'cycleTime': stats.cycleTime, 'volley': stats.volley * c, 'tracking': tracking,\
                    'maxVelocity': maxVelocity, 'explosionDelay': explosionDelay, 'damageReductionFactor': damageReductionFactor,\
                    'explosionRadius': explosionRadius, 'explosionVelocity': explosionVelocity, 'aoeFieldRange': aoeFieldRange\
        }
        weaponSystems.append(statDict)
        #if fit.droneDPS > 0:
    for drone in fit.drones:
        if drone.dps[0] > 0 and drone.amountActive > 0:
            newTracking =  drone.itemModifiedAttributes['trackingSpeed'] / (drone.itemModifiedAttributes['optimalSigRadius'] / 40000)
            statDict = {'dps': drone.dps[0], 'cycleTime': drone.cycleTime, 'type': 'Drone',\
                        'optimal': drone.maxRange, 'name': drone.item.name, 'falloff': drone.falloff,\
                        'maxSpeed': drone.itemModifiedAttributes['maxVelocity'], 'tracking': newTracking,\
                        'volley': drone.dps[1]\
            }
            weaponSystems.append(statDict)
    for fighter in fit.fighters:
        if fighter.dps[0] > 0 and fighter.amountActive > 0:
            abilities = []
            #for ability in fighter.abilities:
            if 'fighterAbilityAttackMissileDamageEM' in fighter.itemModifiedAttributes:
                baseRef = 'fighterAbilityAttackMissile'
                baseRefDam = baseRef + 'Damage'
                damageReductionFactor = log(fighter.itemModifiedAttributes[baseRef + 'ReductionFactor']) / log(fighter.itemModifiedAttributes[baseRef + 'ReductionSensitivity'])
                abBaseDamage = fighter.itemModifiedAttributes[baseRefDam + 'EM'] + fighter.itemModifiedAttributes[baseRefDam + 'Therm'] + fighter.itemModifiedAttributes[baseRefDam + 'Exp'] + fighter.itemModifiedAttributes[baseRefDam + 'Kin']
                abDamage = abBaseDamage * fighter.itemModifiedAttributes[baseRefDam + 'Multiplier']
                ability = {'name': 'RegularAttack', 'volley': abDamage * fighter.amountActive, 'explosionRadius': fighter.itemModifiedAttributes[baseRef + 'ExplosionRadius'],\
                           'explosionVelocity': fighter.itemModifiedAttributes[baseRef + 'ExplosionVelocity'], 'optimal': fighter.itemModifiedAttributes[baseRef + 'RangeOptimal'],\
                           'damageReductionFactor': damageReductionFactor, 'rof': fighter.itemModifiedAttributes[baseRef + 'Duration'],\
                }
                abilities.append(ability)
            if 'fighterAbilityMissilesDamageEM' in fighter.itemModifiedAttributes:
                baseRef = 'fighterAbilityMissiles'
                baseRefDam = baseRef + 'Damage'
                damageReductionFactor = log(fighter.itemModifiedAttributes[baseRefDam + 'ReductionFactor']) / log(fighter.itemModifiedAttributes[baseRefDam + 'ReductionSensitivity'])
                abBaseDamage = fighter.itemModifiedAttributes[baseRefDam + 'EM'] + fighter.itemModifiedAttributes[baseRefDam + 'Therm'] + fighter.itemModifiedAttributes[baseRefDam + 'Exp'] + fighter.itemModifiedAttributes[baseRefDam + 'Kin']
                abDamage = abBaseDamage * fighter.itemModifiedAttributes[baseRefDam + 'Multiplier']
                ability = {'name': 'MissileAttack', 'volley': abDamage * fighter.amountActive, 'explosionRadius': fighter.itemModifiedAttributes[baseRef + 'ExplosionRadius'],\
                           'explosionVelocity': fighter.itemModifiedAttributes[baseRef + 'ExplosionVelocity'], 'optimal': fighter.itemModifiedAttributes[baseRef + 'Range'],\
                           'damageReductionFactor': damageReductionFactor, 'rof': fighter.itemModifiedAttributes[baseRef + 'Duration'],\
                }
                abilities.append(ability)
            statDict = {'dps': fighter.dps[0], 'type': 'Fighter', 'name': fighter.item.name,\
                        'maxSpeed': fighter.itemModifiedAttributes['maxVelocity'], 'abilities': abilities, 'ehp': fighter.itemModifiedAttributes['shieldCapacity'] / 0.8875 * fighter.amountActive,\
                        'volley': fighter.dps[1], 'signatureRadius': fighter.itemModifiedAttributes['signatureRadius']\
            }
            weaponSystems.append(statDict)
    return weaponSystems

def getWeaponBonusMultipliers(fit):
    multipliers = {'turret': 1, 'launcher': 1, 'droneBandwidth': 1}
    from eos.db import gamedata_session
    from eos.gamedata import Traits
    filterVal = Traits.typeID == fit.shipID
    data = gamedata_session.query(Traits).options().filter(filterVal).all()
    roleBonusMode = False
    if len(data) == 0:
        return multipliers
    previousTypedBonus = 0
    previousDroneTypeBonus = 0
    for bonusText in data[0].traitText.splitlines():
        bonusText = bonusText.lower()
        if 'per skill level' in bonusText:
            roleBonusMode = False
        if 'role bonus' in bonusText or 'misc bonus' in bonusText:
            roleBonusMode = True
        multi = 1
        if 'damage' in bonusText and not any(e in bonusText for e in ['control', 'heat']):
            splitText = bonusText.split('%')
            if (float(splitText[0]) > 0) == False:
                print('damage bonus split did not parse correctly!')
                print(float(splitText[0]))
            if roleBonusMode:
                addedMulti = float(splitText[0])
            else:
                addedMulti = float(splitText[0]) * 5
            if any(e in bonusText for e in [' em', 'thermal', 'kinetic', 'explosive']):
                if addedMulti > previousTypedBonus:
                    previousTypedBonus = addedMulti
                else:
                    addedMulti = 0
            if any(e in bonusText for e in ['heavy drone', 'medium drone', 'light drone', 'sentry drone']):
                if addedMulti > previousDroneTypeBonus:
                    previousDroneTypeBonus = addedMulti
                else:
                    addedMulti = 0
            multi = 1 + (addedMulti / 100)
        elif 'rate of fire' in bonusText:
            splitText = bonusText.split('%')
            if (float(splitText[0]) > 0) == False:
                print('rate of fire bonus split did not parse correctly!')
                print(float(splitText[0]))
            if roleBonusMode:
                rofMulti = float(splitText[0])
            else:
                rofMulti = float(splitText[0]) * 5
            multi = 1 / (1 - (rofMulti / 100))
        if multi > 1:
            if 'drone' in bonusText.lower():
                multipliers['droneBandwidth'] *= multi
            elif 'turret' in bonusText.lower():
                multipliers['turret'] *= multi
            elif any(e in bonusText for e in ['missile', 'torpedo']):
                multipliers['launcher'] *= multi
    return multipliers
def getShipSize(groupID):
    # Sizings are somewhat arbitrary but allow for a more managable number of top level groupings in a tree structure.
    shipSizes = ['Frigate', 'Destroyer', 'Cruiser', 'Battlecruiser', 'Battleship', 'Capital', 'Industrial', 'Misc']
    if groupID in [25, 31, 237, 324, 830, 831, 834, 893, 1283, 1527]:
        return shipSizes[0]
    elif groupID in [420, 541, 1305, 1534]:
        return shipSizes[1]
    elif groupID in [26, 358, 832, 833, 894, 906, 963]:
        return shipSizes[2]
    elif groupID in [419, 540, 1201]:
        return shipSizes[3]
    elif groupID in [27, 381, 898, 900]:
        return shipSizes[4]
    elif groupID in [30, 485, 513, 547, 659, 883, 902, 1538]:
        return shipSizes[5]
    elif groupID in [28, 380, 1202, 463, 543, 941]:
        return shipSizes[6]
    elif groupID in [29, 1022]:
        return shipSizes[7]
    else:
        sizeNotFoundMsg = 'ShipSize not found for groupID: ' + str(groupID)
        print(sizeNotFoundMsg)
        return sizeNotFoundMsg

def parseNeededFitDetails(fit, groupID):
    includeShipTypeData = groupID > 0
    fitID = fit.ID
    if len(fit.modules) > 0:
        fitName = fit.ship.name + ': ' + fit.name
    else:
        fitName = fit.name
    print('')
    print('name: ' + fit.name)
    fitL = Fit()
    fitL.recalc(fit)
    fit = eos.db.getFit(fitID)
    fitModAttr = fit.ship.itemModifiedAttributes
    propData = getPropData(fit, fitL)
    print(fitModAttr['rigSize'])
    print(propData)
    mwdPropSpeed = fit.maxSpeed
    if includeShipTypeData:
        mwdPropSpeed = getT2MwdSpeed(fit, fitL)
    projections = getOutgoingProjectionData(fit)
    moduleNames = getModuleNames(fit)
    weaponSystems = getWeaponSystemData(fit)

    turretSlots = fitModAttr['turretSlotsLeft'] if fitModAttr['turretSlotsLeft'] is not None else 0
    launcherSlots = fitModAttr['launcherSlotsLeft'] if fitModAttr['launcherSlotsLeft'] is not None else 0
    droneBandwidth = fitModAttr['droneBandwidth'] if fitModAttr['droneBandwidth'] is not None else 0
    weaponBonusMultipliers = getWeaponBonusMultipliers(fit)
    effectiveTurretSlots = round(turretSlots * weaponBonusMultipliers['turret'], 2);
    effectiveLauncherSlots = round(launcherSlots * weaponBonusMultipliers['launcher'], 2);
    effectiveDroneBandwidth = round(droneBandwidth * weaponBonusMultipliers['droneBandwidth'], 2);
    # Assume a T2 siege module for dreads
    if groupID == 485:
        effectiveTurretSlots *= 9.4
        effectiveLauncherSlots *= 15
    hullResonance = {
        'exp': fitModAttr['explosiveDamageResonance'], 'kin': fitModAttr['kineticDamageResonance'], \
        'therm': fitModAttr['thermalDamageResonance'], 'em': fitModAttr['emDamageResonance']
    }
    armorResonance = {
        'exp': fitModAttr['armorExplosiveDamageResonance'], 'kin': fitModAttr['armorKineticDamageResonance'], \
        'therm': fitModAttr['armorThermalDamageResonance'], 'em': fitModAttr['armorEmDamageResonance']
    }
    shieldResonance = {
        'exp': fitModAttr['shieldExplosiveDamageResonance'], 'kin': fitModAttr['shieldKineticDamageResonance'], \
        'therm': fitModAttr['shieldThermalDamageResonance'], 'em': fitModAttr['shieldEmDamageResonance']
    }
    resonance = {'hull': hullResonance, 'armor': armorResonance, 'shield': shieldResonance}
    shipSize = getShipSize(groupID)

    try:
        parsable =  {
            'name': fitName, 'ehp': fit.ehp, 'droneDPS': fit.droneDPS, \
            'droneVolley': fit.droneVolley, 'hp': fit.hp, 'maxTargets': fit.maxTargets, \
            'maxSpeed': fit.maxSpeed, 'weaponVolley': fit.weaponVolley, 'totalVolley': fit.totalVolley,\
            'maxTargetRange': fit.maxTargetRange, 'scanStrength': fit.scanStrength,\
            'weaponDPS': fit.weaponDPS, 'alignTime': fit.alignTime, 'signatureRadius': fitModAttr['signatureRadius'],\
            'weapons': weaponSystems, 'scanRes': fitModAttr['scanResolution'],\
            'projectedModules': fit.projectedModules, 'capUsed': fit.capUsed, 'capRecharge': fit.capRecharge,\
            'rigSlots': fitModAttr['rigSlots'], 'lowSlots': fitModAttr['lowSlots'],\
            'midSlots': fitModAttr['medSlots'], 'highSlots': fitModAttr['hiSlots'],\
            'turretSlots': fitModAttr['turretSlotsLeft'], 'launcherSlots': fitModAttr['launcherSlotsLeft'],\
            'powerOutput': fitModAttr['powerOutput'], 'rigSize': fitModAttr['rigSize'],\
            'effectiveTurrets': effectiveTurretSlots, 'effectiveLaunchers': effectiveLauncherSlots,\
            'effectiveDroneBandwidth': effectiveDroneBandwidth,\
            'resonance': resonance, 'typeID': fit.shipID, 'groupID': groupID, 'shipSize': shipSize,\
            'droneControlRange': fitModAttr['droneControlRange'], 'mass': fitModAttr['mass'],\
            'moduleNames': moduleNames, 'projections': projections,\
            'unpropedSpeed': propData['unpropedSpeed'], 'unpropedSig': propData['unpropedSig'],\
            'usingMWD': propData['usingMWD'], 'mwdPropSpeed': mwdPropSpeed
        }
    except TypeError:
        print('Error parsing fit:' + str(fit))
        print(TypeError)
        parsable = {'name': fitName + 'Fit could not be correctly parsed'}
    stringified = json.dumps(parsable, skipkeys=True)
    return stringified
