# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================


import eos.config
from eos.const import FittingModuleState
from eos.utils.spoolSupport import SpoolType, SpoolOptions, calculateSpoolup, resolveSpoolOptions


class EffectDef:

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        pass


class Effect4(EffectDef):

    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr('shieldBonus')
        speed = module.getModifiedItemAttr('duration') / 1000.0
        fit.extraAttributes.increase('shieldRepair', amount / speed)


class Effect10(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        # Set reload time to 1 second
        module.reloadTime = 1000


class Effect17(EffectDef):

    grouped = True
    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        miningDroneAmountPercent = container.getModifiedItemAttr('miningDroneAmountPercent')
        if (miningDroneAmountPercent is None) or (miningDroneAmountPercent == 0):
            pass
        else:
            container.multiplyItemAttr('miningAmount', miningDroneAmountPercent / 100)


class Effect21(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('shieldCapacity', module.getModifiedItemAttr('capacityBonus'))


class Effect25(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.increaseItemAttr('capacitorCapacity', ship.getModifiedItemAttr('capacitorBonus'))


class Effect26(EffectDef):

    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr('structureDamageAmount')
        speed = module.getModifiedItemAttr('duration') / 1000.0
        fit.extraAttributes.increase('hullRepair', amount / speed)


class Effect27(EffectDef):

    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr('armorDamageAmount')
        speed = module.getModifiedItemAttr('duration') / 1000.0
        rps = amount / speed
        fit.extraAttributes.increase('armorRepair', rps)
        fit.extraAttributes.increase('armorRepairPreSpool', rps)
        fit.extraAttributes.increase('armorRepairFullSpool', rps)


class Effect34(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        rt = module.getModifiedItemAttr('reloadTime')
        if not rt:
            # Set reload time to 10 seconds
            module.reloadTime = 10000
        else:
            module.reloadTime = rt


class Effect38(EffectDef):

    type = 'active'


class Effect39(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context):
        if 'projected' in context:
            fit.ship.increaseItemAttr('warpScrambleStatus', module.getModifiedItemAttr('warpScrambleStrength'))


class Effect48(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        # Set reload time to 10 seconds
        module.reloadTime = 10000
        # Make so that reloads are always taken into account during clculations
        module.forceReload = True

        if module.charge is None:
            return
        capAmount = module.getModifiedChargeAttr('capacitorBonus') or 0
        module.itemModifiedAttributes['capacitorNeed'] = -capAmount


class Effect50(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('shieldRechargeRate', module.getModifiedItemAttr('shieldRechargeRateMultiplier') or 1)


class Effect51(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('rechargeRate', module.getModifiedItemAttr('capacitorRechargeRateMultiplier'))


class Effect55(EffectDef):

    type = 'active'


class Effect56(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        # We default this to None as there are times when the source attribute doesn't exist (for example, Cap Power Relay).
        # It will return 0 as it doesn't exist, which would nullify whatever the target attribute is
        fit.ship.multiplyItemAttr('powerOutput', module.getModifiedItemAttr('powerOutputMultiplier', None))


class Effect57(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        # We default this to None as there are times when the source attribute doesn't exist (for example, Cap Power Relay).
        # It will return 0 as it doesn't exist, which would nullify whatever the target attribute is
        fit.ship.multiplyItemAttr('shieldCapacity', module.getModifiedItemAttr('shieldCapacityMultiplier', None))


class Effect58(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        # We default this to None as there are times when the source attribute doesn't exist (for example, Cap Power Relay).
        # It will return 0 as it doesn't exist, which would nullify whatever the target attribute is
        fit.ship.multiplyItemAttr('capacitorCapacity', module.getModifiedItemAttr('capacitorCapacityMultiplier', None))


class Effect59(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('capacity', module.getModifiedItemAttr('cargoCapacityMultiplier'))


class Effect60(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('hp', module.getModifiedItemAttr('structureHPMultiplier'))


class Effect61(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('agility', src.getModifiedItemAttr('agilityBonusAdd'))


class Effect63(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('armorHP', module.getModifiedItemAttr('armorHPMultiplier'))


class Effect67(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        # Set reload time to 1 second
        module.reloadTime = 1000


class Effect89(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Projectile Weapon',
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect91(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Energy Weapon',
                                         'damageMultiplier', module.getModifiedItemAttr('damageMultiplier'),
                                         stackingPenalties=True)


class Effect92(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Projectile Weapon',
                                         'damageMultiplier', module.getModifiedItemAttr('damageMultiplier'),
                                         stackingPenalties=True)


class Effect93(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                         'damageMultiplier', module.getModifiedItemAttr('damageMultiplier'),
                                         stackingPenalties=True)


class Effect95(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Energy Weapon',
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect96(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect101(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, src, context):
        # Set reload time to 10 seconds
        src.reloadTime = 10000

        if 'projected' in context:
            if src.item.group.name == 'Missile Launcher Bomb':
                # Bomb Launcher Cooldown Timer
                moduleReactivationDelay = src.getModifiedItemAttr('moduleReactivationDelay')
                speed = src.getModifiedItemAttr('speed')

                # Void and Focused Void Bombs
                neutAmount = src.getModifiedChargeAttr('energyNeutralizerAmount')

                if moduleReactivationDelay and neutAmount and speed:
                    fit.addDrain(src, speed + moduleReactivationDelay, neutAmount, 0)

                # Lockbreaker Bombs
                ecmStrengthBonus = src.getModifiedChargeAttr('scan{0}StrengthBonus'.format(fit.scanType))

                if ecmStrengthBonus:
                    strModifier = 1 - ecmStrengthBonus / fit.scanStrength
                    fit.ecmProjectedStr *= strModifier


class Effect118(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('maxLockedTargets', module.getModifiedItemAttr('maxLockedTargetsBonus'))


class Effect157(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect159(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect160(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect161(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect162(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect172(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect173(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect174(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect212(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Electronics Upgrades'),
                                      'cpu', container.getModifiedItemAttr('cpuNeedBonus') * level)


class Effect214(EffectDef):

    type = 'passive', 'structure'

    @staticmethod
    def handler(fit, skill, context):
        amount = skill.getModifiedItemAttr('maxTargetBonus') * skill.level
        fit.extraAttributes.increase('maxTargetsLockedFromSkills', amount)


class Effect223(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.boostItemAttr('maxVelocity', implant.getModifiedItemAttr('velocityBonus'))


class Effect227(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Propulsion Module',
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus'))


class Effect230(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'duration', container.getModifiedItemAttr('durationBonus') * level)


class Effect235(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.boostItemAttr('warpCapacitorNeed', implant.getModifiedItemAttr('warpCapacitorNeedBonus'))


class Effect242(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Propulsion Module',
                                      'speedFactor', implant.getModifiedItemAttr('speedFBonus'))


class Effect244(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect271(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('armorHP', (container.getModifiedItemAttr('armorHpBonus') or 0) * level)


class Effect272(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'duration', container.getModifiedItemAttr('durationSkillBonus') * level)


class Effect273(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Upgrades'),
                                      'power', container.getModifiedItemAttr('powerNeedBonus') * level)


class Effect277(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.ship.increaseItemAttr('shieldUniformity', skill.getModifiedItemAttr('uniformityBonus') * skill.level)


class Effect279(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect287(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect290(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'maxRange', container.getModifiedItemAttr('rangeSkillBonus') * level)


class Effect298(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'falloff', container.getModifiedItemAttr('falloffBonus') * level)


class Effect315(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        amount = skill.getModifiedItemAttr('maxActiveDroneBonus') * skill.level
        fit.extraAttributes.increase('maxActiveDrones', amount)


class Effect391(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining'),
                                      'miningAmount', container.getModifiedItemAttr('miningAmountBonus') * level)


class Effect392(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('hp', container.getModifiedItemAttr('hullHpBonus') * level)


class Effect394(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        amount = container.getModifiedItemAttr('velocityBonus') or 0
        fit.ship.boostItemAttr('maxVelocity', amount * level,
                               stackingPenalties='skill' not in context and 'implant' not in context and 'booster' not in context)


class Effect395(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('agility', container.getModifiedItemAttr('agilityBonus') * level,
                               stackingPenalties='skill' not in context and 'implant' not in context)


class Effect396(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Energy Grid Upgrades'),
                                      'cpu', container.getModifiedItemAttr('cpuNeedBonus') * level)


class Effect397(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('cpuOutput', container.getModifiedItemAttr('cpuOutputBonus2') * level)


class Effect408(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect414(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'speed', container.getModifiedItemAttr('turretSpeeBonus') * level)


class Effect446(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('shieldCapacity', container.getModifiedItemAttr('shieldCapacityBonus') * level)


class Effect485(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('rechargeRate', container.getModifiedItemAttr('capRechargeBonus') * level)


class Effect486(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('shieldRechargeRate', container.getModifiedItemAttr('rechargeratebonus') * level)


class Effect490(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('powerOutput', container.getModifiedItemAttr('powerEngineeringOutputBonus') * level)


class Effect494(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('warpCapacitorNeed', container.getModifiedItemAttr('warpCapacitorNeedBonus') * level,
                               stackingPenalties='skill' not in context)


class Effect504(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        amount = container.getModifiedItemAttr('droneRangeBonus') * level
        fit.extraAttributes.increase('droneControlRange', amount)


class Effect506(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'capacitorNeed', skill.getModifiedItemAttr('capNeedBonus') * skill.level)


class Effect507(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('maxTargetRange', container.getModifiedItemAttr('maxTargetRangeBonus') * level)


class Effect508(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect511(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect512(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect514(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect516(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect521(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect527(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('shipBonusMI'), skill='Minmatar Industrial')


class Effect529(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('capacity', ship.getModifiedItemAttr('shipBonusAI'), skill='Amarr Industrial')


class Effect536(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('cpuOutput', module.getModifiedItemAttr('cpuMultiplier'))


class Effect542(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusAB'), skill='Amarr Battleship')


class Effect549(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusMB'),
                                      skill='Minmatar Battleship')


class Effect550(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusGB'),
                                      skill='Gallente Battleship')


class Effect553(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusGB'), skill='Gallente Battleship')


class Effect562(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect581(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'cpu', container.getModifiedItemAttr('cpuNeedBonus') * level)


class Effect582(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'speed', skill.getModifiedItemAttr('rofBonus') * skill.level)


class Effect584(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'damageMultiplier', implant.getModifiedItemAttr('damageMultiplierBonus'))


class Effect587(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Weapon',
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect588(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Projectile Weapon',
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect589(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect590(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Energy Pulse Weapons'),
                                      'duration', container.getModifiedItemAttr('durationBonus') * level)


class Effect596(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.multiplyItemAttr('maxRange', module.getModifiedChargeAttr('weaponRangeMultiplier'))


class Effect598(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.multiplyItemAttr('speed', module.getModifiedChargeAttr('speedMultiplier') or 1)


class Effect599(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.multiplyItemAttr('falloff', module.getModifiedChargeAttr('fallofMultiplier') or 1)


class Effect600(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.multiplyItemAttr('trackingSpeed', module.getModifiedChargeAttr('trackingSpeedMultiplier'))


class Effect602(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusMC'), skill='Minmatar Cruiser')


class Effect604(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusMB2'), skill='Minmatar Battleship')


class Effect607(EffectDef):

    runTime = 'early'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        # Set flag which is used to determine if ship is cloaked or not
        # This is used to apply cloak-only bonuses, like Black Ops' speed bonus
        # Doesn't apply to covops cloaks
        fit.extraAttributes['cloaked'] = True
        # Apply speed penalty
        fit.ship.multiplyItemAttr('maxVelocity', module.getModifiedItemAttr('maxVelocityModifier'))


class Effect623(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Mining Drone Operation'),
                                     'miningAmount',
                                     container.getModifiedItemAttr('miningAmountBonus') * level)


class Effect627(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('powerOutput', module.getModifiedItemAttr('powerIncrease'))


class Effect657(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('agility',
                               module.getModifiedItemAttr('agilityMultiplier'),
                               stackingPenalties=True)


class Effect660(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                        'emDamage', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect661(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                        'explosiveDamage', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect662(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                        'thermalDamage', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect668(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                        'kineticDamage', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect670(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', module.getModifiedItemAttr('warpScrambleStrength'))


class Effect675(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Energy Pulse Weapons'),
                                      'cpu', skill.getModifiedItemAttr('cpuNeedBonus') * skill.level)


class Effect677(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'cpu', container.getModifiedItemAttr('cpuNeedBonus') * level)


class Effect699(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        penalized = False if 'skill' in context or 'implant' in context or 'booster' in context else True
        fit.ship.boostItemAttr('scanResolution', container.getModifiedItemAttr('scanResolutionBonus') * level,
                               stackingPenalties=penalized)


class Effect706(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpFactor', src.getModifiedItemAttr('eliteBonusCovertOps1'), skill='Covert Ops')


class Effect726(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        # TODO: investigate if we can live without such ifs or hardcoding
        # Viator doesn't have GI bonus
        if 'shipBonusGI' in fit.ship.item.attributes:
            bonusAttr = 'shipBonusGI'
        else:
            bonusAttr = 'shipBonusGI2'
        fit.ship.boostItemAttr('capacity', ship.getModifiedItemAttr(bonusAttr), skill='Gallente Industrial')


class Effect727(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('capacity', ship.getModifiedItemAttr('shipBonusCI'), skill='Caldari Industrial')


class Effect728(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('capacity', ship.getModifiedItemAttr('shipBonusMI'), skill='Minmatar Industrial')


class Effect729(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        # TODO: investigate if we can live without such ifs or hardcoding
        # Viator doesn't have GI bonus
        if 'shipBonusGI' in fit.ship.item.attributes:
            bonusAttr = 'shipBonusGI'
        else:
            bonusAttr = 'shipBonusGI2'
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr(bonusAttr), skill='Gallente Industrial')


class Effect730(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('shipBonusCI'), skill='Caldari Industrial')


class Effect732(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('shipBonusAI'), skill='Amarr Industrial')


class Effect736(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('capacitorCapacity', ship.getModifiedItemAttr('shipBonusAB2'), skill='Amarr Battleship')


class Effect744(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('CPU Management'),
                                      'duration', container.getModifiedItemAttr('scanspeedBonus') * level)


class Effect754(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect757(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect760(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'speed', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect763(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        for dmgType in ('em', 'kinetic', 'explosive', 'thermal'):
            fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                               '%sDamage' % dmgType,
                                               container.getModifiedItemAttr('missileDamageMultiplierBonus'),
                                               stackingPenalties=True)


class Effect784(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        penalized = False if 'skill' in context or 'implant' in context or 'booster' in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'explosionDelay', container.getModifiedItemAttr('maxFlightTimeBonus') * level,
                                        stackingPenalties=penalized)


class Effect804(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        # Dirty hack to work around cap charges setting cap booster
        # injection amount to zero
        rawAttr = module.item.getAttribute('capacitorNeed')
        if rawAttr is not None and rawAttr >= 0:
            module.boostItemAttr('capacitorNeed', module.getModifiedChargeAttr('capNeedBonus') or 0)


class Effect836(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('capacity', module.getModifiedItemAttr('cargoCapacityBonus'))


class Effect848(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Cloaking'),
                                      'cloakingTargetingDelay',
                                      skill.getModifiedItemAttr('cloakingTargetingDelayBonus') * skill.level)


class Effect854(EffectDef):

    type = 'offline'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('scanResolution',
                                  module.getModifiedItemAttr('scanResolutionMultiplier'),
                                  stackingPenalties=True, penaltyGroup='cloakingScanResolutionMultiplier')


class Effect856(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        penalized = False if 'skill' in context or 'implant' in context else True
        fit.ship.boostItemAttr('baseWarpSpeed', container.getModifiedItemAttr('WarpSBonus'),
                               stackingPenalties=penalized)


class Effect874(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')


class Effect882(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect887(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusAB2'), skill='Amarr Battleship')


class Effect889(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect891(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusCB3'), skill='Caldari Battleship')


class Effect892(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusCB3'), skill='Caldari Battleship')


class Effect896(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cloaking Device',
                                         'cpu', container.getModifiedItemAttr('cloakingCpuNeedBonus'))


class Effect898(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect899(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect900(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Light Drone Operation'),
                                     'thermalDamage', ship.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect907(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect909(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorHP', ship.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect912(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'speed', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect918(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.extraAttributes.increase('maxActiveDrones', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect919(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect958(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', ship.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect959(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', ship.getModifiedItemAttr('shipBonusAC2'),
                               skill='Amarr Cruiser')


class Effect960(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', ship.getModifiedItemAttr('shipBonusAC2'),
                               skill='Amarr Cruiser')


class Effect961(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance', ship.getModifiedItemAttr('shipBonusAC2'),
                               skill='Amarr Cruiser')


class Effect968(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusMC2'),
                                      skill='Minmatar Cruiser')


class Effect980(EffectDef):

    runTime = 'early'
    type = 'active'

    @staticmethod
    def handler(fit, ship, context):
        fit.extraAttributes['cloaked'] = True
        # TODO: Implement


class Effect989(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusGunship1'), skill='Assault Frigates')


class Effect991(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusGunship1'), skill='Assault Frigates')


class Effect996(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('eliteBonusGunship2'),
                                      skill='Assault Frigates')


class Effect998(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('eliteBonusGunship2'), skill='Assault Frigates')


class Effect999(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', ship.getModifiedItemAttr('eliteBonusGunship2'),
                                      skill='Assault Frigates')


class Effect1001(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('rechargeRate', ship.getModifiedItemAttr('eliteBonusGunship2'), skill='Assault Frigates')


class Effect1003(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Pulse Laser Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1004(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Beam Laser Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1005(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Blaster Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1006(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Railgun Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1007(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Autocannon Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1008(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Artillery Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1009(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Pulse Laser Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1010(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Beam Laser Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1011(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Blaster Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1012(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Railgun Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1013(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Autocannon Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1014(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Artillery Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1015(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Pulse Laser Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1016(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Beam Laser Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1017(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Blaster Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1018(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Railgun Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1019(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Autocannon Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1020(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Artillery Specialization'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1021(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusGunship2'),
                                      skill='Assault Frigates')


class Effect1024(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect1025(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect1030(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect1033(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('eliteBonusLogistics1'), skill='Logistics Cruisers')


class Effect1034(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('eliteBonusLogistics2'), skill='Logistics Cruisers')


class Effect1035(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('eliteBonusLogistics2'), skill='Logistics Cruisers')


class Effect1036(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('eliteBonusLogistics1'), skill='Logistics Cruisers')


class Effect1046(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'maxRange',
                                      src.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect1047(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'maxRange',
                                      src.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect1048(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'maxRange',
                                      src.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect1049(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'maxRange',
                                      src.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect1056(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                      skill='Heavy Assault Cruisers')


class Effect1057(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                      skill='Heavy Assault Cruisers')


class Effect1058(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                      skill='Heavy Assault Cruisers')


class Effect1060(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                      skill='Heavy Assault Cruisers')


class Effect1061(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                      skill='Heavy Assault Cruisers')


class Effect1062(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                      skill='Heavy Assault Cruisers')


class Effect1063(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                      skill='Heavy Assault Cruisers')


class Effect1080(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'falloff', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                      skill='Heavy Assault Cruisers')


class Effect1081(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'explosionDelay', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                        skill='Heavy Assault Cruisers')


class Effect1082(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'explosionDelay', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                        skill='Heavy Assault Cruisers')


class Effect1084(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.extraAttributes.increase('droneControlRange', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                     skill='Heavy Assault Cruisers')


class Effect1087(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                      skill='Heavy Assault Cruisers')


class Effect1099(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')


class Effect1176(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Propulsion Module',
                                      'speedFactor', container.getModifiedItemAttr('speedFBonus') * level)


class Effect1179(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusGunship2'),
                                      skill='Assault Frigates')


class Effect1181(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Capacitor Transmitter',
                                      'capacitorNeed', ship.getModifiedItemAttr('eliteBonusLogistics1'),
                                      skill='Logistics Cruisers')


class Effect1182(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Capacitor Transmitter',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect1183(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Capacitor Transmitter',
                                      'capacitorNeed', ship.getModifiedItemAttr('eliteBonusLogistics2'),
                                      skill='Logistics Cruisers')


class Effect1184(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Capacitor Transmitter',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect1185(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.boostItemAttr('signatureRadius', implant.getModifiedItemAttr('signatureRadiusBonus'))


class Effect1190(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting'),
                                      'duration', container.getModifiedItemAttr('iceHarvestCycleBonus') * level)


class Effect1200(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.multiplyItemAttr('specialtyMiningAmount',
                                module.getModifiedChargeAttr('specialisationAsteroidYieldMultiplier'))
        # module.multiplyItemAttr('miningAmount', module.getModifiedChargeAttr('specialisationAsteroidYieldMultiplier'))


class Effect1212(EffectDef):

    runTime = 'late'
    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.preAssignItemAttr('specialtyMiningAmount', module.getModifiedItemAttr('miningAmount'))


class Effect1215(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'powerTransferAmount', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect1218(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect1219(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'powerTransferAmount', ship.getModifiedItemAttr('shipBonusAB'),
                                      skill='Amarr Battleship')


class Effect1220(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'powerTransferAmount', ship.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect1221(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect1222(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect1228(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect1230(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect1232(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect1233(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect1234(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect1239(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect1240(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect1255(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cyberimplant',
                                                 'durationBonus', implant.getModifiedItemAttr('implantSetBloodraider'))


class Effect1256(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capacitor Emission Systems'),
                                      'duration', implant.getModifiedItemAttr('durationBonus'))


class Effect1261(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cyberimplant',
                                                 'velocityBonus', implant.getModifiedItemAttr('implantSetSerpentis'))


class Effect1264(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('eliteBonusInterceptor2'),
                                      skill='Interceptors')


class Effect1268(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('eliteBonusInterceptor2'),
                                      skill='Interceptors')


class Effect1281(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        penalized = 'implant' not in context
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', container.getModifiedItemAttr('repairBonus'),
                                      stackingPenalties=penalized)


class Effect1318(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        groups = ('ECM', 'Burst Jammer')
        level = container.level if 'skill' in context else 1
        for scanType in ('Gravimetric', 'Ladar', 'Magnetometric', 'Radar'):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                          'scan{0}StrengthBonus'.format(scanType),
                                          container.getModifiedItemAttr('scanSkillEwStrengthBonus') * level,
                                          stackingPenalties=False if 'skill' in context else True)


class Effect1360(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Sensor Linking'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect1361(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect1370(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Target Painting'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect1372(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect1395(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', container.getModifiedItemAttr('shieldBoostMultiplier'))


class Effect1397(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cyberimplant',
                                                 'shieldBoostMultiplier', implant.getModifiedItemAttr('implantSetGuristas'))


class Effect1409(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Astrometrics'),
                                      'duration', container.getModifiedItemAttr('durationBonus') * level)


class Effect1410(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):

        level = container.level if 'skill' in context else 1

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Propulsion Jamming'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect1412(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusCB'), skill='Caldari Battleship')


class Effect1434(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for sensorType in ('Gravimetric', 'Ladar', 'Magnetometric', 'Radar'):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Electronic Warfare'),
                                          'scan{0}StrengthBonus'.format(sensorType),
                                          ship.getModifiedItemAttr('shipBonusCB'), stackingPenalties=True,
                                          skill='Caldari Battleship')


class Effect1441(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusCB3'), skill='Caldari Battleship')


class Effect1442(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect1443(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect1445(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Sensor Linking'),
                                      'maxRange', container.getModifiedItemAttr('rangeSkillBonus') * level,
                                      stackingPenalties='skill' not in context)


class Effect1446(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter',
                                      'maxRange', container.getModifiedItemAttr('rangeSkillBonus') * level,
                                      stackingPenalties='skill' not in context)


class Effect1448(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Weapon Disruptor',
                                      'maxRange', container.getModifiedItemAttr('rangeSkillBonus') * level,
                                      stackingPenalties='skill' not in context)


class Effect1449(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Sensor Linking'),
                                      'falloffEffectiveness', skill.getModifiedItemAttr('falloffBonus') * skill.level)


class Effect1450(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter',
                                      'falloffEffectiveness', skill.getModifiedItemAttr('falloffBonus') * skill.level)


class Effect1451(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Weapon Disruptor',
                                      'falloffEffectiveness', skill.getModifiedItemAttr('falloffBonus') * skill.level)


class Effect1452(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'maxRange', container.getModifiedItemAttr('rangeSkillBonus') * level,
                                      stackingPenalties='skill' not in context and 'implant' not in context)


class Effect1453(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'falloffEffectiveness', skill.getModifiedItemAttr('falloffBonus') * skill.level)


class Effect1472(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        penalize = False if 'skill' in context or 'implant' in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'aoeCloudSize', container.getModifiedItemAttr('aoeCloudSizeBonus') * level,
                                        stackingPenalties=penalize)


class Effect1500(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'capacitorNeed', container.getModifiedItemAttr('shieldBoostCapacitorBonus') * level)


class Effect1550(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter',
                                      'signatureRadiusBonus',
                                      skill.getModifiedItemAttr('scanSkillTargetPaintStrengthBonus') * skill.level)


class Effect1551(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter',
                                      'signatureRadiusBonus', ship.getModifiedItemAttr('shipBonusMF2'),
                                      skill='Minmatar Frigate')


class Effect1577(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(
            lambda implant: 'signatureRadiusBonus' in implant.itemModifiedAttributes and
                            'implantSetAngel' in implant.itemModifiedAttributes,
            'signatureRadiusBonus',
            implant.getModifiedItemAttr('implantSetAngel'))


class Effect1579(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill('Cybernetics'),
                                                 'armorHpBonus', implant.getModifiedItemAttr('implantSetSansha') or 1)


class Effect1581(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.ship.boostItemAttr('jumpDriveRange', skill.getModifiedItemAttr('jumpDriveRangeBonus') * skill.level)


class Effect1585(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Energy Turret'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1586(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Projectile Turret'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1587(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Hybrid Turret'),
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1588(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'),
                                        'kineticDamage', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect1590(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        penalize = False if 'skill' in context or 'implant' in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'aoeVelocity', container.getModifiedItemAttr('aoeVelocityBonus') * level,
                                        stackingPenalties=penalize)


class Effect1592(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'),
                                        'emDamage', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect1593(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'),
                                        'explosiveDamage', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect1594(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'),
                                        'thermalDamage', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect1595(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        mod = src.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'emDamage', src.getModifiedItemAttr('damageMultiplierBonus') * mod)


class Effect1596(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        mod = src.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'explosiveDamage', src.getModifiedItemAttr('damageMultiplierBonus') * mod)


class Effect1597(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        mod = src.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', src.getModifiedItemAttr('damageMultiplierBonus') * mod)


class Effect1615(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        skillName = 'Advanced Spaceship Command'
        skill = fit.character.getSkill(skillName)
        fit.ship.boostItemAttr('agility', skill.getModifiedItemAttr('agilityBonus'), skill=skillName)


class Effect1616(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        if fit.ship.item.requiresSkill('Capital Ships'):
            fit.ship.boostItemAttr('agility', skill.getModifiedItemAttr('agilityBonus') * skill.level)


class Effect1617(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.multiplyItemAttr('agility', src.getModifiedItemAttr('advancedCapitalAgility'), stackingPenalties=True)


class Effect1634(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Operation'),
                                      'capacitorNeed', container.getModifiedItemAttr('shieldBoostCapacitorBonus') * level)


class Effect1635(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Repair Systems'),
                                      'duration', container.getModifiedItemAttr('durationSkillBonus') * level,
                                      stackingPenalties='skill' not in context)


class Effect1638(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Gunnery') or mod.item.requiresSkill('Missile Launcher Operation'),
            'power', skill.getModifiedItemAttr('powerNeedBonus') * skill.level)


class Effect1643(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff2Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff1Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff4Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff3Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'buffDuration',
                                      src.getModifiedItemAttr('mindlinkBonus'))


class Effect1644(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff3Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff4Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff2Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff1Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'buffDuration',
                                      src.getModifiedItemAttr('mindlinkBonus'))


class Effect1645(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff4Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff3Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff2Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff1Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'buffDuration',
                                      src.getModifiedItemAttr('mindlinkBonus'))


class Effect1646(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff4Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff3Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff1Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff2Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'buffDuration',
                                      src.getModifiedItemAttr('mindlinkBonus'))


class Effect1650(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        amount = -skill.getModifiedItemAttr('consumptionQuantityBonus')
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill(skill),
                                         'consumptionQuantity', amount * skill.level)


class Effect1657(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        mod = src.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'thermalDamage', src.getModifiedItemAttr('damageMultiplierBonus') * mod)


class Effect1668(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('capacity', ship.getModifiedItemAttr('freighterBonusA2'), skill='Amarr Freighter')


class Effect1669(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('capacity', ship.getModifiedItemAttr('freighterBonusC2'), skill='Caldari Freighter')


class Effect1670(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('capacity', ship.getModifiedItemAttr('freighterBonusG2'), skill='Gallente Freighter')


class Effect1671(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('capacity', ship.getModifiedItemAttr('freighterBonusM2'), skill='Minmatar Freighter')


class Effect1672(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('freighterBonusA1'), skill='Amarr Freighter')


class Effect1673(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('freighterBonusC1'), skill='Caldari Freighter')


class Effect1674(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('freighterBonusG1'), skill='Gallente Freighter')


class Effect1675(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('freighterBonusM1'), skill='Minmatar Freighter')


class Effect1720(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Operation') or mod.item.requiresSkill('Capital Shield Operation'),
            'shieldBonus', module.getModifiedItemAttr('shieldBoostMultiplier'),
            stackingPenalties=True)


class Effect1722(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.ship.boostItemAttr('jumpDriveCapacitorNeed',
                               skill.getModifiedItemAttr('jumpDriveCapacitorNeedBonus') * skill.level)


class Effect1730(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill(skill),
                                     'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect1738(EffectDef):

    type = 'active'


class Effect1763(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'speed', container.getModifiedItemAttr('rofBonus') * level)


class Effect1764(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        penalized = False if 'skill' in context or 'implant' in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', container.getModifiedItemAttr('speedFactor') * level,
                                        stackingPenalties=penalized)


class Effect1773(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect1804(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect1805(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance', ship.getModifiedItemAttr('shipBonusAF'),
                               skill='Amarr Frigate')


class Effect1806(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', ship.getModifiedItemAttr('shipBonusAF'),
                               skill='Amarr Frigate')


class Effect1807(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', ship.getModifiedItemAttr('shipBonusAF'),
                               skill='Amarr Frigate')


class Effect1812(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldEmDamageResonance', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect1813(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', ship.getModifiedItemAttr('shipBonusCC2'),
                               skill='Caldari Cruiser')


class Effect1814(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldKineticDamageResonance', ship.getModifiedItemAttr('shipBonusCC2'),
                               skill='Caldari Cruiser')


class Effect1815(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', ship.getModifiedItemAttr('shipBonusCC2'),
                               skill='Caldari Cruiser')


class Effect1816(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldEmDamageResonance', ship.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect1817(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', ship.getModifiedItemAttr('shipBonusCF'),
                               skill='Caldari Frigate')


class Effect1819(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldKineticDamageResonance', ship.getModifiedItemAttr('shipBonusCF'),
                               skill='Caldari Frigate')


class Effect1820(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', ship.getModifiedItemAttr('shipBonusCF'),
                               skill='Caldari Frigate')


class Effect1848(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff4Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff2Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff1Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff3Multiplier',
                                        src.getModifiedItemAttr('mindlinkBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'buffDuration',
                                      src.getModifiedItemAttr('mindlinkBonus'))


class Effect1851(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill),
                                      'speed', skill.getModifiedItemAttr('rofBonus') * skill.level)


class Effect1862(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect1863(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect1864(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusCF2'),
                                        skill='Caldari Frigate')


class Effect1882(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining'),
                                      'miningAmount', module.getModifiedItemAttr('miningAmountBonus'))


class Effect1885(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Cruise',
                                      'speed', ship.getModifiedItemAttr('shipBonus2CB'), skill='Caldari Battleship')


class Effect1886(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Torpedo',
                                      'speed', ship.getModifiedItemAttr('shipBonus2CB'), skill='Caldari Battleship')


class Effect1896(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting'),
                                      'duration', ship.getModifiedItemAttr('eliteBonusBarge2'), skill='Exhumers')


class Effect1910(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'powerTransferAmount', ship.getModifiedItemAttr('eliteBonusReconShip2'),
                                      skill='Recon Ships')


class Effect1911(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'scanGravimetricStrengthBonus', ship.getModifiedItemAttr('eliteBonusReconShip2'),
                                      skill='Recon Ships')


class Effect1912(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'scanMagnetometricStrengthBonus', ship.getModifiedItemAttr('eliteBonusReconShip2'),
                                      skill='Recon Ships')


class Effect1913(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'scanRadarStrengthBonus', ship.getModifiedItemAttr('eliteBonusReconShip2'),
                                      skill='Recon Ships')


class Effect1914(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'scanLadarStrengthBonus', ship.getModifiedItemAttr('eliteBonusReconShip2'),
                                      skill='Recon Ships')


class Effect1921(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusReconShip2'), skill='Recon Ships')


class Effect1922(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler',
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusReconShip2'), skill='Recon Ships')


class Effect1959(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('mass', module.getModifiedItemAttr('massAddition'))


class Effect1964(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect1969(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect1996(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect2000(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr('droneRangeBonus')
        fit.extraAttributes.increase('droneControlRange', amount)


class Effect2008(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Cynosural Field Generator',
                                      'duration', ship.getModifiedItemAttr('durationBonus'))


class Effect2013(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'maxVelocity', container.getModifiedItemAttr('droneMaxVelocityBonus') * level, stackingPenalties=True)


class Effect2014(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        stacking = False if 'skill' in context else True
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'maxRange',
                                     container.getModifiedItemAttr('rangeSkillBonus') * level,
                                     stackingPenalties=stacking)


class Effect2015(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'shieldCapacity', module.getModifiedItemAttr('hullHpBonus'))


class Effect2016(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'armorHP', module.getModifiedItemAttr('hullHpBonus'))


class Effect2017(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'hp', container.getModifiedItemAttr('hullHpBonus') * level)


class Effect2019(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == 'Logistic Drone',
                                     'shieldBonus', container.getModifiedItemAttr('damageHP') * level)


class Effect2020(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == 'Logistic Drone',
                                     'armorDamageAmount', container.getModifiedItemAttr('damageHP') * level,
                                     stackingPenalties=True)


class Effect2029(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('signatureRadius', module.getModifiedItemAttr('signatureRadiusAdd'))


class Effect2041(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for type in ('kinetic', 'thermal', 'explosive', 'em'):
            fit.ship.boostItemAttr('armor%sDamageResonance' % type.capitalize(),
                                   module.getModifiedItemAttr('%sDamageResistanceBonus' % type),
                                   stackingPenalties=True)


class Effect2052(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for type in ('kinetic', 'thermal', 'explosive', 'em'):
            fit.ship.boostItemAttr('shield%sDamageResonance' % type.capitalize(),
                                   module.getModifiedItemAttr('%sDamageResistanceBonus' % type),
                                   stackingPenalties=True)


class Effect2053(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Shield Resistance Amplifier',
                                      'emDamageResistanceBonus', skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2054(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Shield Resistance Amplifier',
                                      'explosiveDamageResistanceBonus',
                                      skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2055(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Shield Resistance Amplifier',
                                      'kineticDamageResistanceBonus',
                                      skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2056(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Shield Resistance Amplifier',
                                      'thermalDamageResistanceBonus',
                                      skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2105(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Coating',
                                      'emDamageResistanceBonus', skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2106(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Coating',
                                      'explosiveDamageResistanceBonus',
                                      skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2107(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Coating',
                                      'kineticDamageResistanceBonus',
                                      skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2108(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Coating',
                                      'thermalDamageResistanceBonus',
                                      skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2109(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Plating Energized',
                                      'emDamageResistanceBonus', skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2110(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Plating Energized',
                                      'explosiveDamageResistanceBonus',
                                      skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2111(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Plating Energized',
                                      'kineticDamageResistanceBonus',
                                      skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2112(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Plating Energized',
                                      'thermalDamageResistanceBonus',
                                      skill.getModifiedItemAttr('hardeningBonus') * skill.level)


class Effect2130(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('maxRangeBonus'))


class Effect2131(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('maxRangeBonus'))


class Effect2132(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'maxRange', ship.getModifiedItemAttr('maxRangeBonus'))


class Effect2133(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Capacitor Transmitter',
                                      'maxRange', ship.getModifiedItemAttr('maxRangeBonus2'))


class Effect2134(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Shield Booster', 'maxRange',
                                      ship.getModifiedItemAttr('maxRangeBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Ancillary Remote Shield Booster', 'maxRange',
                                      ship.getModifiedItemAttr('maxRangeBonus'))


class Effect2135(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Armor Repairer', 'maxRange',
                                      src.getModifiedItemAttr('maxRangeBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Ancillary Remote Armor Repairer', 'maxRange',
                                      src.getModifiedItemAttr('maxRangeBonus'))


class Effect2143(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter',
                                      'signatureRadiusBonus', ship.getModifiedItemAttr('shipBonusMC2'),
                                      skill='Minmatar Cruiser')


class Effect2155(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusCommandShips1'),
                                      skill='Command Ships')


class Effect2156(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('eliteBonusCommandShips2'), skill='Command Ships')


class Effect2157(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusCommandShips1'),
                                      skill='Command Ships')


class Effect2158(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'speed', ship.getModifiedItemAttr('eliteBonusCommandShips2'), skill='Command Ships')


class Effect2160(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'falloff', ship.getModifiedItemAttr('eliteBonusCommandShips2'), skill='Command Ships')


class Effect2161(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusCommandShips1'),
                                      skill='Command Ships')


class Effect2179(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for type in ('shieldCapacity', 'armorHP', 'hp'):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                         type, ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect2181(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for type in ('shieldCapacity', 'armorHP', 'hp'):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                         type, ship.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect2186(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for type in ('shieldCapacity', 'armorHP', 'hp'):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                         type, ship.getModifiedItemAttr('shipBonusGB2'), skill='Gallente Battleship')


class Effect2187(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusGB2'),
                                     skill='Gallente Battleship')


class Effect2188(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect2189(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect2200(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Light Missiles') or mod.charge.requiresSkill('Rockets'),
            'kineticDamage', ship.getModifiedItemAttr('eliteBonusInterdictors1'), skill='Interdictors')


class Effect2201(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('eliteBonusInterdictors1'), skill='Interdictors')


class Effect2215(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect2232(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for type in ('Gravimetric', 'Magnetometric', 'Radar', 'Ladar'):
            fit.ship.boostItemAttr('scan%sStrength' % type,
                                   module.getModifiedItemAttr('scan%sStrengthPercent' % type),
                                   stackingPenalties=True)


class Effect2249(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'miningAmount', ship.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect2250(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Mining Drone Operation'),
                                     'miningAmount', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect2251(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Leadership'), 'maxGroupActive',
                                         src.getModifiedItemAttr('maxGangModules'))
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Leadership'), 'maxGroupOnline',
                                         src.getModifiedItemAttr('maxGangModules'))


class Effect2252(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredItemForce(lambda mod: mod.item.requiresSkill('Cloaking'),
                                      'moduleReactivationDelay',
                                      container.getModifiedItemAttr('covertOpsAndReconOpsCloakModuleDelay'))


class Effect2253(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemForce(lambda mod: mod.item.group.name == 'Cloaking Device',
                                      'cloakingTargetingDelay',
                                      ship.getModifiedItemAttr('covertOpsStealthBomberTargettingDelay'))


class Effect2255(EffectDef):

    type = 'active'


class Effect2298(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        for type in ('Gravimetric', 'Magnetometric', 'Radar', 'Ladar'):
            sensorType = 'scan{0}Strength'.format(type)
            sensorBoost = 'scan{0}StrengthPercent'.format(type)
            if sensorBoost in implant.item.attributes:
                fit.ship.boostItemAttr(sensorType, implant.getModifiedItemAttr(sensorBoost))


class Effect2302(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
            for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
                bonus = '%s%sDamageResonance' % (attrPrefix, damageType)
                bonus = '%s%s' % (bonus[0].lower(), bonus[1:])
                booster = '%s%sDamageResonance' % (layer, damageType)
                fit.ship.multiplyItemAttr(bonus, module.getModifiedItemAttr(booster),
                                          stackingPenalties=True, penaltyGroup='preMul')


class Effect2305(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer',
                                      'energyNeutralizerAmount', ship.getModifiedItemAttr('eliteBonusReconShip2'),
                                      skill='Recon Ships')


class Effect2354(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Remote Armor Repair Systems'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect2355(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Emission Systems'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect2356(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Capacitor Emission Systems'),
                                      'capacitorNeed', skill.getModifiedItemAttr('capNeedBonus') * skill.level)


class Effect2402(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        damageTypes = ('em', 'explosive', 'kinetic', 'thermal')
        for dmgType in damageTypes:
            dmgAttr = '{0}Damage'.format(dmgType)
            fit.modules.filteredItemBoost(
                lambda mod: mod.item.group.name == 'Super Weapon' and dmgAttr in mod.itemModifiedAttributes,
                dmgAttr, skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect2422(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.boostItemAttr('maxVelocity', implant.getModifiedItemAttr('implantBonusVelocity'))


class Effect2432(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.ship.boostItemAttr('capacitorCapacity', container.getModifiedItemAttr('capacitorCapacityBonus') * level)


class Effect2444(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining'),
                                      'cpu', module.getModifiedItemAttr('cpuPenaltyPercent'))


class Effect2445(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting'),
                                      'cpu', module.getModifiedItemAttr('cpuPenaltyPercent'))


class Effect2456(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Upgrades'),
                                      'cpuPenaltyPercent',
                                      container.getModifiedItemAttr('miningUpgradeCPUReductionBonus') * level)


class Effect2465(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for type in ('Em', 'Explosive', 'Kinetic', 'Thermal'):
            fit.ship.boostItemAttr('armor{0}DamageResonance'.format(type), ship.getModifiedItemAttr('shipBonusAB'),
                                   skill='Amarr Battleship')


class Effect2479(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting'),
                                      'duration', module.getModifiedItemAttr('iceHarvestCycleBonus'))


class Effect2485(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.boostItemAttr('armorHP', implant.getModifiedItemAttr('armorHpBonus2'))


class Effect2488(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.boostItemAttr('maxVelocity', implant.getModifiedItemAttr('velocityBonus2'))


class Effect2489(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Tracking Computer',
                                      'falloffEffectiveness', ship.getModifiedItemAttr('shipBonusMC'),
                                      skill='Minmatar Cruiser')


class Effect2490(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Tracking Computer',
                                      'falloffEffectiveness', ship.getModifiedItemAttr('shipBonusGC2'),
                                      skill='Gallente Cruiser')


class Effect2491(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Burst Jammer',
                                      'ecmBurstRange', container.getModifiedItemAttr('rangeSkillBonus') * level,
                                      stackingPenalties=False if 'skill' in context else True)


class Effect2492(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Burst Jammer',
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect2503(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusGB2'),
                                      skill='Gallente Battleship')


class Effect2504(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect2561(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', ship.getModifiedItemAttr('eliteBonusGunship1'),
                                        skill='Assault Frigates')


class Effect2589(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        for i in range(5):
            attr = 'boosterEffectChance{0}'.format(i + 1)
            fit.boosters.filteredItemBoost(lambda booster: attr in booster.itemModifiedAttributes,
                                           attr, container.getModifiedItemAttr('boosterChanceBonus') * level)


class Effect2602(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldEmDamageResonance', ship.getModifiedItemAttr('shipBonus2CB'),
                               skill='Caldari Battleship')


class Effect2603(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', ship.getModifiedItemAttr('shipBonus2CB'),
                               skill='Caldari Battleship')


class Effect2604(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldKineticDamageResonance', ship.getModifiedItemAttr('shipBonus2CB'),
                               skill='Caldari Battleship')


class Effect2605(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', ship.getModifiedItemAttr('shipBonus2CB'),
                               skill='Caldari Battleship')


class Effect2611(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusGunship1'),
                                      skill='Assault Frigates')


class Effect2644(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('signatureRadius', module.getModifiedItemAttr('signatureRadiusBonus'), stackingPenalties=True)


class Effect2645(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('scanResolution', module.getModifiedItemAttr('scanResolutionMultiplier'),
                                  stackingPenalties=True)


class Effect2646(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRangeBonus'),
                               stackingPenalties=True)


class Effect2647(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Heavy',
                                      'speed', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                      skill='Heavy Assault Cruisers')


class Effect2648(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Heavy Assault',
                                      'speed', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                      skill='Heavy Assault Cruisers')


class Effect2649(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Rapid Light',
                                      'speed', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                      skill='Heavy Assault Cruisers')


class Effect2670(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRangeBonus'),
                               stackingPenalties=True)
        fit.ship.boostItemAttr('scanResolution', module.getModifiedItemAttr('scanResolutionBonus'),
                               stackingPenalties=True)

        for scanType in ('Gravimetric', 'Magnetometric', 'Radar', 'Ladar'):
            fit.ship.boostItemAttr(
                'scan{}Strength'.format(scanType),
                module.getModifiedItemAttr('scan{}StrengthPercent'.format(scanType)),
                stackingPenalties=True
            )


class Effect2688(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Weapon',
                                      'capacitorNeed', module.getModifiedItemAttr('capNeedBonus'))


class Effect2689(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                      'capacitorNeed', module.getModifiedItemAttr('capNeedBonus'))


class Effect2690(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Weapon',
                                      'cpu', module.getModifiedItemAttr('cpuNeedBonus'))


class Effect2691(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                      'cpu', module.getModifiedItemAttr('cpuNeedBonus'))


class Effect2693(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Weapon',
                                      'falloff', module.getModifiedItemAttr('falloffBonus'),
                                      stackingPenalties=True)


class Effect2694(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                      'falloff', module.getModifiedItemAttr('falloffBonus'),
                                      stackingPenalties=True)


class Effect2695(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Projectile Weapon',
                                      'falloff', module.getModifiedItemAttr('falloffBonus'),
                                      stackingPenalties=True)


class Effect2696(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Weapon',
                                      'maxRange', module.getModifiedItemAttr('maxRangeBonus'),
                                      stackingPenalties=True)


class Effect2697(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                      'maxRange', module.getModifiedItemAttr('maxRangeBonus'),
                                      stackingPenalties=True)


class Effect2698(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Projectile Weapon',
                                      'maxRange', module.getModifiedItemAttr('maxRangeBonus'),
                                      stackingPenalties=True)


class Effect2706(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Weapon',
                                      'power', module.getModifiedItemAttr('drawback'))


class Effect2707(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                      'power', module.getModifiedItemAttr('drawback'))


class Effect2708(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Projectile Weapon',
                                      'power', module.getModifiedItemAttr('drawback'))


class Effect2712(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('armorHP', module.getModifiedItemAttr('drawback'))


class Effect2713(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('cpuOutput', module.getModifiedItemAttr('drawback'))


class Effect2714(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'cpu', module.getModifiedItemAttr('drawback'))


class Effect2716(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('signatureRadius', module.getModifiedItemAttr('drawback'), stackingPenalties=True)


class Effect2717(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('drawback'),
                               stackingPenalties=True)


class Effect2718(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('shieldCapacity', module.getModifiedItemAttr('drawback'))


class Effect2726(EffectDef):

    type = 'active'


class Effect2727(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == 'Gas Cloud Harvester',
                                         'maxGroupActive', skill.level)


class Effect2734(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for type in ('Gravimetric', 'Ladar', 'Radar', 'Magnetometric'):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                          'scan{0}StrengthBonus'.format(type),
                                          ship.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect2735(EffectDef):

    attr = 'boosterArmorHPPenalty'
    displayName = 'Armor Capacity'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.ship.boostItemAttr('armorHP', booster.getModifiedItemAttr(attr))


class Effect2736(EffectDef):

    attr = 'boosterArmorRepairAmountPenalty'
    displayName = 'Armor Repair Amount'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Repair Unit',
                                      'armorDamageAmount', booster.getModifiedItemAttr(attr))


class Effect2737(EffectDef):

    attr = 'boosterShieldCapacityPenalty'
    displayName = 'Shield Capacity'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.ship.boostItemAttr('shieldCapacity', booster.getModifiedItemAttr(attr))


class Effect2739(EffectDef):

    attr = 'boosterTurretOptimalRangePenalty'
    displayName = 'Turret Optimal Range'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'maxRange', booster.getModifiedItemAttr(attr))


class Effect2741(EffectDef):

    attr = 'boosterTurretFalloffPenalty'
    displayName = 'Turret Falloff'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'falloff', booster.getModifiedItemAttr(attr))


class Effect2745(EffectDef):

    attr = 'boosterCapacitorCapacityPenalty'
    displayName = 'Cap Capacity'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.ship.boostItemAttr('capacitorCapacity', booster.getModifiedItemAttr(attr))


class Effect2746(EffectDef):

    attr = 'boosterMaxVelocityPenalty'
    displayName = 'Velocity'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.ship.boostItemAttr('maxVelocity', booster.getModifiedItemAttr(attr))


class Effect2747(EffectDef):

    attr = 'boosterTurretTrackingPenalty'
    displayName = 'Turret Tracking'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'trackingSpeed', booster.getModifiedItemAttr(attr))


class Effect2748(EffectDef):

    attr = 'boosterMissileVelocityPenalty'
    displayName = 'Missile Velocity'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', booster.getModifiedItemAttr(attr))


class Effect2749(EffectDef):

    attr = 'boosterAOEVelocityPenalty'
    displayName = 'Missile Explosion Velocity'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'aoeVelocity', booster.getModifiedItemAttr(attr))


class Effect2756(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for type in ('Gravimetric', 'Magnetometric', 'Ladar', 'Radar'):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                          'scan{0}StrengthBonus'.format(type), ship.getModifiedItemAttr('shipBonusCC'),
                                          skill='Caldari Cruiser')


class Effect2757(EffectDef):

    type = 'active'


class Effect2760(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        attrs = ('boosterArmorHPPenalty', 'boosterArmorRepairAmountPenalty')
        for attr in attrs:
            fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                           container.getModifiedItemAttr('boosterAttributeModifier') * level)


class Effect2763(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        attrs = ('boosterShieldBoostAmountPenalty', 'boosterShieldCapacityPenalty', 'shieldBoostMultiplier')
        for attr in attrs:
            # shieldBoostMultiplier can be positive (Blue Pill) and negative value (other boosters)
            # We're interested in decreasing only side-effects
            fit.boosters.filteredItemBoost(lambda booster: booster.getModifiedItemAttr(attr) < 0,
                                           attr, container.getModifiedItemAttr('boosterAttributeModifier') * level)


class Effect2766(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        attrs = ('boosterCapacitorCapacityPenalty', 'boosterMaxVelocityPenalty')
        for attr in attrs:
            fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                           container.getModifiedItemAttr('boosterAttributeModifier') * level)


class Effect2776(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        attrs = ('boosterAOEVelocityPenalty', 'boosterMissileAOECloudPenalty', 'boosterMissileVelocityPenalty')
        for attr in attrs:
            fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                           container.getModifiedItemAttr('boosterAttributeModifier') * level)


class Effect2778(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        attrs = ('boosterTurretFalloffPenalty', 'boosterTurretOptimalRangePenalty', 'boosterTurretTrackingPenalty')
        for attr in attrs:
            fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                           container.getModifiedItemAttr('boosterAttributeModifier') * level)


class Effect2791(EffectDef):

    attr = 'boosterMissileAOECloudPenalty'
    displayName = 'Missile Explosion Radius'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, booster, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'aoeCloudSize', booster.getModifiedItemAttr(attr))


class Effect2792(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for type in ('kinetic', 'thermal', 'explosive', 'em'):
            fit.ship.boostItemAttr('armor' + type.capitalize() + 'DamageResonance',
                                   module.getModifiedItemAttr(type + 'DamageResistanceBonus') or 0,
                                   stackingPenalties=True)


class Effect2794(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Salvaging'),
                                         'accessDifficultyBonus', container.getModifiedItemAttr('accessDifficultyBonus'),
                                         position='post')


class Effect2795(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for type in ('kinetic', 'thermal', 'explosive', 'em'):
            fit.ship.boostItemAttr('shield' + type.capitalize() + 'DamageResonance',
                                   module.getModifiedItemAttr(type + 'DamageResistanceBonus') or 0,
                                   stackingPenalties=True)


class Effect2796(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('mass', module.getModifiedItemAttr('massBonusPercentage'), stackingPenalties=True)


class Effect2797(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Projectile Weapon',
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect2798(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Projectile Weapon',
                                         'damageMultiplier', module.getModifiedItemAttr('damageMultiplier'),
                                         stackingPenalties=True)


class Effect2799(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect2801(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Energy Weapon',
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect2802(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                         'damageMultiplier', module.getModifiedItemAttr('damageMultiplier'),
                                         stackingPenalties=True)


class Effect2803(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Energy Weapon',
                                         'damageMultiplier', module.getModifiedItemAttr('damageMultiplier'),
                                         stackingPenalties=True)


class Effect2804(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect2805(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusAB2'),
                                      skill='Amarr Battleship')


class Effect2809(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect2810(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'explosionDelay', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                        skill='Heavy Assault Cruisers')


class Effect2812(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Burst Jammer',
                                      'ecmBurstRange', ship.getModifiedItemAttr('shipBonusCB3'), skill='Caldari Battleship')


class Effect2837(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('armorHP', module.getModifiedItemAttr('armorHPBonusAdd'))


class Effect2847(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'trackingSpeed', container.getModifiedItemAttr('trackingSpeedBonus') * level)


class Effect2848(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredItemIncrease(lambda module: module.item.requiresSkill('Archaeology'),
                                         'accessDifficultyBonus',
                                         container.getModifiedItemAttr('accessDifficultyBonusModifier'), position='post')


class Effect2849(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredItemIncrease(lambda c: c.item.requiresSkill('Hacking'),
                                         'accessDifficultyBonus',
                                         container.getModifiedItemAttr('accessDifficultyBonusModifier'), position='post')


class Effect2850(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Propulsion Module',
                                      'duration', module.getModifiedItemAttr('durationBonus'))


class Effect2851(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        for dmgType in ('em', 'kinetic', 'explosive', 'thermal'):
            fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                               '%sDamage' % dmgType,
                                               container.getModifiedItemAttr('missileDamageMultiplierBonus'),
                                               stackingPenalties=True)


class Effect2853(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda module: module.item.requiresSkill('Cloaking'),
                                      'cloakingTargetingDelay', module.getModifiedItemAttr('cloakingTargetingDelayBonus'))


class Effect2857(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('speedFactor'))


class Effect2865(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('implantBonusVelocity'),
                               stackingPenalties=True)


class Effect2866(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.boosters.filteredItemBoost(lambda bst: True, 'boosterDuration',
                                       container.getModifiedItemAttr('durationBonus') * level)


class Effect2867(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'damageMultiplier', module.getModifiedItemAttr('damageMultiplierBonus'),
                                     stackingPenalties=True)


class Effect2868(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Repair Systems'),
                                      'armorDamageAmount', implant.getModifiedItemAttr('repairBonus'),
                                      stackingPenalties=True)


class Effect2872(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Defender Missiles'),
                                           'maxVelocity', container.getModifiedItemAttr('missileVelocityBonus'))


class Effect2881(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'emDamage', implant.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2882(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'explosiveDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2883(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'kineticDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2884(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'thermalDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2885(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gas Cloud Harvesting'),
                                      'duration', implant.getModifiedItemAttr('durationBonus'))


class Effect2887(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'emDamage', implant.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2888(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'explosiveDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2889(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'kineticDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2890(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'thermalDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2891(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'emDamage', implant.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2892(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'explosiveDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2893(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'kineticDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2894(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'thermalDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2899(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'emDamage', implant.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2900(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'explosiveDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2901(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'kineticDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2902(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'thermalDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2903(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'emDamage', implant.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2904(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'explosiveDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2905(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'kineticDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2906(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'thermalDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2907(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'emDamage', implant.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2908(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'explosiveDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2909(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'kineticDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2910(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'thermalDamage', container.getModifiedItemAttr('damageMultiplierBonus'))


class Effect2911(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Data Miners',
                                      'duration', implant.getModifiedItemAttr('durationBonus'))


class Effect2967(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        amount = -skill.getModifiedItemAttr('consumptionQuantityBonus')
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill(skill),
                                         'consumptionQuantity', amount * skill.level)


class Effect2977(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Hull Repair Systems'),
                                      'capacitorNeed', skill.getModifiedItemAttr('capNeedBonus') * skill.level)


class Effect2980(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Remote Hull Repair Systems'),
                                      'capacitorNeed', skill.getModifiedItemAttr('capNeedBonus') * skill.level)


class Effect2982(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        # We need to make sure that the attribute exists, otherwise we add attributes that don't belong.  See #927
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation') and
                                                  mod.item.getAttribute('duration'),
                                      'duration',
                                      skill.getModifiedItemAttr('projECMDurationBonus') * skill.level)

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation') and
                                                  mod.item.getAttribute('durationECMJammerBurstProjector'),
                                      'durationECMJammerBurstProjector',
                                      skill.getModifiedItemAttr('projECMDurationBonus') * skill.level)

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation') and
                                                  mod.item.getAttribute('durationTargetIlluminationBurstProjector'),
                                      'durationTargetIlluminationBurstProjector',
                                      skill.getModifiedItemAttr('projECMDurationBonus') * skill.level)

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation') and
                                                  mod.item.getAttribute('durationSensorDampeningBurstProjector'),
                                      'durationSensorDampeningBurstProjector',
                                      skill.getModifiedItemAttr('projECMDurationBonus') * skill.level)

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation') and
                                                  mod.item.getAttribute('durationWeaponDisruptionBurstProjector'),
                                      'durationWeaponDisruptionBurstProjector',
                                      skill.getModifiedItemAttr('projECMDurationBonus') * skill.level)


class Effect3001(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('speed', module.getModifiedItemAttr('overloadRofBonus'))


class Effect3002(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('duration', module.getModifiedItemAttr('overloadSelfDurationBonus') or 0)


class Effect3024(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                        'explosiveDamage', ship.getModifiedItemAttr('eliteBonusCovertOps1'),
                                        skill='Covert Ops')


class Effect3025(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('damageMultiplier', module.getModifiedItemAttr('overloadDamageModifier'))


class Effect3026(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                        'kineticDamage', ship.getModifiedItemAttr('eliteBonusCovertOps1'),
                                        skill='Covert Ops')


class Effect3027(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                        'thermalDamage', ship.getModifiedItemAttr('eliteBonusCovertOps1'),
                                        skill='Covert Ops')


class Effect3028(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                        'emDamage', ship.getModifiedItemAttr('eliteBonusCovertOps1'), skill='Covert Ops')


class Effect3029(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('emDamageResistanceBonus', module.getModifiedItemAttr('overloadHardeningBonus'))


class Effect3030(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('thermalDamageResistanceBonus', module.getModifiedItemAttr('overloadHardeningBonus'))


class Effect3031(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('explosiveDamageResistanceBonus', module.getModifiedItemAttr('overloadHardeningBonus'))


class Effect3032(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('kineticDamageResistanceBonus', module.getModifiedItemAttr('overloadHardeningBonus'))


class Effect3035(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        for type in ('kinetic', 'thermal', 'explosive', 'em'):
            module.boostItemAttr('%sDamageResistanceBonus' % type,
                                 module.getModifiedItemAttr('overloadHardeningBonus'))


class Effect3036(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Bomb',
                                      'moduleReactivationDelay', skill.getModifiedItemAttr('reactivationDelayBonus') * skill.level)


class Effect3046(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('maxVelocity', module.getModifiedItemAttr('maxVelocityModifier'), stackingPenalties=True)


class Effect3047(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('hp', module.getModifiedItemAttr('structureHPMultiplier'))


class Effect3061(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'heatDamage', module.getModifiedItemAttr('heatDamageBonus'))


class Effect3169(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'cpu',
                                      src.getModifiedItemAttr('shieldTransportCpuNeedBonus'))


class Effect3172(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        # This is actually level-less bonus, anyway you have to train cruisers 5
        # and will get 100% (20%/lvl as stated by description)
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == 'Logistic Drone',
                                     'armorDamageAmount', ship.getModifiedItemAttr('droneArmorDamageAmountBonus'))


class Effect3173(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        # This is actually level-less bonus, anyway you have to train cruisers 5
        # and will get 100% (20%/lvl as stated by description)
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == 'Logistic Drone',
                                     'shieldBonus', ship.getModifiedItemAttr('droneShieldBonusBonus'))


class Effect3174(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('maxRange', module.getModifiedItemAttr('overloadRangeBonus'),
                             stackingPenalties=True)


class Effect3175(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('speedFactor', module.getModifiedItemAttr('overloadSpeedFactorBonus'),
                             stackingPenalties=True)


class Effect3182(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        if 'projected' not in context:
            for scanType in ('Gravimetric', 'Magnetometric', 'Radar', 'Ladar'):
                module.boostItemAttr('scan{0}StrengthBonus'.format(scanType),
                                     module.getModifiedItemAttr('overloadECMStrengthBonus'),
                                     stackingPenalties=True)


class Effect3196(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: 'heatDamage' in mod.item.attributes, 'heatDamage',
                                      skill.getModifiedItemAttr('thermodynamicsHeatDamage') * skill.level)


class Effect3200(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('duration', module.getModifiedItemAttr('overloadSelfDurationBonus'))
        module.boostItemAttr('armorDamageAmount', module.getModifiedItemAttr('overloadArmorDamageAmount'),
                             stackingPenalties=True)


class Effect3201(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('duration', module.getModifiedItemAttr('overloadSelfDurationBonus'))
        module.boostItemAttr('shieldBonus', module.getModifiedItemAttr('overloadShieldBonus'), stackingPenalties=True)


class Effect3212(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('FoF Missiles'),
                                        'aoeCloudSize', container.getModifiedItemAttr('aoeCloudSizeBonus') * level)


class Effect3234(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect3235(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect3236(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect3237(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect3241(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', ship.getModifiedItemAttr('eliteBonusGunship1'),
                               skill='Assault Frigates')


class Effect3242(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance', ship.getModifiedItemAttr('eliteBonusGunship1'),
                               skill='Assault Frigates')


class Effect3243(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', ship.getModifiedItemAttr('eliteBonusGunship1'),
                               skill='Assault Frigates')


class Effect3244(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', ship.getModifiedItemAttr('eliteBonusGunship1'),
                               skill='Assault Frigates')


class Effect3249(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('rechargeRate', ship.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect3264(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        amount = -skill.getModifiedItemAttr('consumptionQuantityBonus')
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill(skill),
                                         'consumptionQuantity', amount * skill.level)


class Effect3267(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Industrial Reconfiguration'),
                                      'consumptionQuantity', ship.getModifiedItemAttr('shipBonusORECapital1'),
                                      skill='Capital Industrial Ships')


class Effect3297(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer',
                                      'energyNeutralizerAmount', ship.getModifiedItemAttr('shipBonusAB'),
                                      skill='Amarr Battleship')


class Effect3298(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer',
                                      'energyNeutralizerAmount', ship.getModifiedItemAttr('shipBonusAC'),
                                      skill='Amarr Cruiser')


class Effect3299(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer',
                                      'energyNeutralizerAmount', ship.getModifiedItemAttr('shipBonusAF'),
                                      skill='Amarr Frigate')


class Effect3313(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.ship.boostItemAttr('maxJumpClones', skill.getModifiedItemAttr('maxJumpClonesBonus') * skill.level)


class Effect3331(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorHP', ship.getModifiedItemAttr('eliteBonusCommandShips1'), skill='Command Ships')


class Effect3335(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', ship.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect3336(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', ship.getModifiedItemAttr('shipBonusMC2'),
                               skill='Minmatar Cruiser')


class Effect3339(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', ship.getModifiedItemAttr('shipBonusMC2'),
                               skill='Minmatar Cruiser')


class Effect3340(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance', ship.getModifiedItemAttr('shipBonusMC2'),
                               skill='Minmatar Cruiser')


class Effect3343(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('eliteBonusHeavyInterdictors1'),
                                      skill='Heavy Interdiction Cruisers')


class Effect3355(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('eliteBonusHeavyInterdictors1'),
                                        skill='Heavy Interdiction Cruisers')


class Effect3356(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('eliteBonusHeavyInterdictors1'),
                                        skill='Heavy Interdiction Cruisers')


class Effect3357(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('eliteBonusHeavyInterdictors1'),
                                        skill='Heavy Interdiction Cruisers')


class Effect3366(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect3367(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler',
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusElectronicAttackShip1'),
                                      skill='Electronic Attack Ships')


class Effect3369(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusElectronicAttackShip1'),
                                      skill='Electronic Attack Ships')


class Effect3370(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusElectronicAttackShip1'),
                                      skill='Electronic Attack Ships')


class Effect3371(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler',
                                      'capacitorNeed', ship.getModifiedItemAttr('eliteBonusElectronicAttackShip2'),
                                      skill='Electronic Attack Ships')


class Effect3374(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('signatureRadius', ship.getModifiedItemAttr('eliteBonusElectronicAttackShip2'),
                               skill='Electronic Attack Ships')


class Effect3379(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'capacitorNeed', implant.getModifiedItemAttr('capNeedBonus'))


class Effect3380(EffectDef):

    runTime = 'early'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context):

        if 'projected' in context:
            fit.ship.increaseItemAttr('warpScrambleStatus', module.getModifiedItemAttr('warpScrambleStrength'))
            if module.charge is not None and module.charge.ID == 45010:
                for mod in fit.modules:
                    if not mod.isEmpty and mod.item.requiresSkill('High Speed Maneuvering') and mod.state > FittingModuleState.ONLINE:
                        mod.state = FittingModuleState.ONLINE
                    if not mod.isEmpty and mod.item.requiresSkill('Micro Jump Drive Operation') and mod.state > FittingModuleState.ONLINE:
                        mod.state = FittingModuleState.ONLINE
        else:
            if module.charge is None:
                fit.ship.boostItemAttr('mass', module.getModifiedItemAttr('massBonusPercentage'))
                fit.ship.boostItemAttr('signatureRadius', module.getModifiedItemAttr('signatureRadiusBonus'))
                fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Propulsion Module',
                                              'speedBoostFactor', module.getModifiedItemAttr('speedBoostFactorBonus'))
                fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Propulsion Module',
                                          'speedFactor', module.getModifiedItemAttr('speedFactorBonus'))

            fit.ship.forceItemAttr('disallowAssistance', 1)


class Effect3392(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('eliteBonusBlackOps1'), skill='Black Ops')


class Effect3403(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        if fit.extraAttributes['cloaked']:
            fit.ship.multiplyItemAttr('maxVelocity', ship.getModifiedItemAttr('eliteBonusBlackOps2'), skill='Black Ops')


class Effect3406(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('eliteBonusBlackOps1'), skill='Black Ops')


class Effect3415(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusViolatorsRole1'))


class Effect3416(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusViolatorsRole1'))


class Effect3417(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusViolatorsRole1'))


class Effect3424(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('eliteBonusViolators1'), skill='Marauders')


class Effect3425(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('eliteBonusViolators1'), skill='Marauders')


class Effect3427(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Tractor Beam',
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusViolatorsRole2'))


class Effect3439(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter',
                                      'signatureRadiusBonus', ship.getModifiedItemAttr('eliteBonusViolators1'),
                                      skill='Marauders')


class Effect3447(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect3466(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('rechargeRate', ship.getModifiedItemAttr('eliteBonusElectronicAttackShip2'),
                               skill='Electronic Attack Ships')


class Effect3467(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('capacitorCapacity', ship.getModifiedItemAttr('eliteBonusElectronicAttackShip2'),
                               skill='Electronic Attack Ships')


class Effect3468(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Disrupt Field Generator',
                                      'warpScrambleRange', ship.getModifiedItemAttr('eliteBonusHeavyInterdictors2'),
                                      skill='Heavy Interdiction Cruisers')


class Effect3473(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Tractor Beam',
                                      'maxTractorVelocity', ship.getModifiedItemAttr('eliteBonusViolatorsRole3'))


class Effect3478(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect3480(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusAB2'), skill='Amarr Battleship')


class Effect3483(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect3484(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect3487(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect3489(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect3493(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Cargo Scanner',
                                      'cargoScanRange', ship.getModifiedItemAttr('cargoScannerRangeBonus'))


class Effect3494(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Survey Scanner',
                                      'surveyScanRange', ship.getModifiedItemAttr('surveyScannerRangeBonus'))


class Effect3495(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        groups = ('Stasis Web', 'Warp Scrambler')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'capacitorNeed', ship.getModifiedItemAttr('eliteBonusInterceptorRole'))


class Effect3496(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cyberimplant',
                                                 'agilityBonus', implant.getModifiedItemAttr('implantSetThukker'))


class Effect3498(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cyberimplant',
                                                 'scanStrengthBonus', implant.getModifiedItemAttr('implantSetSisters'))


class Effect3499(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cyberimplant',
                                                 'boosterAttributeModifier',
                                                 implant.getModifiedItemAttr('implantSetSyndicate'))


class Effect3513(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cyberimplant',
                                                 'rangeSkillBonus', implant.getModifiedItemAttr('implantSetMordus'))


class Effect3514(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler',
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusInterceptor2'), skill='Interceptors')


class Effect3519(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Bomb Deployment'),
                                      'cpu', skill.getModifiedItemAttr('cpuNeedBonus') * skill.level)


class Effect3520(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Bomb Deployment'),
                                      'power', skill.getModifiedItemAttr('powerNeedBonus') * skill.level)


class Effect3526(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Cynosural Field Generator',
                                      'consumptionQuantity',
                                      container.getModifiedItemAttr('consumptionQuantityBonusPercentage') * level)


class Effect3530(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('eliteBonusBlackOps1'), skill='Black Ops')


class Effect3532(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.ship.boostItemAttr('jumpDriveConsumptionAmount',
                               skill.getModifiedItemAttr('consumptionQuantityBonusPercentage') * skill.level)


class Effect3561(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Weapon Disruptor',
                                      'trackingSpeedBonus',
                                      container.getModifiedItemAttr('scanSkillEwStrengthBonus') * level)


class Effect3568(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Tracking Computer',
                                      'maxRangeBonus', ship.getModifiedItemAttr('eliteBonusLogistics1'),
                                      skill='Logistics Cruisers')


class Effect3569(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Tracking Computer',
                                      'maxRangeBonus', ship.getModifiedItemAttr('eliteBonusLogistics2'),
                                      skill='Logistics Cruisers')


class Effect3570(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Tracking Computer',
                                      'trackingSpeedBonus', ship.getModifiedItemAttr('eliteBonusLogistics2'),
                                      skill='Logistics Cruisers')


class Effect3571(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Tracking Computer',
                                      'trackingSpeedBonus', ship.getModifiedItemAttr('eliteBonusLogistics1'),
                                      skill='Logistics Cruisers')


class Effect3586(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        penalized = False if 'skill' in context else True
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'scanResolutionBonus',
                                      container.getModifiedItemAttr('scanSkillEwStrengthBonus') * level,
                                      stackingPenalties=penalized)


class Effect3587(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'maxTargetRangeBonus', ship.getModifiedItemAttr('shipBonusGC2'),
                                      skill='Gallente Cruiser')


class Effect3588(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'maxTargetRangeBonus', ship.getModifiedItemAttr('shipBonusGF2'),
                                      skill='Gallente Frigate')


class Effect3589(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'scanResolutionBonus', ship.getModifiedItemAttr('shipBonusGF2'),
                                      skill='Gallente Frigate')


class Effect3590(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'scanResolutionBonus', ship.getModifiedItemAttr('shipBonusGC2'),
                                      skill='Gallente Cruiser')


class Effect3591(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'maxTargetRangeBonus',
                                      container.getModifiedItemAttr('scanSkillEwStrengthBonus') * level)


class Effect3592(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('hp', ship.getModifiedItemAttr('eliteBonusJumpFreighter1'), skill='Jump Freighters')


class Effect3593(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('jumpDriveConsumptionAmount', ship.getModifiedItemAttr('eliteBonusJumpFreighter2'),
                               skill='Jump Freighters')


class Effect3597(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('scanResolutionBonus', module.getModifiedChargeAttr('scanResolutionBonusBonus'))


class Effect3598(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('maxTargetRangeBonus', module.getModifiedChargeAttr('maxTargetRangeBonusBonus'))


class Effect3599(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('trackingSpeedBonus', module.getModifiedChargeAttr('trackingSpeedBonusBonus'))


class Effect3600(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('maxRangeBonus', module.getModifiedChargeAttr('maxRangeBonusBonus'))


class Effect3601(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.forceItemAttr('disallowInEmpireSpace', module.getModifiedChargeAttr('disallowInEmpireSpace'))


class Effect3602(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('duration', module.getModifiedChargeAttr('durationBonus'))


class Effect3617(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('signatureRadiusBonus', module.getModifiedChargeAttr('signatureRadiusBonusBonus'))


class Effect3618(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('massBonusPercentage', module.getModifiedChargeAttr('massBonusPercentageBonus'))


class Effect3619(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('speedBoostFactorBonus', module.getModifiedChargeAttr('speedBoostFactorBonusBonus'))


class Effect3620(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('speedFactorBonus', module.getModifiedChargeAttr('speedFactorBonusBonus'))


class Effect3648(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('warpScrambleRange', module.getModifiedChargeAttr('warpScrambleRangeBonus'))


class Effect3649(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusViolators1'),
                                      skill='Marauders')


class Effect3650(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'maxRange', implant.getModifiedItemAttr('rangeSkillBonus'))


class Effect3651(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter',
                                      'maxRange', implant.getModifiedItemAttr('rangeSkillBonus'))


class Effect3652(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Weapon Disruptor',
                                      'maxRange', implant.getModifiedItemAttr('rangeSkillBonus'))


class Effect3653(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Burst Projectors',
                                      'maxRange', implant.getModifiedItemAttr('rangeSkillBonus'))


class Effect3655(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'maxRange', module.getModifiedItemAttr('maxRangeBonus'),
                                      stackingPenalties=True)


class Effect3656(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'trackingSpeed', module.getModifiedItemAttr('trackingSpeedBonus'),
                                      stackingPenalties=True)


class Effect3657(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('scanResolution', module.getModifiedItemAttr('scanResolutionBonus'),
                               stackingPenalties=True)


class Effect3659(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRangeBonus'),
                               stackingPenalties=True)


class Effect3660(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('maxLockedTargets', module.getModifiedItemAttr('maxLockedTargetsBonus'))


class Effect3668(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Mining Laser',
                                      'maxRange', implant.getModifiedItemAttr('maxRangeBonus'))


class Effect3669(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Frequency Mining Laser',
                                      'maxRange', implant.getModifiedItemAttr('maxRangeBonus'))


class Effect3670(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Strip Miner',
                                      'maxRange', implant.getModifiedItemAttr('maxRangeBonus'))


class Effect3671(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Gas Cloud Harvester',
                                      'maxRange', implant.getModifiedItemAttr('maxRangeBonus'))


class Effect3672(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cyberimplant',
                                                 'maxRangeBonus', implant.getModifiedItemAttr('implantSetORE'))


class Effect3677(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusAB2'), skill='Amarr Battleship')


class Effect3678(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldCapacity', ship.getModifiedItemAttr('eliteBonusJumpFreighter1'),
                               skill='Jump Freighters')


class Effect3679(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorHP', ship.getModifiedItemAttr('eliteBonusJumpFreighter1'), skill='Jump Freighters')


class Effect3680(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('freighterBonusC1'), skill='Caldari Freighter')


class Effect3681(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('freighterBonusM1'), skill='Minmatar Freighter')


class Effect3682(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('freighterBonusG1'), skill='Gallente Freighter')


class Effect3683(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('freighterBonusA1'), skill='Amarr Freighter')


class Effect3686(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('falloffBonus', module.getModifiedChargeAttr('falloffBonusBonus'))


class Effect3703(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        groups = ('Missile Launcher Rapid Light', 'Missile Launcher Heavy', 'Missile Launcher Heavy Assault')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'speed', ship.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect3705(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect3706(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect3726(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('agility', module.getModifiedItemAttr('agilityBonus'), stackingPenalties=True)


class Effect3727(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('implantBonusVelocity'),
                               stackingPenalties=True)


class Effect3739(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Tractor Beam', 'maxRange',
                                      src.getModifiedItemAttr('roleBonusTractorBeamRange'))


class Effect3740(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Tractor Beam', 'maxTractorVelocity',
                                      ship.getModifiedItemAttr('roleBonusTractorBeamVelocity'))


class Effect3742(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('specialOreHoldCapacity',
                               src.getModifiedItemAttr('shipBonusICS1'),
                               skill='Industrial Command Ships')

        fit.ship.boostItemAttr('capacity',
                               src.getModifiedItemAttr('shipBonusICS1'),
                               skill='Industrial Command Ships')


class Effect3744(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('shipBonusICS2'), skill='Industrial Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('shipBonusICS2'), skill='Industrial Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'buffDuration',
                                      src.getModifiedItemAttr('shipBonusICS2'), skill='Industrial Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('shipBonusICS2'), skill='Industrial Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('shipBonusICS2'), skill='Industrial Command Ships')


class Effect3745(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Survey Scanner', 'surveyScanRange',
                                      src.getModifiedItemAttr('roleBonusSurveyScannerRange'))


class Effect3765(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Missile Launcher Torpedo',
                                         'power', ship.getModifiedItemAttr('stealthBomberLauncherPower'))


class Effect3766(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
                                      'signatureRadiusBonus', ship.getModifiedItemAttr('eliteBonusInterceptor'),
                                      skill='Interceptors')


class Effect3767(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'aoeVelocity', ship.getModifiedItemAttr('eliteBonusCommandShips2'),
                                        skill='Command Ships')


class Effect3771(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('armorHP', module.getModifiedItemAttr('armorHPBonusAdd') or 0)


class Effect3773(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('turretSlotsLeft', module.getModifiedItemAttr('turretHardPointModifier'))
        fit.ship.increaseItemAttr('launcherSlotsLeft', module.getModifiedItemAttr('launcherHardPointModifier'))


class Effect3774(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('hiSlots', module.getModifiedItemAttr('hiSlotModifier'))
        fit.ship.increaseItemAttr('medSlots', module.getModifiedItemAttr('medSlotModifier'))
        fit.ship.increaseItemAttr('lowSlots', module.getModifiedItemAttr('lowSlotModifier'))


class Effect3782(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('powerOutput', module.getModifiedItemAttr('powerOutput'))


class Effect3783(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('cpuOutput', module.getModifiedItemAttr('cpuOutput'))


class Effect3797(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('droneBandwidth', module.getModifiedItemAttr('droneBandwidth'))


class Effect3799(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('droneCapacity', module.getModifiedItemAttr('droneCapacity'))


class Effect3807(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRange'))


class Effect3808(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('signatureRadius', module.getModifiedItemAttr('signatureRadius'))


class Effect3810(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, subsystem, context):
        fit.ship.increaseItemAttr('capacity', subsystem.getModifiedItemAttr('cargoCapacityAdd') or 0)


class Effect3811(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('capacitorCapacity', module.getModifiedItemAttr('capacitorCapacity') or 0)


class Effect3831(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('shieldCapacity', module.getModifiedItemAttr('shieldCapacity'))


class Effect3857(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('subsystemBonusAmarrPropulsion'),
                               skill='Amarr Propulsion Systems')


class Effect3859(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('maxVelocity', src.getModifiedItemAttr('subsystemBonusCaldariPropulsion'),
                               skill='Caldari Propulsion Systems')


class Effect3860(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('subsystemBonusMinmatarPropulsion'),
                               skill='Minmatar Propulsion Systems')


class Effect3861(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'speedFactor', module.getModifiedItemAttr('subsystemBonusMinmatarPropulsion'),
                                      skill='Minmatar Propulsion Systems')


class Effect3863(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'speedFactor', module.getModifiedItemAttr('subsystemBonusCaldariPropulsion'),
                                      skill='Caldari Propulsion Systems')


class Effect3864(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'speedFactor', module.getModifiedItemAttr('subsystemBonusAmarrPropulsion'),
                                      skill='Amarr Propulsion Systems')


class Effect3865(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('agility', src.getModifiedItemAttr('subsystemBonusAmarrPropulsion2'),
                               skill='Amarr Propulsion Systems')


class Effect3866(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('agility', src.getModifiedItemAttr('subsystemBonusCaldariPropulsion2'),
                               skill='Caldari Propulsion Systems')


class Effect3867(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('agility', src.getModifiedItemAttr('subsystemBonusGallentePropulsion2'),
                               skill='Gallente Propulsion Systems')


class Effect3868(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('agility', src.getModifiedItemAttr('subsystemBonusMinmatarPropulsion2'),
                               skill='Minmatar Propulsion Systems')


class Effect3869(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
                                      'signatureRadiusBonus', src.getModifiedItemAttr('subsystemBonusMinmatarPropulsion2'),
                                      skill='Minmatar Propulsion Systems')


class Effect3872(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
                                      'signatureRadiusBonus', src.getModifiedItemAttr('subsystemBonusAmarrPropulsion2'),
                                      skill='Amarr Propulsion Systems')


class Effect3875(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Propulsion Module',
                                      'capacitorNeed', module.getModifiedItemAttr('subsystemBonusGallentePropulsion'),
                                      skill='Gallente Propulsion Systems')


class Effect3893(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('scanLadarStrength', src.getModifiedItemAttr('subsystemBonusMinmatarCore'),
                               skill='Minmatar Core Systems')


class Effect3895(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('scanMagnetometricStrength', src.getModifiedItemAttr('subsystemBonusGallenteCore'),
                               skill='Gallente Core Systems')


class Effect3897(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('scanGravimetricStrength', src.getModifiedItemAttr('subsystemBonusCaldariCore'), skill='Caldari Core Systems')


class Effect3900(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('scanRadarStrength', src.getModifiedItemAttr('subsystemBonusAmarrCore'),
                               skill='Amarr Core Systems')


class Effect3959(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', module.getModifiedItemAttr('subsystemBonusAmarrDefensive'),
                                      skill='Amarr Defensive Systems')


class Effect3961(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', module.getModifiedItemAttr('subsystemBonusGallenteDefensive'),
                                      skill='Gallente Defensive Systems')


class Effect3962(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('subsystemBonusMinmatarDefensive'),
                                      skill='Minmatar Defensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', src.getModifiedItemAttr('subsystemBonusMinmatarDefensive'),
                                      skill='Minmatar Defensive Systems')


class Effect3964(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', module.getModifiedItemAttr('subsystemBonusCaldariDefensive'),
                                      skill='Caldari Defensive Systems')


class Effect3976(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('shieldCapacity', module.getModifiedItemAttr('subsystemBonusCaldariDefensive'),
                               skill='Caldari Defensive Systems')


class Effect3979(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldCapacity', src.getModifiedItemAttr('subsystemBonusMinmatarDefensive'),
                               skill='Minmatar Defensive Systems')
        fit.ship.boostItemAttr('armorHP', src.getModifiedItemAttr('subsystemBonusMinmatarDefensive'),
                               skill='Minmatar Defensive Systems')


class Effect3980(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('armorHP', module.getModifiedItemAttr('subsystemBonusGallenteDefensive'),
                               skill='Gallente Defensive Systems')


class Effect3982(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('armorHP', module.getModifiedItemAttr('subsystemBonusAmarrDefensive'),
                               skill='Amarr Defensive Systems')


class Effect3992(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr('shieldCapacity', beacon.getModifiedItemAttr('shieldCapacityMultiplier'))


class Effect3993(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr('maxTargetRange', beacon.getModifiedItemAttr('maxTargetRangeMultiplier'),
                                  stackingPenalties=True, penaltyGroup='postMul')


class Effect3995(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr('signatureRadius', beacon.getModifiedItemAttr('signatureRadiusMultiplier'),
                                  stackingPenalties=True, penaltyGroup='postMul')


class Effect3996(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', beacon.getModifiedItemAttr('armorEmDamageResistanceBonus'),
                               stackingPenalties=True)


class Effect3997(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance',
                               beacon.getModifiedItemAttr('armorExplosiveDamageResistanceBonus'),
                               stackingPenalties=True)


class Effect3998(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance',
                               beacon.getModifiedItemAttr('armorKineticDamageResistanceBonus'),
                               stackingPenalties=True)


class Effect3999(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance',
                               beacon.getModifiedItemAttr('armorThermalDamageResistanceBonus'),
                               stackingPenalties=True)


class Effect4002(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                           'maxVelocity', beacon.getModifiedItemAttr('missileVelocityMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4003(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr('maxVelocity', beacon.getModifiedItemAttr('maxVelocityMultiplier'),
                                  stackingPenalties=True, penaltyGroup='postMul')


class Effect4016(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Gunnery'),
                                         'damageMultiplier', beacon.getModifiedItemAttr('damageMultiplierMultiplier'),
                                         stackingPenalties=True)


class Effect4017(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                           'thermalDamage', beacon.getModifiedItemAttr('damageMultiplierMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4018(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                           'emDamage', beacon.getModifiedItemAttr('damageMultiplierMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4019(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                           'explosiveDamage', beacon.getModifiedItemAttr('damageMultiplierMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4020(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                           'kineticDamage', beacon.getModifiedItemAttr('damageMultiplierMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4021(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.drones.filteredItemMultiply(lambda drone: drone.item.requiresSkill('Drones'),
                                        'damageMultiplier', beacon.getModifiedItemAttr('damageMultiplierMultiplier'),
                                        stackingPenalties=True, penaltyGroup='postMul')


class Effect4022(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Gunnery'),
                                         'trackingSpeed', module.getModifiedItemAttr('trackingSpeedMultiplier'),
                                         stackingPenalties=True, penaltyGroup='postMul')


class Effect4023(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                           'aoeVelocity', beacon.getModifiedItemAttr('aoeVelocityMultiplier'))


class Effect4033(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'heatDamage' in mod.itemModifiedAttributes,
                                         'heatDamage', module.getModifiedItemAttr('heatDamageMultiplier'))


class Effect4034(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadArmorDamageAmount' in mod.itemModifiedAttributes,
                                         'overloadArmorDamageAmount', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4035(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadDamageModifier' in mod.itemModifiedAttributes,
                                         'overloadDamageModifier', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4036(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadDurationBonus' in mod.itemModifiedAttributes,
                                         'overloadDurationBonus', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4037(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadECCMStrenghtBonus' in mod.itemModifiedAttributes,
                                         'overloadECCMStrenghtBonus', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4038(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadECMStrenghtBonus' in mod.itemModifiedAttributes,
                                         'overloadECMStrenghtBonus', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4039(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadHardeningBonus' in mod.itemModifiedAttributes,
                                         'overloadHardeningBonus', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4040(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadRangeBonus' in mod.itemModifiedAttributes,
                                         'overloadRangeBonus', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4041(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadRofBonus' in mod.itemModifiedAttributes,
                                         'overloadRofBonus', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4042(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadSelfDurationBonus' in mod.itemModifiedAttributes,
                                         'overloadSelfDurationBonus', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4043(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadShieldBonus' in mod.itemModifiedAttributes,
                                         'overloadShieldBonus', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4044(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: 'overloadSpeedFactorBonus' in mod.itemModifiedAttributes,
                                         'overloadSpeedFactorBonus', module.getModifiedItemAttr('overloadBonusMultiplier'))


class Effect4045(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Smart Bomb',
                                         'empFieldRange', module.getModifiedItemAttr('empFieldRangeMultiplier'))


class Effect4046(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Smart Bomb',
                                         'emDamage', module.getModifiedItemAttr('smartbombDamageMultiplier'))


class Effect4047(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Smart Bomb',
                                         'thermalDamage', module.getModifiedItemAttr('smartbombDamageMultiplier'))


class Effect4048(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Smart Bomb',
                                         'kineticDamage', module.getModifiedItemAttr('smartbombDamageMultiplier'))


class Effect4049(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Smart Bomb',
                                         'explosiveDamage', module.getModifiedItemAttr('smartbombDamageMultiplier'))


class Effect4054(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                         'damageMultiplier', module.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                         stackingPenalties=True)


class Effect4055(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                         'damageMultiplier', module.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                         stackingPenalties=True)


class Effect4056(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                         'damageMultiplier', module.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                         stackingPenalties=True)


class Effect4057(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Rockets'),
                                           'emDamage', beacon.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4058(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Rockets'),
                                           'explosiveDamage', beacon.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4059(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Rockets'),
                                           'kineticDamage', beacon.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4060(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Rockets'),
                                           'thermalDamage', beacon.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4061(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                           'thermalDamage', beacon.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4062(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                           'emDamage', beacon.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4063(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                           'explosiveDamage', beacon.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect4086(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Repair Systems') or
                                                     mod.item.requiresSkill('Capital Repair Systems'),
                                         'armorDamageAmount', module.getModifiedItemAttr('armorDamageAmountMultiplier'),
                                         stackingPenalties=True, penaltyGroup='postMul')


class Effect4088(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                         'armorDamageAmount',
                                         module.getModifiedItemAttr('armorDamageAmountMultiplierRemote'),
                                         stackingPenalties=True)


class Effect4089(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                         'shieldBonus', module.getModifiedItemAttr('shieldBonusMultiplierRemote'),
                                         stackingPenalties=True, penaltyGroup='postMul')


class Effect4090(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr('capacitorCapacity', beacon.getModifiedItemAttr('capacitorCapacityMultiplierSystem'))


class Effect4091(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr('rechargeRate', beacon.getModifiedItemAttr('rechargeRateMultiplier'))


class Effect4093(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'damageMultiplier', module.getModifiedItemAttr('subsystemBonusAmarrOffensive'),
                                      skill='Amarr Offensive Systems')


class Effect4104(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'maxRange', module.getModifiedItemAttr('subsystemBonusCaldariOffensive'),
                                      skill='Caldari Offensive Systems')


class Effect4106(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'falloff', module.getModifiedItemAttr('subsystemBonusGallenteOffensive'),
                                      skill='Gallente Offensive Systems')


class Effect4114(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'falloff', module.getModifiedItemAttr('subsystemBonusMinmatarOffensive'),
                                      skill='Minmatar Offensive Systems')


class Effect4115(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'maxRange', module.getModifiedItemAttr('subsystemBonusMinmatarOffensive'),
                                      skill='Minmatar Offensive Systems')


class Effect4122(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Missile Launcher Heavy', 'Missile Launcher Rapid Light', 'Missile Launcher Heavy Assault')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'speed', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')


class Effect4135(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr('shieldEmDamageResonance', beacon.getModifiedItemAttr('shieldEmDamageResistanceBonus'),
                               stackingPenalties=True)


class Effect4136(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance',
                               beacon.getModifiedItemAttr('shieldExplosiveDamageResistanceBonus'),
                               stackingPenalties=True)


class Effect4137(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr('shieldKineticDamageResonance',
                               beacon.getModifiedItemAttr('shieldKineticDamageResistanceBonus'),
                               stackingPenalties=True)


class Effect4138(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance',
                               beacon.getModifiedItemAttr('shieldThermalDamageResistanceBonus'),
                               stackingPenalties=True)


class Effect4152(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      module.getModifiedItemAttr('subsystemBonusAmarrCore'),
                                      skill='Amarr Core Systems')


class Effect4153(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      module.getModifiedItemAttr('subsystemBonusCaldariCore'),
                                      skill='Caldari Core Systems')


class Effect4154(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      module.getModifiedItemAttr('subsystemBonusGallenteCore'),
                                      skill='Gallente Core Systems')


class Effect4155(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      module.getModifiedItemAttr('subsystemBonusMinmatarCore'),
                                      skill='Minmatar Core Systems')


class Effect4158(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('capacitorCapacity', src.getModifiedItemAttr('subsystemBonusCaldariCore'),
                               skill='Caldari Core Systems')


class Effect4159(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('capacitorCapacity', src.getModifiedItemAttr('subsystemBonusAmarrCore'), skill='Amarr Core Systems')


class Effect4161(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'),
                                        'baseMaxScanDeviation',
                                        container.getModifiedItemAttr('maxScanDeviationModifier') * level)


class Effect4162(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        penalized = False if 'skill' in context or 'implant' in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'),
                                        'baseSensorStrength', container.getModifiedItemAttr('scanStrengthBonus') * level,
                                        stackingPenalties=penalized)


class Effect4165(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == 'Scanner Probe',
                                        'baseSensorStrength', ship.getModifiedItemAttr('shipBonusCF2'),
                                        skill='Caldari Frigate')


class Effect4166(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == 'Scanner Probe',
                                        'baseSensorStrength', ship.getModifiedItemAttr('shipBonusMF2'),
                                        skill='Minmatar Frigate')


class Effect4167(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == 'Scanner Probe',
                                        'baseSensorStrength', ship.getModifiedItemAttr('shipBonusGF2'),
                                        skill='Gallente Frigate')


class Effect4168(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == 'Scanner Probe',
                                        'baseSensorStrength', ship.getModifiedItemAttr('eliteBonusCovertOps2'),
                                        skill='Covert Ops')


class Effect4187(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      ship.getModifiedItemAttr('shipBonusStrategicCruiserAmarr1'),
                                      skill='Amarr Strategic Cruiser')


class Effect4188(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      ship.getModifiedItemAttr('shipBonusStrategicCruiserCaldari1'),
                                      skill='Caldari Strategic Cruiser')


class Effect4189(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      ship.getModifiedItemAttr('shipBonusStrategicCruiserGallente1'),
                                      skill='Gallente Strategic Cruiser')


class Effect4190(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      ship.getModifiedItemAttr('shipBonusStrategicCruiserMinmatar1'),
                                      skill='Minmatar Strategic Cruiser')


class Effect4215(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'capacitorNeed', module.getModifiedItemAttr('subsystemBonusAmarrOffensive2'),
                                      skill='Amarr Offensive Systems')


class Effect4216(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'powerTransferAmount',
                                      src.getModifiedItemAttr('subsystemBonusAmarrCore2'), skill='Amarr Core Systems')


class Effect4217(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'energyNeutralizerAmount',
                                      src.getModifiedItemAttr('subsystemBonusAmarrCore2'), skill='Amarr Core Systems')


class Effect4248(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'kineticDamage', src.getModifiedItemAttr('subsystemBonusCaldariOffensive2'),
                                        skill='Caldari Offensive Systems')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'kineticDamage', src.getModifiedItemAttr('subsystemBonusCaldariOffensive2'),
                                        skill='Caldari Offensive Systems')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'kineticDamage', src.getModifiedItemAttr('subsystemBonusCaldariOffensive2'),
                                        skill='Caldari Offensive Systems')


class Effect4250(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'armorHP', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'),
                                     skill='Gallente Offensive Systems')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'hp', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'),
                                     skill='Gallente Offensive Systems')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'damageMultiplier', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'),
                                     skill='Gallente Offensive Systems')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'shieldCapacity', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'),
                                     skill='Gallente Offensive Systems')


class Effect4251(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', module.getModifiedItemAttr('subsystemBonusMinmatarOffensive2'),
                                      skill='Minmatar Offensive Systems')


class Effect4256(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Missile Launcher Heavy', 'Missile Launcher Rapid Light', 'Missile Launcher Heavy Assault')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'speed', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive2'),
                                      skill='Minmatar Offensive Systems')


class Effect4264(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('rechargeRate', src.getModifiedItemAttr('subsystemBonusMinmatarCore'),
                               skill='Minmatar Core Systems')


class Effect4265(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('rechargeRate', src.getModifiedItemAttr('subsystemBonusGallenteCore'),
                               skill='Gallente Core Systems')


class Effect4269(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('scanResolution', src.getModifiedItemAttr('subsystemBonusAmarrCore3'),
                               skill='Amarr Core Systems')


class Effect4270(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('scanResolution', src.getModifiedItemAttr('subsystemBonusMinmatarCore3'),
                               skill='Minmatar Core Systems')


class Effect4271(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('maxTargetRange', src.getModifiedItemAttr('subsystemBonusCaldariCore2'), skill='Caldari Core Systems')


class Effect4272(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('maxTargetRange', src.getModifiedItemAttr('subsystemBonusGallenteCore2'),
                               skill='Gallente Core Systems')


class Effect4273(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler', 'maxRange',
                                      src.getModifiedItemAttr('subsystemBonusGallenteCore2'), skill='Gallente Core Systems')


class Effect4274(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'maxRange', src.getModifiedItemAttr('subsystemBonusMinmatarCore2'), skill='Minmatar Core Systems')


class Effect4275(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', src.getModifiedItemAttr('subsystemBonusCaldariPropulsion2'),
                               skill='Caldari Propulsion Systems')


class Effect4277(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpCapacitorNeed', src.getModifiedItemAttr('subsystemBonusGallentePropulsion'),
                               skill='Gallente Propulsion Systems')


class Effect4278(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', src.getModifiedItemAttr('subsystemBonusGallentePropulsion2'),
                               skill='Gallente Propulsion Systems')


class Effect4280(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr('agility', beacon.getModifiedItemAttr('agilityMultiplier'), stackingPenalties=True)


class Effect4282(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', module.getModifiedItemAttr('subsystemBonusGallenteOffensive2'),
                                      skill='Gallente Offensive Systems')


class Effect4283(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', module.getModifiedItemAttr('subsystemBonusCaldariOffensive2'),
                                      skill='Caldari Offensive Systems')


class Effect4286(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('subsystemBonusAmarrOffensive2'), skill='Amarr Offensive Systems')


class Effect4288(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('subsystemBonusGallenteOffensive2'), skill='Gallente Offensive Systems')


class Effect4290(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems') or mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'capacitorNeed', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive2'),
                                      skill='Minmatar Offensive Systems')


class Effect4292(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'capacitorNeed', src.getModifiedItemAttr('subsystemBonusCaldariOffensive2'),
                                      skill='Caldari Offensive Systems')


class Effect4321(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'scanLadarStrengthBonus',
                                      src.getModifiedItemAttr('subsystemBonusCaldariCore2'), skill='Caldari Core Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'scanRadarStrengthBonus',
                                      src.getModifiedItemAttr('subsystemBonusCaldariCore2'), skill='Caldari Core Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'maxRange',
                                      src.getModifiedItemAttr('subsystemBonusCaldariCore2'), skill='Caldari Core Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'scanGravimetricStrengthBonus',
                                      src.getModifiedItemAttr('subsystemBonusCaldariCore2'), skill='Caldari Core Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'scanMagnetometricStrengthBonus',
                                      src.getModifiedItemAttr('subsystemBonusCaldariCore2'), skill='Caldari Core Systems')


class Effect4327(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'hp', src.getModifiedItemAttr('subsystemBonusAmarrOffensive3'), skill='Amarr Offensive Systems')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'armorHP', src.getModifiedItemAttr('subsystemBonusAmarrOffensive3'), skill='Amarr Offensive Systems')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'shieldCapacity', src.getModifiedItemAttr('subsystemBonusAmarrOffensive3'), skill='Amarr Offensive Systems')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'damageMultiplier', src.getModifiedItemAttr('subsystemBonusAmarrOffensive3'), skill='Amarr Offensive Systems')


class Effect4330(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'maxRange', module.getModifiedItemAttr('subsystemBonusAmarrOffensive3'),
                                      skill='Amarr Offensive Systems')


class Effect4331(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles') or mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'maxVelocity', src.getModifiedItemAttr('subsystemBonusCaldariOffensive3'),
                                        skill='Caldari Offensive Systems')


class Effect4342(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('maxTargetRange', src.getModifiedItemAttr('subsystemBonusMinmatarCore2'),
                               skill='Minmatar Core Systems')


class Effect4343(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('maxTargetRange', src.getModifiedItemAttr('subsystemBonusAmarrCore2'),
                               skill='Amarr Core Systems')


class Effect4347(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'trackingSpeed', module.getModifiedItemAttr('subsystemBonusGallenteOffensive3'),
                                      skill='Gallente Offensive Systems')


class Effect4351(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'trackingSpeed', module.getModifiedItemAttr('subsystemBonusMinmatarOffensive3'),
                                      skill='Minmatar Offensive Systems')


class Effect4358(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'maxRange', module.getModifiedItemAttr('ecmRangeBonus'),
                                      stackingPenalties=True)


class Effect4360(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Missile Launcher Heavy', 'Missile Launcher Rapid Light', 'Missile Launcher Heavy Assault')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'speed', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')


class Effect4362(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                        'explosiveDamage', src.getModifiedItemAttr('subsystemBonusAmarrOffensive2'), skill='Amarr Offensive Systems')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', src.getModifiedItemAttr('subsystemBonusAmarrOffensive2'), skill='Amarr Offensive Systems')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                        'emDamage', src.getModifiedItemAttr('subsystemBonusAmarrOffensive2'), skill='Amarr Offensive Systems')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                        'thermalDamage', src.getModifiedItemAttr('subsystemBonusAmarrOffensive2'), skill='Amarr Offensive Systems')


class Effect4366(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect4369(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.forceItemAttr('warpBubbleImmune', module.getModifiedItemAttr('warpBubbleImmuneModifier'))


class Effect4370(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'falloffEffectiveness', ship.getModifiedItemAttr('shipBonusCC2'),
                                      skill='Caldari Cruiser')


class Effect4372(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'falloffEffectiveness', ship.getModifiedItemAttr('shipBonusCB3'),
                                      skill='Caldari Battleship')


class Effect4373(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusAmarrOffensive'), skill='Amarr Offensive Systems')


class Effect4377(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect4378(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')


class Effect4379(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect4380(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect4384(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('eliteBonusReconShip1'),
                                        skill='Recon Ships')


class Effect4385(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('eliteBonusReconShip1'),
                                        skill='Recon Ships')


class Effect4393(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'thermalDamage', ship.getModifiedItemAttr('eliteBonusCovertOps2'),
                                        skill='Covert Ops')


class Effect4394(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'emDamage', ship.getModifiedItemAttr('eliteBonusCovertOps2'), skill='Covert Ops')


class Effect4395(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'explosiveDamage', ship.getModifiedItemAttr('eliteBonusCovertOps2'),
                                        skill='Covert Ops')


class Effect4396(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'kineticDamage', ship.getModifiedItemAttr('eliteBonusCovertOps2'),
                                        skill='Covert Ops')


class Effect4397(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'aoeVelocity', ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect4398(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'aoeVelocity', ship.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect4399(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'aoeVelocity', ship.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect4400(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'aoeVelocity', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect4413(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'explosionDelay', ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect4415(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'explosionDelay', ship.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect4416(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'explosionDelay', ship.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect4417(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'explosionDelay', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect4451(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.increaseItemAttr('scanRadarStrength', implant.getModifiedItemAttr('scanRadarStrengthModifier'))


class Effect4452(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.increaseItemAttr('scanLadarStrength', implant.getModifiedItemAttr('scanLadarStrengthModifier'))


class Effect4453(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.increaseItemAttr('scanGravimetricStrength', implant.getModifiedItemAttr('scanGravimetricStrengthModifier'))


class Effect4454(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.ship.increaseItemAttr('scanMagnetometricStrength',
                                  implant.getModifiedItemAttr('scanMagnetometricStrengthModifier'))


class Effect4456(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill('Cybernetics'),
                                                 'scanMagnetometricStrengthPercent',
                                                 implant.getModifiedItemAttr('implantSetFederationNavy'))


class Effect4457(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill('Cybernetics'),
                                                 'scanRadarStrengthPercent',
                                                 implant.getModifiedItemAttr('implantSetImperialNavy'))


class Effect4458(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill('Cybernetics'),
                                                 'scanLadarStrengthPercent',
                                                 implant.getModifiedItemAttr('implantSetRepublicFleet'))


class Effect4459(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill('Cybernetics'),
                                                 'scanGravimetricStrengthPercent',
                                                 implant.getModifiedItemAttr('implantSetCaldariNavy'))


class Effect4460(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill('Cybernetics'),
                                                 'scanRadarStrengthModifier',
                                                 implant.getModifiedItemAttr('implantSetLGImperialNavy'))


class Effect4461(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill('Cybernetics'),
                                                 'scanMagnetometricStrengthModifier',
                                                 implant.getModifiedItemAttr('implantSetLGFederationNavy'))


class Effect4462(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill('Cybernetics'),
                                                 'scanGravimetricStrengthModifier',
                                                 implant.getModifiedItemAttr('implantSetLGCaldariNavy'))


class Effect4463(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill('Cybernetics'),
                                                 'scanLadarStrengthModifier',
                                                 implant.getModifiedItemAttr('implantSetLGRepublicFleet'))


class Effect4464(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'), 'speed',
                                      src.getModifiedItemAttr('shipBonusMF'), stackingPenalties=True, skill='Minmatar Frigate')


class Effect4471(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')


class Effect4472(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusMC'), skill='Minmatar Cruiser')


class Effect4473(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('shipBonusATC1'))


class Effect4474(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusATC2'))


class Effect4475(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusATC2'))


class Effect4476(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusATF2'))


class Effect4477(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusATF2'))


class Effect4478(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Propulsion Module',
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusATF1'))


class Effect4479(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == 'Survey Probe',
                                        'explosionDelay', ship.getModifiedItemAttr('eliteBonusCovertOps3'),
                                        skill='Covert Ops')


class Effect4482(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect4484(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusGB'), skill='Gallente Battleship')


class Effect4485(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'speedFactor', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect4489(EffectDef):

    type = 'active'


class Effect4490(EffectDef):

    type = 'active'


class Effect4491(EffectDef):

    type = 'active'


class Effect4492(EffectDef):

    type = 'active'


class Effect4510(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'speedFactor', ship.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect4512(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect4513(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'speedFactor', ship.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')


class Effect4515(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect4516(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect4527(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                      'falloff', module.getModifiedItemAttr('falloffBonus'),
                                      stackingPenalties=True)


class Effect4555(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'),
                                        'emDamage', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect4556(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'),
                                        'explosiveDamage', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect4557(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'),
                                        'kineticDamage', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect4558(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'),
                                        'thermalDamage', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect4559(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        for attr in ('maxRange', 'falloff', 'trackingSpeed'):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          attr, module.getModifiedItemAttr('%sBonus' % attr),
                                          stackingPenalties=True)


class Effect4575(EffectDef):

    runTime = 'early'
    type = 'active'

    @staticmethod
    def handler(fit, src, context):
        fit.extraAttributes['siege'] = True
        fit.ship.boostItemAttr('maxVelocity', src.getModifiedItemAttr('speedFactor'), stackingPenalties=True)
        fit.ship.multiplyItemAttr('mass', src.getModifiedItemAttr('siegeMassMultiplier'))
        fit.ship.multiplyItemAttr('scanResolution',
                                  src.getModifiedItemAttr('scanResolutionMultiplier'),
                                  stackingPenalties=True)

        #  Remote Shield Repper Bonuses
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Emission Systems'),
                                      'duration',
                                      src.getModifiedItemAttr('industrialCoreRemoteLogisticsDurationBonus'),
                                      )
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Emission Systems'),
                                      'maxRange',
                                      src.getModifiedItemAttr('industrialCoreRemoteLogisticsRangeBonus'),
                                      stackingPenalties=True
                                      )
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Emission Systems'),
                                      'capacitorNeed',
                                      src.getModifiedItemAttr('industrialCoreRemoteLogisticsDurationBonus')
                                      )
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Emission Systems'),
                                      'falloffEffectiveness',
                                      src.getModifiedItemAttr('industrialCoreRemoteLogisticsRangeBonus'),
                                      stackingPenalties=True
                                      )

        #  Local Shield Repper Bonuses
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Operation'),
                                      'duration',
                                      src.getModifiedItemAttr('industrialCoreLocalLogisticsDurationBonus'),
                                      )
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Operation'),
                                      'shieldBonus',
                                      src.getModifiedItemAttr('industrialCoreLocalLogisticsAmountBonus'),
                                      stackingPenalties=True
                                      )

        # Mining Burst Bonuses
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'),
                                      'warfareBuff1Value',
                                      src.getModifiedItemAttr('industrialCoreBonusMiningBurstStrength'),
                                      )

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'),
                                      'warfareBuff2Value',
                                      src.getModifiedItemAttr('industrialCoreBonusMiningBurstStrength'),
                                      )

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'),
                                      'warfareBuff3Value',
                                      src.getModifiedItemAttr('industrialCoreBonusMiningBurstStrength'),
                                      )

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'),
                                      'warfareBuff4Value',
                                      src.getModifiedItemAttr('industrialCoreBonusMiningBurstStrength'),
                                      )

        #  Command Burst Range Bonus
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Leadership'),
                                      'maxRange',
                                      src.getModifiedItemAttr('industrialCoreBonusCommandBurstRange'),
                                      stackingPenalties=True
                                      )

        # Drone Bonuses
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Ice Harvesting Drone Operation'),
                                     'duration',
                                     src.getModifiedItemAttr('industrialCoreBonusDroneIceHarvesting'),
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Mining Drone Operation'),
                                     'miningAmount',
                                     src.getModifiedItemAttr('industrialCoreBonusDroneMining'),
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'maxVelocity',
                                     src.getModifiedItemAttr('industrialCoreBonusDroneVelocity'),
                                     )

        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier',
                                     src.getModifiedItemAttr('industrialCoreBonusDroneDamageHP'),
                                     stackingPenalties=True
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'shieldCapacity',
                                     src.getModifiedItemAttr('industrialCoreBonusDroneDamageHP'),
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'armorHP',
                                     src.getModifiedItemAttr('industrialCoreBonusDroneDamageHP'),
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'hp',
                                     src.getModifiedItemAttr('industrialCoreBonusDroneDamageHP'),
                                     )

        #  Todo: remote impedance (no reps, etc)
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('siegeModeWarpStatus'))
        fit.ship.boostItemAttr('remoteRepairImpedance', src.getModifiedItemAttr('remoteRepairImpedanceBonus'))
        fit.ship.increaseItemAttr('disallowTethering', src.getModifiedItemAttr('disallowTethering'))
        fit.ship.boostItemAttr('sensorDampenerResistance', src.getModifiedItemAttr('sensorDampenerResistanceBonus'))
        fit.ship.boostItemAttr('remoteAssistanceImpedance', src.getModifiedItemAttr('remoteAssistanceImpedanceBonus'))
        fit.ship.increaseItemAttr('disallowDocking', src.getModifiedItemAttr('disallowDocking'))


class Effect4576(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Tracking Computer',
                                      'falloffBonus', ship.getModifiedItemAttr('eliteBonusLogistics1'),
                                      skill='Logistics Cruisers')


class Effect4577(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Tracking Computer',
                                      'falloffBonus', ship.getModifiedItemAttr('eliteBonusLogistics2'),
                                      skill='Logistics Cruisers')


class Effect4579(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == 'Stasis Webifying Drone',
                                     'speedFactor', module.getModifiedItemAttr('webSpeedFactorBonus'))


class Effect4619(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect4620(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect4621(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      ship.getModifiedItemAttr('shipBonusATF1'))


class Effect4622(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusATF2'))


class Effect4623(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusATF2'))


class Effect4624(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusATC2'))


class Effect4625(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusATC2'))


class Effect4626(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect4635(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        damageTypes = ('em', 'explosive', 'kinetic', 'thermal')
        for damageType in damageTypes:
            fit.modules.filteredChargeBoost(
                lambda mod: mod.charge.requiresSkill('Cruise Missiles') or mod.charge.requiresSkill('Torpedoes'),
                '{0}Damage'.format(damageType), ship.getModifiedItemAttr('eliteBonusViolatorsRole1'))


class Effect4636(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Cruise Missiles') or mod.charge.requiresSkill('Torpedoes'),
            'aoeVelocity', ship.getModifiedItemAttr('shipBonus2CB'), skill='Caldari Battleship')


class Effect4637(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Cruise Missiles') or mod.charge.requiresSkill('Torpedoes'),
            'maxVelocity', ship.getModifiedItemAttr('shipBonusCB3'), skill='Caldari Battleship')


class Effect4640(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        damageTypes = ('Em', 'Explosive', 'Kinetic', 'Thermal')
        for damageType in damageTypes:
            fit.ship.boostItemAttr('armor{0}DamageResonance'.format(damageType), ship.getModifiedItemAttr('shipBonusAC2'),
                                   skill='Amarr Cruiser')


class Effect4643(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        damageTypes = ('em', 'explosive', 'kinetic', 'thermal')
        for damageType in damageTypes:
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                            '{0}Damage'.format(damageType), ship.getModifiedItemAttr('shipBonusAC'),
                                            skill='Amarr Cruiser')


class Effect4645(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        groups = ('Missile Launcher Rapid Light', 'Missile Launcher Heavy Assault', 'Missile Launcher Heavy')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'speed', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                      skill='Heavy Assault Cruisers')


class Effect4648(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        sensorTypes = ('Gravimetric', 'Ladar', 'Magnetometric', 'Radar')
        for type in sensorTypes:
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'scan{0}StrengthBonus'.format(type),
                                          ship.getModifiedItemAttr('eliteBonusBlackOps1'), skill='Black Ops')


class Effect4649(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        affectedGroups = ('Missile Launcher Cruise', 'Missile Launcher Torpedo')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in affectedGroups,
                                      'speed', ship.getModifiedItemAttr('shipBonus2CB'), skill='Caldari Battleship')


class Effect4667(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Salvaging'),
                                      'duration', ship.getModifiedItemAttr('shipBonusOreIndustrial1'),
                                      skill='ORE Industrial')


class Effect4668(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Tractor Beam',
                                      'duration', ship.getModifiedItemAttr('shipBonusOreIndustrial1'),
                                      skill='ORE Industrial')


class Effect4669(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Tractor Beam',
                                      'maxTractorVelocity', ship.getModifiedItemAttr('shipBonusOreIndustrial2'),
                                      skill='ORE Industrial')


class Effect4670(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Tractor Beam',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusOreIndustrial2'),
                                      skill='ORE Industrial')


class Effect4728(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        damages = ('em', 'thermal', 'kinetic', 'explosive')
        for damage in damages:
            # Nerf missile damage
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                            '{0}Damage'.format(damage),
                                            beacon.getModifiedItemAttr('systemEffectDamageReduction'))
            # Nerf smartbomb damage
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Smart Bomb',
                                          '{0}Damage'.format(damage),
                                          beacon.getModifiedItemAttr('systemEffectDamageReduction'))
            # Nerf armor resistances
            fit.ship.boostItemAttr('armor{0}DamageResonance'.format(damage.capitalize()),
                                   beacon.getModifiedItemAttr('armor{0}DamageResistanceBonus'.format(damage.capitalize())))
            # Nerf shield resistances
            fit.ship.boostItemAttr('shield{0}DamageResonance'.format(damage.capitalize()),
                                   beacon.getModifiedItemAttr('shield{0}DamageResistanceBonus'.format(damage.capitalize())))
        # Nerf drone damage output
        fit.drones.filteredItemBoost(lambda drone: True,
                                     'damageMultiplier', beacon.getModifiedItemAttr('systemEffectDamageReduction'))
        # Nerf turret damage output
        fit.modules.filteredItemBoost(lambda module: module.item.requiresSkill('Gunnery'),
                                      'damageMultiplier', beacon.getModifiedItemAttr('systemEffectDamageReduction'))


class Effect4760(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpCapacitorNeed', src.getModifiedItemAttr('subsystemBonusCaldariPropulsion'),
                               skill='Caldari Propulsion Systems')


class Effect4775(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer',
                                      'energyNeutralizerAmount', ship.getModifiedItemAttr('shipBonus2AF'),
                                      skill='Amarr Frigate')


class Effect4782(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusATF2'))


class Effect4789(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusATF1'))


class Effect4793(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Heavy',
                                      'speed', ship.getModifiedItemAttr('shipBonusATC1'))


class Effect4794(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Rapid Light',
                                      'speed', ship.getModifiedItemAttr('shipBonusATC1'))


class Effect4795(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Heavy Assault',
                                      'speed', ship.getModifiedItemAttr('shipBonusATC1'))


class Effect4799(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        sensorTypes = ('Gravimetric', 'Ladar', 'Magnetometric', 'Radar')
        for type in sensorTypes:
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Burst Jammer',
                                          'scan{0}StrengthBonus'.format(type),
                                          ship.getModifiedItemAttr('eliteBonusBlackOps1'), skill='Black Ops')


class Effect4804(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill(skill), 'accessDifficultyBonus',
                                         skill.getModifiedItemAttr('accessDifficultyBonusAbsolutePercent') * skill.level)


class Effect4809(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'scanGravimetricStrengthBonus', module.getModifiedItemAttr('ecmStrengthBonusPercent'),
                                      stackingPenalties=True)


class Effect4810(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'scanLadarStrengthBonus', module.getModifiedItemAttr('ecmStrengthBonusPercent'),
                                      stackingPenalties=True)


class Effect4811(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'scanMagnetometricStrengthBonus',
                                      module.getModifiedItemAttr('ecmStrengthBonusPercent'),
                                      stackingPenalties=True)


class Effect4812(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                      'scanRadarStrengthBonus', module.getModifiedItemAttr('ecmStrengthBonusPercent'),
                                      stackingPenalties=True)


class Effect4814(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), 'consumptionQuantity',
                                      skill.getModifiedItemAttr('consumptionQuantityBonusPercent') * skill.level)


class Effect4817(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Salvager',
                                      'duration', implant.getModifiedItemAttr('durationBonus'))


class Effect4820(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                         'power', ship.getModifiedItemAttr('bcLargeTurretPower'))


class Effect4821(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                         'power', ship.getModifiedItemAttr('bcLargeTurretPower'))


class Effect4822(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                         'power', ship.getModifiedItemAttr('bcLargeTurretPower'))


class Effect4823(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                         'cpu', ship.getModifiedItemAttr('bcLargeTurretCPU'))


class Effect4824(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                         'cpu', ship.getModifiedItemAttr('bcLargeTurretCPU'))


class Effect4825(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                         'cpu', ship.getModifiedItemAttr('bcLargeTurretCPU'))


class Effect4826(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                         'capacitorNeed', ship.getModifiedItemAttr('bcLargeTurretCap'))


class Effect4827(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                         'capacitorNeed', ship.getModifiedItemAttr('bcLargeTurretCap'))


class Effect4867(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Special Edition Implant',
                                                 'powerEngineeringOutputBonus',
                                                 implant.getModifiedItemAttr('implantSetChristmas'))


class Effect4868(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Special Edition Implant',
                                                 'capacitorCapacityBonus',
                                                 implant.getModifiedItemAttr('implantSetChristmas'))


class Effect4869(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Special Edition Implant',
                                                 'cpuOutputBonus2', implant.getModifiedItemAttr('implantSetChristmas'))


class Effect4871(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Special Edition Implant',
                                                 'capRechargeBonus', implant.getModifiedItemAttr('implantSetChristmas'))


class Effect4896(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'hp', ship.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect4897(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect4898(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect4901(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'speed', ship.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect4902(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
                                      'signatureRadiusBonus', ship.getModifiedItemAttr('MWDSignatureRadiusBonus'))


class Effect4906(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.drones.filteredItemMultiply(lambda drone: drone.item.requiresSkill('Fighters'),
                                        'damageMultiplier', beacon.getModifiedItemAttr('damageMultiplierMultiplier'),
                                        stackingPenalties=True, penaltyGroup='postMul')


class Effect4911(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('shieldRechargeRate', module.getModifiedItemAttr('shieldRechargeRateMultiplier'))


class Effect4921(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('signatureRadius', module.getModifiedItemAttr('signatureRadiusBonusPercent'))


class Effect4923(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Micro Jump Drive Operation'),
                                      'duration', skill.getModifiedItemAttr('durationBonus') * skill.level)


class Effect4928(EffectDef):

    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        # pyfalog = Logger(__name__)

        damagePattern = fit.damagePattern
        # pyfalog.debug('==============================')

        static_adaptive_behavior = eos.config.settings['useStaticAdaptiveArmorHardener']

        if (damagePattern.emAmount == damagePattern.thermalAmount == damagePattern.kineticAmount == damagePattern.explosiveAmount) and static_adaptive_behavior:
            # pyfalog.debug('Setting adaptivearmorhardener resists to uniform profile.')
            for attr in ('armorEmDamageResonance', 'armorThermalDamageResonance', 'armorKineticDamageResonance', 'armorExplosiveDamageResonance'):
                fit.ship.multiplyItemAttr(attr, module.getModifiedItemAttr(attr), stackingPenalties=True, penaltyGroup='preMul')
            return

        # Skip if there is no damage pattern. Example: projected ships or fleet boosters
        if damagePattern:

            # Populate a tuple with the damage profile modified by current armor resists.
            baseDamageTaken = (
                damagePattern.emAmount * fit.ship.getModifiedItemAttr('armorEmDamageResonance'),
                damagePattern.thermalAmount * fit.ship.getModifiedItemAttr('armorThermalDamageResonance'),
                damagePattern.kineticAmount * fit.ship.getModifiedItemAttr('armorKineticDamageResonance'),
                damagePattern.explosiveAmount * fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance'),
            )
            # pyfalog.debug('Damage Adjusted for Armor Resists: %f/%f/%f/%f' % (baseDamageTaken[0], baseDamageTaken[1], baseDamageTaken[2], baseDamageTaken[3]))

            resistanceShiftAmount = module.getModifiedItemAttr(
                'resistanceShiftAmount') / 100  # The attribute is in percent and we want a fraction
            RAHResistance = [
                module.getModifiedItemAttr('armorEmDamageResonance'),
                module.getModifiedItemAttr('armorThermalDamageResonance'),
                module.getModifiedItemAttr('armorKineticDamageResonance'),
                module.getModifiedItemAttr('armorExplosiveDamageResonance'),
            ]

            # Simulate RAH cycles until the RAH either stops changing or enters a loop.
            # The number of iterations is limited to prevent an infinite loop if something goes wrong.
            cycleList = []
            loopStart = -20
            for num in range(50):
                # pyfalog.debug('Starting cycle %d.' % num)
                # The strange order is to emulate the ingame sorting when different types have taken the same amount of damage.
                # This doesn't take into account stacking penalties. In a few cases fitting a Damage Control causes an inaccurate result.
                damagePattern_tuples = [
                    (0, baseDamageTaken[0] * RAHResistance[0], RAHResistance[0]),
                    (3, baseDamageTaken[3] * RAHResistance[3], RAHResistance[3]),
                    (2, baseDamageTaken[2] * RAHResistance[2], RAHResistance[2]),
                    (1, baseDamageTaken[1] * RAHResistance[1], RAHResistance[1]),
                ]

                # Sort the tuple to drop the highest damage value to the bottom
                sortedDamagePattern_tuples = sorted(damagePattern_tuples, key=lambda damagePattern: damagePattern[1])

                if sortedDamagePattern_tuples[2][1] == 0:
                    # One damage type: the top damage type takes from the other three
                    # Since the resistances not taking damage will end up going to the type taking damage we just do the whole thing at once.
                    change0 = 1 - sortedDamagePattern_tuples[0][2]
                    change1 = 1 - sortedDamagePattern_tuples[1][2]
                    change2 = 1 - sortedDamagePattern_tuples[2][2]
                    change3 = -(change0 + change1 + change2)
                elif sortedDamagePattern_tuples[1][1] == 0:
                    # Two damage types: the top two damage types take from the other two
                    # Since the resistances not taking damage will end up going equally to the types taking damage we just do the whole thing at once.
                    change0 = 1 - sortedDamagePattern_tuples[0][2]
                    change1 = 1 - sortedDamagePattern_tuples[1][2]
                    change2 = -(change0 + change1) / 2
                    change3 = -(change0 + change1) / 2
                else:
                    # Three or four damage types: the top two damage types take from the other two
                    change0 = min(resistanceShiftAmount, 1 - sortedDamagePattern_tuples[0][2])
                    change1 = min(resistanceShiftAmount, 1 - sortedDamagePattern_tuples[1][2])
                    change2 = -(change0 + change1) / 2
                    change3 = -(change0 + change1) / 2

                RAHResistance[sortedDamagePattern_tuples[0][0]] = sortedDamagePattern_tuples[0][2] + change0
                RAHResistance[sortedDamagePattern_tuples[1][0]] = sortedDamagePattern_tuples[1][2] + change1
                RAHResistance[sortedDamagePattern_tuples[2][0]] = sortedDamagePattern_tuples[2][2] + change2
                RAHResistance[sortedDamagePattern_tuples[3][0]] = sortedDamagePattern_tuples[3][2] + change3
                # pyfalog.debug('Resistances shifted to %f/%f/%f/%f' % ( RAHResistance[0], RAHResistance[1], RAHResistance[2], RAHResistance[3]))

                # See if the current RAH profile has been encountered before, indicating a loop.
                for i, val in enumerate(cycleList):
                    tolerance = 1e-06
                    if abs(RAHResistance[0] - val[0]) <= tolerance and \
                                abs(RAHResistance[1] - val[1]) <= tolerance and \
                                abs(RAHResistance[2] - val[2]) <= tolerance and \
                                abs(RAHResistance[3] - val[3]) <= tolerance:
                        loopStart = i
                        # pyfalog.debug('Loop found: %d-%d' % (loopStart, num))
                        break
                if loopStart >= 0:
                    break

                cycleList.append(list(RAHResistance))

            # if loopStart < 0:
                # pyfalog.error('Reactive Armor Hardener failed to find equilibrium. Damage profile after armor: {0}/{1}/{2}/{3}'.format(
                #             baseDamageTaken[0], baseDamageTaken[1], baseDamageTaken[2], baseDamageTaken[3]))

            # Average the profiles in the RAH loop, or the last 20 if it didn't find a loop.
            loopCycles = cycleList[loopStart:]
            numCycles = len(loopCycles)
            average = [0, 0, 0, 0]
            for cycle in loopCycles:
                for i in range(4):
                    average[i] += cycle[i]

            for i in range(4):
                average[i] = round(average[i] / numCycles, 3)

            # Set the new resistances
            # pyfalog.debug('Setting new resist profile: %f/%f/%f/%f' % ( average[0], average[1], average[2],average[3]))
            for i, attr in enumerate((
                    'armorEmDamageResonance', 'armorThermalDamageResonance', 'armorKineticDamageResonance',
                    'armorExplosiveDamageResonance')):
                module.increaseItemAttr(attr, average[i] - module.getModifiedItemAttr(attr))
                fit.ship.multiplyItemAttr(attr, average[i], stackingPenalties=True, penaltyGroup='preMul')


class Effect4934(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('shipBonusGF2'),
                                      skill='Gallente Frigate')


class Effect4936(EffectDef):

    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr('shieldBonus')
        speed = module.getModifiedItemAttr('duration') / 1000.0
        fit.extraAttributes.increase('shieldRepair', amount / speed)


class Effect4941(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect4942(EffectDef):

    type = 'active'


class Effect4945(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Breaker',
                                      'duration', skill.getModifiedItemAttr('durationBonus') * skill.level)


class Effect4946(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Breaker',
                                      'capacitorNeed', skill.getModifiedItemAttr('capNeedBonus') * skill.level)


class Effect4950(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect4951(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Operation') or mod.item.requiresSkill('Capital Shield Operation'),
            'shieldBonus', container.getModifiedItemAttr('shieldBoostMultiplier'))


class Effect4961(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Shield Operation') or
                                                     mod.item.requiresSkill('Capital Shield Operation'),
                                         'shieldBonus', module.getModifiedItemAttr('shieldBonusMultiplier'),
                                         stackingPenalties=True, penaltyGroup='postMul')


class Effect4967(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Operation') or mod.item.requiresSkill('Capital Shield Operation'),
            'duration', module.getModifiedItemAttr('durationSkillBonus'))


class Effect4970(EffectDef):

    attr = 'boosterShieldBoostAmountPenalty'
    displayName = 'Shield Boost'
    type = 'boosterSideEffect'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'), 'shieldBonus',
                                      src.getModifiedItemAttr('boosterShieldBoostAmountPenalty'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Operation'), 'shieldBonus',
                                      src.getModifiedItemAttr('boosterShieldBoostAmountPenalty'))


class Effect4972(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Light',
                                      'speed', ship.getModifiedItemAttr('eliteBonusGunship1'), skill='Assault Frigates')


class Effect4973(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Rocket',
                                      'speed', ship.getModifiedItemAttr('eliteBonusGunship1'), skill='Assault Frigates')


class Effect4974(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', ship.getModifiedItemAttr('eliteBonusViolators2'), skill='Marauders')


class Effect4975(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusATF2'))


class Effect4976(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Resistance Shift Hardener', 'duration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Resistance Phasing'), 'duration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)


class Effect4989(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'aoeCloudSize', implant.getModifiedItemAttr('aoeCloudSizeBonus'))


class Effect4990(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'capacitorNeed', ship.getModifiedItemAttr('rookieSETCapBonus'))


class Effect4991(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('rookieSETDamageBonus'))


class Effect4994(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', ship.getModifiedItemAttr('rookieArmorResistanceBonus'))


class Effect4995(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', ship.getModifiedItemAttr('rookieArmorResistanceBonus'))


class Effect4996(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', ship.getModifiedItemAttr('rookieArmorResistanceBonus'))


class Effect4997(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance', ship.getModifiedItemAttr('rookieArmorResistanceBonus'))


class Effect4999(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('rookieSHTOptimalBonus'))


class Effect5000(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('rookieMissileKinDamageBonus'))


class Effect5008(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldEmDamageResonance', ship.getModifiedItemAttr('rookieShieldResistBonus'))


class Effect5009(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', ship.getModifiedItemAttr('rookieShieldResistBonus'))


class Effect5011(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldKineticDamageResonance', ship.getModifiedItemAttr('rookieShieldResistBonus'))


class Effect5012(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', ship.getModifiedItemAttr('rookieShieldResistBonus'))


class Effect5013(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('rookieSHTDamageBonus'))


class Effect5014(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier', ship.getModifiedItemAttr('rookieDroneBonus'))


class Effect5015(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'maxTargetRangeBonus', ship.getModifiedItemAttr('rookieDampStrengthBonus'))


class Effect5016(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'scanResolutionBonus', ship.getModifiedItemAttr('rookieDampStrengthBonus'))


class Effect5017(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('rookieArmorRepBonus'))


class Effect5018(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('maxVelocity', ship.getModifiedItemAttr('rookieShipVelocityBonus'))


class Effect5019(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter',
                                      'signatureRadiusBonus', ship.getModifiedItemAttr('rookieTargetPainterStrengthBonus'))


class Effect5020(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('rookieSPTDamageBonus'))


class Effect5021(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', ship.getModifiedItemAttr('rookieShieldBoostBonus'))


class Effect5028(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for type in ('Gravimetric', 'Ladar', 'Radar', 'Magnetometric'):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM',
                                          'scan{0}StrengthBonus'.format(type),
                                          ship.getModifiedItemAttr('rookieECMStrengthBonus'))


class Effect5029(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Mining Drone Operation'),
                                     'miningAmount',
                                     src.getModifiedItemAttr('roleBonusDroneMiningYield'),
                                     )


class Effect5030(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Mining Drone Operation'),
                                     'miningAmount', container.getModifiedItemAttr('rookieDroneBonus'))


class Effect5035(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for type in ('shieldCapacity', 'armorHP', 'hp'):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                         type, ship.getModifiedItemAttr('rookieDroneBonus'))


class Effect5036(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Salvaging'),
                                      'duration', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect5045(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Salvaging'),
                                      'duration', ship.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect5048(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Salvaging'),
                                      'duration', ship.getModifiedItemAttr('shipBonusGF'), skill='Amarr Frigate')


class Effect5051(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Salvaging'),
                                      'duration', ship.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect5055(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Ice Harvesting'),
                                         'duration', ship.getModifiedItemAttr('iceHarvestCycleBonus'))


class Effect5058(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Mining'),
                                         'miningAmount', module.getModifiedItemAttr('miningAmountMultiplier'))


class Effect5059(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting'),
                                      'duration', container.getModifiedItemAttr('shipBonusORE3'), skill='Mining Barge')


class Effect5066(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Target Painting'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect5067(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('specialOreHoldCapacity', ship.getModifiedItemAttr('shipBonusORE2'), skill='Mining Barge')


class Effect5068(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldCapacity', ship.getModifiedItemAttr('shipBonusORE2'), skill='Mining Barge')


class Effect5069(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Mercoxit Processing'),
                                        'specialisationAsteroidYieldMultiplier',
                                        module.getModifiedItemAttr('miningAmountBonus'))


class Effect5079(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect5080(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect5081(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRangeBonus'),
                               stackingPenalties=True)


class Effect5087(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for layer in ('shieldCapacity', 'armorHP', 'hp'):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                         layer, ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect5090(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect5103(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect5104(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect5105(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect5106(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')


class Effect5107(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect5108(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('shipBonusGF2'),
                                      skill='Gallente Frigate')


class Effect5109(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect5110(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect5111(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'trackingSpeed', ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect5119(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == 'Scanner Probe',
                                        'baseSensorStrength', ship.getModifiedItemAttr('shipBonus2AF'),
                                        skill='Amarr Frigate')


class Effect5121(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Capacitor Transmitter',
                                      'powerTransferAmount', ship.getModifiedItemAttr('energyTransferAmountBonus'))


class Effect5122(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusMC'), skill='Minmatar Cruiser')


class Effect5123(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect5124(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect5125(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('shipBonusGC2'),
                                      skill='Gallente Cruiser')


class Effect5126(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect5127(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect5128(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect5129(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter',
                                      'signatureRadiusBonus', ship.getModifiedItemAttr('shipBonusMC'),
                                      skill='Minmatar Cruiser')


class Effect5131(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        groups = ('Missile Launcher Heavy', 'Missile Launcher Rapid Light', 'Missile Launcher Heavy Assault')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'speed', ship.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect5132(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect5133(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect5136(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect5139(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining'),
                                      'miningAmount', module.getModifiedItemAttr('shipBonusOREfrig1'),
                                      skill='Mining Frigate')


class Effect5142(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Gas Cloud Harvester',
                                         'miningAmount', module.getModifiedItemAttr('miningAmountMultiplier'))


class Effect5153(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5156(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Gas Cloud Harvester',
                                      'duration', module.getModifiedItemAttr('shipBonusOREfrig2'), skill='Mining Frigate')


class Effect5162(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Resistance Shift Hardener', 'capacitorNeed',
                                      src.getModifiedItemAttr('capNeedBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Resistance Phasing'), 'capacitorNeed',
                                      src.getModifiedItemAttr('capNeedBonus') * lvl)


class Effect5165(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'maxVelocity', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5168(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.drones.filteredItemIncrease(lambda drone: drone.item.requiresSkill('Salvage Drone Operation'),
                                        'accessDifficultyBonus',
                                        container.getModifiedItemAttr('accessDifficultyBonus') * container.level)


class Effect5180(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.ship.boostItemAttr('scanGravimetricStrength',
                               container.getModifiedItemAttr('sensorStrengthBonus') * container.level)


class Effect5181(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.ship.boostItemAttr('scanLadarStrength', container.getModifiedItemAttr('sensorStrengthBonus') * container.level)


class Effect5182(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.ship.boostItemAttr('scanMagnetometricStrength',
                               container.getModifiedItemAttr('sensorStrengthBonus') * container.level)


class Effect5183(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.ship.boostItemAttr('scanRadarStrength', container.getModifiedItemAttr('sensorStrengthBonus') * container.level)


class Effect5185(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'powerTransferAmount', ship.getModifiedItemAttr('shipBonus2AF'),
                                      skill='Amarr Frigate')


class Effect5187(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Sensor Dampener',
                                      'falloffEffectiveness', ship.getModifiedItemAttr('shipBonusGC'),
                                      skill='Gallente Cruiser')


class Effect5188(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Hybrid Weapon',
                                      'trackingSpeed', module.getModifiedItemAttr('trackingSpeedBonus'),
                                      stackingPenalties=True)


class Effect5189(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Weapon',
                                      'trackingSpeed', module.getModifiedItemAttr('trackingSpeedBonus'),
                                      stackingPenalties=True)


class Effect5190(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Projectile Weapon',
                                      'trackingSpeed', module.getModifiedItemAttr('trackingSpeedBonus'),
                                      stackingPenalties=True)


class Effect5201(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Armor Reinforcer',
                                      'massAddition', container.getModifiedItemAttr('massPenaltyReduction') * level)


class Effect5205(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('rookieSETTracking'))


class Effect5206(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('rookieSETOptimal'))


class Effect5207(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'powerTransferAmount', ship.getModifiedItemAttr('rookieNosDrain'))


class Effect5208(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer',
                                      'energyNeutralizerAmount', ship.getModifiedItemAttr('rookieNeutDrain'))


class Effect5209(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'speedFactor', ship.getModifiedItemAttr('rookieWebAmount'))


class Effect5212(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda mod: True,
                                     'maxVelocity', ship.getModifiedItemAttr('rookieDroneMWDspeed'))


class Effect5213(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'maxVelocity', ship.getModifiedItemAttr('rookieRocketVelocity'))


class Effect5214(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('rookieLightMissileVelocity'))


class Effect5215(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('rookieSHTTracking'))


class Effect5216(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'falloff', ship.getModifiedItemAttr('rookieSHTFalloff'))


class Effect5217(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('rookieSPTTracking'))


class Effect5218(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('rookieSPTFalloff'))


class Effect5219(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'maxRange', ship.getModifiedItemAttr('rookieSPTOptimal'))


class Effect5220(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5221(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5222(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5223(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5224(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5225(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5226(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5227(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5228(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5229(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'),
                                        'baseSensorStrength', container.getModifiedItemAttr('shipBonusRole8'))


class Effect5230(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        for damageType in ('kinetic', 'thermal', 'explosive', 'em'):
            fit.ship.boostItemAttr('shield' + damageType.capitalize() + 'DamageResonance',
                                   module.getModifiedItemAttr(damageType + 'DamageResistanceBonus'),
                                   stackingPenalties=True)


class Effect5231(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        for damageType in ('kinetic', 'thermal', 'explosive', 'em'):
            fit.ship.boostItemAttr('armor%sDamageResonance' % damageType.capitalize(),
                                   module.getModifiedItemAttr('%sDamageResistanceBonus' % damageType),
                                   stackingPenalties=True)


class Effect5234(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Rockets') or mod.charge.requiresSkill('Light Missiles'),
            'explosiveDamage', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect5237(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Rockets') or mod.charge.requiresSkill('Light Missiles'),
            'kineticDamage', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect5240(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Rockets') or mod.charge.requiresSkill('Light Missiles'),
            'thermalDamage', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect5243(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Rockets') or mod.charge.requiresSkill('Light Missiles'),
            'emDamage', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect5259(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Cloaking Device',
                                      'cpu', ship.getModifiedItemAttr('eliteBonusReconShip1'), skill='Recon Ships')


class Effect5260(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Cloaking'),
                                      'cpu', ship.getModifiedItemAttr('eliteBonusCovertOps1'), skill='Covert Ops')


class Effect5261(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.increaseItemAttr('cpu', module.getModifiedItemAttr('covertCloakCPUAdd') or 0)


class Effect5262(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Cloaking'),
                                         'covertCloakCPUAdd', module.getModifiedItemAttr('covertCloakCPUPenalty'))


class Effect5263(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Cynosural Field Theory'),
                                         'covertCloakCPUAdd', module.getModifiedItemAttr('covertCloakCPUPenalty'))


class Effect5264(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.increaseItemAttr('cpu', module.getModifiedItemAttr('warfareLinkCPUAdd') or 0)


class Effect5265(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Leadership'),
                                         'warfareLinkCPUAdd', module.getModifiedItemAttr('warfareLinkCPUPenalty'))


class Effect5266(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Cloaking Device',
                                      'cpu', ship.getModifiedItemAttr('eliteIndustrialCovertCloakBonus'),
                                      skill='Transport Ships')


class Effect5267(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'power', module.getModifiedItemAttr('drawback'))


class Effect5268(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Repair Systems'),
                                      'power', module.getModifiedItemAttr('drawback'))


class Effect5275(EffectDef):

    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        if module.charge and module.charge.name == 'Nanite Repair Paste':
            multiplier = 3
        else:
            multiplier = 1

        amount = module.getModifiedItemAttr('armorDamageAmount') * multiplier
        speed = module.getModifiedItemAttr('duration') / 1000.0
        rps = amount / speed
        fit.extraAttributes.increase('armorRepair', rps)
        fit.extraAttributes.increase('armorRepairPreSpool', rps)
        fit.extraAttributes.increase('armorRepairFullSpool', rps)


class Effect5293(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusAD1'), skill='Amarr Destroyer')


class Effect5294(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusAD2'), skill='Amarr Destroyer')


class Effect5295(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'damageMultiplier',
                                     src.getModifiedItemAttr('shipBonusAD1'), skill='Amarr Destroyer')


class Effect5300(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'shieldCapacity',
                                     src.getModifiedItemAttr('shipBonusAD1'), skill='Amarr Destroyer')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'hp',
                                     src.getModifiedItemAttr('shipBonusAD1'), skill='Amarr Destroyer')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'armorHP',
                                     src.getModifiedItemAttr('shipBonusAD1'), skill='Amarr Destroyer')


class Effect5303(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusCD1'), skill='Caldari Destroyer')


class Effect5304(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusCD2'), skill='Caldari Destroyer')


class Effect5305(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusCD1'),
                                        skill='Caldari Destroyer')


class Effect5306(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusCD1'),
                                        skill='Caldari Destroyer')


class Effect5307(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'aoeVelocity', ship.getModifiedItemAttr('shipBonusCD2'), skill='Caldari Destroyer')


class Effect5308(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'aoeVelocity', ship.getModifiedItemAttr('shipBonusCD2'), skill='Caldari Destroyer')


class Effect5309(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusGD1'), skill='Gallente Destroyer')


class Effect5310(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusGD2'), skill='Gallente Destroyer')


class Effect5311(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'damageMultiplier',
                                     src.getModifiedItemAttr('shipBonusGD1'), skill='Gallente Destroyer')


class Effect5316(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'shieldCapacity',
                                     src.getModifiedItemAttr('shipBonusGD1'), skill='Gallente Destroyer')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'armorHP',
                                     src.getModifiedItemAttr('shipBonusGD1'), skill='Gallente Destroyer')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'hp',
                                     src.getModifiedItemAttr('shipBonusGD1'), skill='Gallente Destroyer')


class Effect5317(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusMD1'),
                                      skill='Minmatar Destroyer')


class Effect5318(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusMD2'), skill='Minmatar Destroyer')


class Effect5319(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusMD1'),
                                        skill='Minmatar Destroyer')


class Effect5320(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusMD1'),
                                        skill='Minmatar Destroyer')


class Effect5321(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
                                      'signatureRadiusBonus', ship.getModifiedItemAttr('shipBonusMD2'),
                                      skill='Minmatar Destroyer')


class Effect5322(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', ship.getModifiedItemAttr('shipBonusABC1'),
                               skill='Amarr Battlecruiser')


class Effect5323(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', ship.getModifiedItemAttr('shipBonusABC1'),
                               skill='Amarr Battlecruiser')


class Effect5324(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', ship.getModifiedItemAttr('shipBonusABC1'),
                               skill='Amarr Battlecruiser')


class Effect5325(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance', ship.getModifiedItemAttr('shipBonusABC1'),
                               skill='Amarr Battlecruiser')


class Effect5326(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusABC2'),
                                     skill='Amarr Battlecruiser')


class Effect5331(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for layer in ('shieldCapacity', 'armorHP', 'hp'):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                         layer, ship.getModifiedItemAttr('shipBonusABC2'), skill='Amarr Battlecruiser')


class Effect5332(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusABC1'),
                                      skill='Amarr Battlecruiser')


class Effect5333(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusABC2'),
                                      skill='Amarr Battlecruiser')


class Effect5334(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusCBC1'), skill='Caldari Battlecruiser')


class Effect5335(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldEmDamageResonance', ship.getModifiedItemAttr('shipBonusCBC2'),
                               skill='Caldari Battlecruiser')


class Effect5336(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', ship.getModifiedItemAttr('shipBonusCBC2'),
                               skill='Caldari Battlecruiser')


class Effect5337(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldKineticDamageResonance', ship.getModifiedItemAttr('shipBonusCBC2'),
                               skill='Caldari Battlecruiser')


class Effect5338(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', ship.getModifiedItemAttr('shipBonusCBC2'),
                               skill='Caldari Battlecruiser')


class Effect5339(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusCBC1'),
                                        skill='Caldari Battlecruiser')


class Effect5340(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusCBC1'),
                                        skill='Caldari Battlecruiser')


class Effect5341(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusGBC1'),
                                      skill='Gallente Battlecruiser')


class Effect5342(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('shipBonusGBC2'),
                                      skill='Gallente Battlecruiser')


class Effect5343(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusGBC1'),
                                     skill='Gallente Battlecruiser')


class Effect5348(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for layer in ('shieldCapacity', 'armorHP', 'hp'):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                         layer, ship.getModifiedItemAttr('shipBonusGBC1'), skill='Gallente Battlecruiser')


class Effect5349(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Heavy',
                                      'speed', ship.getModifiedItemAttr('shipBonusMBC2'), skill='Minmatar Battlecruiser')


class Effect5350(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Heavy Assault',
                                      'speed', ship.getModifiedItemAttr('shipBonusMBC2'), skill='Minmatar Battlecruiser')


class Effect5351(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusMBC1'),
                                      skill='Minmatar Battlecruiser')


class Effect5352(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusMBC1'),
                                      skill='Minmatar Battlecruiser')


class Effect5353(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusMBC2'), skill='Minmatar Battlecruiser')


class Effect5354(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusABC1'),
                                      skill='Amarr Battlecruiser')


class Effect5355(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusABC2'),
                                      skill='Amarr Battlecruiser')


class Effect5356(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusCBC1'), skill='Caldari Battlecruiser')


class Effect5357(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusCBC2'),
                                      skill='Caldari Battlecruiser')


class Effect5358(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusGBC1'),
                                      skill='Gallente Battlecruiser')


class Effect5359(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusGBC2'),
                                      skill='Gallente Battlecruiser')


class Effect5360(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusMBC1'), skill='Minmatar Battlecruiser')


class Effect5361(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusMBC2'), skill='Minmatar Battlecruiser')


class Effect5364(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Repair Systems') or mod.item.requiresSkill('Capital Repair Systems'),
            'armorDamageAmount', booster.getModifiedItemAttr('armorDamageAmountBonus') or 0)


class Effect5365(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('eliteBonusViolators2'),
                                      skill='Marauders')


class Effect5366(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('shipBonusATC2'))


class Effect5367(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('shipBonusGB2'),
                                      skill='Gallente Battleship')


class Effect5378(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'aoeCloudSize', ship.getModifiedItemAttr('shipBonusCBC1'),
                                        skill='Caldari Battlecruiser')


class Effect5379(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'aoeCloudSize', ship.getModifiedItemAttr('shipBonusCBC1'),
                                        skill='Caldari Battlecruiser')


class Effect5380(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusGBC2'),
                                      skill='Gallente Battlecruiser')


class Effect5381(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusABC1'),
                                      skill='Amarr Battlecruiser')


class Effect5382(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect5383(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect5384(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect5385(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect5386(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect5387(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'aoeCloudSize', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect5388(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'aoeCloudSize', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect5389(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'trackingSpeed', ship.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect5390(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'maxVelocity', ship.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect5397(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'),
                                        'baseMaxScanDeviation',
                                        module.getModifiedItemAttr('maxScanDeviationModifierModule'),
                                        stackingPenalties=True)


class Effect5398(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Astrometrics'),
                                      'duration', module.getModifiedItemAttr('scanDurationBonus'))


class Effect5399(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'),
                                        'baseSensorStrength', module.getModifiedItemAttr('scanStrengthBonusModule'),
                                        stackingPenalties=True)


class Effect5402(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusABC2'),
                                        skill='Amarr Battlecruiser')


class Effect5403(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusABC2'),
                                        skill='Amarr Battlecruiser')


class Effect5410(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusABC2'),
                                      skill='Amarr Battlecruiser')


class Effect5411(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusCD1'), skill='Caldari Destroyer')


class Effect5417(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusAB'), skill='Amarr Battleship')


class Effect5418(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusAB'), skill='Amarr Battleship')


class Effect5419(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusAB'), skill='Amarr Battleship')


class Effect5420(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'hp', ship.getModifiedItemAttr('shipBonusAB'), skill='Amarr Battleship')


class Effect5424(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusGB'), skill='Gallente Battleship')


class Effect5427(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'trackingSpeed', ship.getModifiedItemAttr('shipBonusGB'), skill='Gallente Battleship')


class Effect5428(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'maxRange', ship.getModifiedItemAttr('shipBonusGB'), skill='Gallente Battleship')


class Effect5429(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'aoeVelocity', ship.getModifiedItemAttr('shipBonusMB2'),
                                        skill='Minmatar Battleship')


class Effect5430(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'aoeVelocity', ship.getModifiedItemAttr('shipBonusMB2'),
                                        skill='Minmatar Battleship')


class Effect5431(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusAB'), skill='Amarr Battleship')


class Effect5433(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Hacking'),
                                         'virusCoherence', container.getModifiedItemAttr('virusCoherenceBonus') * level)


class Effect5437(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Archaeology'),
                                         'virusCoherence', container.getModifiedItemAttr('virusCoherenceBonus') * level)


class Effect5440(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                           'kineticDamage', beacon.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5444(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'aoeCloudSize', ship.getModifiedItemAttr('shipBonusCB'), skill='Caldari Battleship')


class Effect5445(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'aoeCloudSize', ship.getModifiedItemAttr('shipBonusCB'), skill='Caldari Battleship')


class Effect5456(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Cruise',
                                      'speed', ship.getModifiedItemAttr('shipBonusCB'), skill='Caldari Battleship')


class Effect5457(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Torpedo',
                                      'speed', ship.getModifiedItemAttr('shipBonusCB'), skill='Caldari Battleship')


class Effect5459(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Hacking'), 'virusStrength', src.getModifiedItemAttr('virusStrengthBonus'))


class Effect5460(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemIncrease(
            lambda mod: (mod.item.requiresSkill('Hacking') or mod.item.requiresSkill('Archaeology')),
            'virusStrength', container.getModifiedItemAttr('virusStrengthBonus') * level)


class Effect5461(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('shieldRechargeRate', module.getModifiedItemAttr('rechargeratebonus') or 0)


class Effect5468(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('shipBonusCI2'), skill='Caldari Industrial')


class Effect5469(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('shipBonusMI2'), skill='Minmatar Industrial')


class Effect5470(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('shipBonusGI2'), skill='Gallente Industrial')


class Effect5471(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('shipBonusAI2'), skill='Amarr Industrial')


class Effect5476(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('specialOreHoldCapacity', ship.getModifiedItemAttr('shipBonusGI2'),
                               skill='Gallente Industrial')


class Effect5477(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('specialAmmoHoldCapacity', ship.getModifiedItemAttr('shipBonusMI2'),
                               skill='Minmatar Industrial')


class Effect5478(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('specialPlanetaryCommoditiesHoldCapacity', ship.getModifiedItemAttr('shipBonusGI2'),
                               skill='Gallente Industrial')


class Effect5479(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('specialMineralHoldCapacity', ship.getModifiedItemAttr('shipBonusGI2'),
                               skill='Gallente Industrial')


class Effect5480(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Special Edition Implant',
                                                 'implantBonusVelocity', implant.getModifiedItemAttr('implantSetChristmas'))


class Effect5482(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Special Edition Implant',
                                                 'agilityBonus', implant.getModifiedItemAttr('implantSetChristmas'))


class Effect5483(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Special Edition Implant',
                                                 'shieldCapacityBonus', implant.getModifiedItemAttr('implantSetChristmas'))


class Effect5484(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Special Edition Implant',
                                                 'armorHpBonus2', implant.getModifiedItemAttr('implantSetChristmas'))


class Effect5485(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect5486(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusMBC2'),
                                      skill='Minmatar Battlecruiser')


class Effect5496(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Heavy Assault',
                                      'speed', ship.getModifiedItemAttr('eliteBonusCommandShips1'), skill='Command Ships')


class Effect5497(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Heavy',
                                      'speed', ship.getModifiedItemAttr('eliteBonusCommandShips1'), skill='Command Ships')


class Effect5498(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'aoeVelocity', ship.getModifiedItemAttr('eliteBonusCommandShips2'),
                                        skill='Command Ships')


class Effect5499(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'aoeCloudSize', ship.getModifiedItemAttr('eliteBonusCommandShips2'),
                                        skill='Command Ships')


class Effect5500(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'aoeCloudSize', ship.getModifiedItemAttr('eliteBonusCommandShips2'),
                                        skill='Command Ships')


class Effect5501(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusCommandShips2'),
                                      skill='Command Ships')


class Effect5502(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('eliteBonusCommandShips1'),
                                      skill='Command Ships')


class Effect5503(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'trackingSpeed', ship.getModifiedItemAttr('eliteBonusCommandShips2'),
                                     skill='Command Ships')


class Effect5504(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'maxVelocity', ship.getModifiedItemAttr('eliteBonusCommandShips2'),
                                     skill='Command Ships')


class Effect5505(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'speed', ship.getModifiedItemAttr('eliteBonusCommandShips1'), skill='Command Ships')


class Effect5514(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        damageTypes = ('em', 'explosive', 'kinetic', 'thermal')
        for damageType in damageTypes:
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                            '{0}Damage'.format(damageType),
                                            ship.getModifiedItemAttr('eliteBonusCommandShips2'), skill='Command Ships')


class Effect5521(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        damageTypes = ('em', 'explosive', 'kinetic', 'thermal')
        for damageType in damageTypes:
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                            '{0}Damage'.format(damageType),
                                            ship.getModifiedItemAttr('eliteBonusCommandShips2'), skill='Command Ships')


class Effect5539(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect5540(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect5541(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect5542(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect5552(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                        skill='Heavy Assault Cruisers')


class Effect5553(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'maxVelocity', ship.getModifiedItemAttr('eliteBonusHeavyGunship1'),
                                        skill='Heavy Assault Cruisers')


class Effect5554(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('shipBonusGC2'),
                                      skill='Gallente Cruiser')


class Effect5555(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'maxVelocity', ship.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect5556(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'trackingSpeed', ship.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect5557(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'maxRange', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                     skill='Heavy Assault Cruisers')


class Effect5558(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'trackingSpeed', ship.getModifiedItemAttr('eliteBonusHeavyGunship2'),
                                     skill='Heavy Assault Cruisers')


class Effect5559(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect5560(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Micro Jump Drive',
                                      'moduleReactivationDelay', ship.getModifiedItemAttr('roleBonusMarauder'))


class Effect5564(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusCaldariOffensive'), skill='Caldari Offensive Systems')


class Effect5568(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusGallenteOffensive'), skill='Gallente Offensive Systems')


class Effect5570(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'),
                                      'war'
                                      'fareBuff1Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'buffDuration', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive'), skill='Minmatar Offensive Systems')


class Effect5572(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'buffDuration',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')


class Effect5573(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'buffDuration',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')


class Effect5574(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'buffDuration',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')


class Effect5575(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'buffDuration',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('eliteBonusCommandShips3'), skill='Command Ships')


class Effect5607(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capacitor Emission Systems'),
                                      'capacitorNeed', container.getModifiedItemAttr('capNeedBonus') * level)


class Effect5610(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusAB'), skill='Amarr Battleship')


class Effect5611(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusGB2'), skill='Gallente Battleship')


class Effect5618(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Rapid Heavy',
                                      'speed', ship.getModifiedItemAttr('shipBonus2CB'), skill='Caldari Battleship')


class Effect5619(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Rapid Heavy',
                                      'speed', ship.getModifiedItemAttr('shipBonusCB'), skill='Caldari Battleship')


class Effect5620(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Rapid Heavy',
                                      'speed', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect5621(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Cruise',
                                      'speed', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect5622(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Torpedo',
                                      'speed', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect5628(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect5629(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusMB'),
                                        skill='Minmatar Battleship')


class Effect5630(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusMB'),
                                        skill='Minmatar Battleship')


class Effect5631(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusMB'),
                                        skill='Minmatar Battleship')


class Effect5632(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusMB'),
                                        skill='Minmatar Battleship')


class Effect5633(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect5634(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusMB'),
                                        skill='Minmatar Battleship')


class Effect5635(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusMB'),
                                        skill='Minmatar Battleship')


class Effect5636(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusMB'), skill='Minmatar Battleship')


class Effect5637(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusMB'),
                                        skill='Minmatar Battleship')


class Effect5638(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusMB'),
                                        skill='Minmatar Battleship')


class Effect5639(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusMB'),
                                        skill='Minmatar Battleship')


class Effect5644(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect5647(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Cloaking'),
                                      'cpu', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5650(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        damageTypes = ('Em', 'Explosive', 'Kinetic', 'Thermal')
        for damageType in damageTypes:
            fit.ship.boostItemAttr('armor{0}DamageResonance'.format(damageType), ship.getModifiedItemAttr('shipBonusAF'),
                                   skill='Amarr Frigate')


class Effect5657(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        damageTypes = ('Em', 'Explosive', 'Kinetic', 'Thermal')
        for damageType in damageTypes:
            fit.ship.boostItemAttr('shield{0}DamageResonance'.format(damageType),
                                   ship.getModifiedItemAttr('eliteBonusInterceptor2'), skill='Interceptors')


class Effect5673(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusInterceptor2'),
                                      skill='Interceptors')


class Effect5676(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Rockets') or mod.charge.requiresSkill('Light Missiles'),
            'aoeCloudSize', ship.getModifiedItemAttr('shipBonusCD2'), skill='Caldari Destroyer')


class Effect5688(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', ship.getModifiedItemAttr('shipBonusAD2'), skill='Amarr Destroyer')


class Effect5695(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for damageType in ('Em', 'Thermal', 'Explosive', 'Kinetic'):
            fit.ship.boostItemAttr('armor%sDamageResonance' % damageType,
                                   ship.getModifiedItemAttr('eliteBonusInterdictors1'), skill='Interdictors')


class Effect5717(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == 'Cyberimplant',
                                                 'WarpSBonus', implant.getModifiedItemAttr('implantSetWarpSpeed'))


class Effect5721(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5722(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusGD1'), skill='Gallente Destroyer')


class Effect5723(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
                                      'signatureRadiusBonus', ship.getModifiedItemAttr('eliteBonusInterdictors2'),
                                      skill='Interdictors')


class Effect5724(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect5725(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5726(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5733(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'explosiveDamage', ship.getModifiedItemAttr('eliteBonusViolatorsRole1'))


class Effect5734(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'kineticDamage', ship.getModifiedItemAttr('eliteBonusViolatorsRole1'))


class Effect5735(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'emDamage', ship.getModifiedItemAttr('eliteBonusViolatorsRole1'))


class Effect5736(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'thermalDamage', ship.getModifiedItemAttr('eliteBonusViolatorsRole1'))


class Effect5737(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'),
                                        'baseSensorStrength', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5738(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusRole8'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'falloffEffectiveness', ship.getModifiedItemAttr('shipBonusRole8'))


class Effect5754(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('maxRangeBonus', module.getModifiedItemAttr('overloadTrackingModuleStrengthBonus'))
        module.boostItemAttr('falloffBonus', module.getModifiedItemAttr('overloadTrackingModuleStrengthBonus'))
        module.boostItemAttr('trackingSpeedBonus', module.getModifiedItemAttr('overloadTrackingModuleStrengthBonus'))


class Effect5757(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('maxTargetRangeBonus', module.getModifiedItemAttr('overloadSensorModuleStrengthBonus'))
        module.boostItemAttr('scanResolutionBonus', module.getModifiedItemAttr('overloadSensorModuleStrengthBonus'),
                             stackingPenalties=True)

        for scanType in ('Gravimetric', 'Magnetometric', 'Radar', 'Ladar'):
            module.boostItemAttr(
                'scan{}StrengthPercent'.format(scanType),
                module.getModifiedItemAttr('overloadSensorModuleStrengthBonus'),
                stackingPenalties=True
            )


class Effect5758(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('signatureRadiusBonus', module.getModifiedItemAttr('overloadPainterStrengthBonus') or 0)


class Effect5769(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == 'Logistic Drone',
                                     'structureDamageAmount', container.getModifiedItemAttr('damageHP') * level)


class Effect5778(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'speed', ship.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')


class Effect5779(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')


class Effect5793(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        for attr in ('maxRangeBonus', 'falloffBonus'):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'),
                                          attr, container.getModifiedItemAttr('scanSkillEwStrengthBonus') * level)


class Effect5802(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'speedFactor', module.getModifiedItemAttr('shipBonus2CB'), skill='Caldari Battleship')


class Effect5803(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5804(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5805(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'hp', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5806(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5807(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5808(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5809(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5810(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'hp', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5811(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusGB2'),
                                        skill='Gallente Battleship')


class Effect5812(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusGB2'),
                                        skill='Gallente Battleship')


class Effect5813(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'speedFactor', module.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect5814(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect5815(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect5816(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Light Drone Operation'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5817(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Light Drone Operation'),
                                     'hp', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5818(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Light Drone Operation'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5819(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Light Drone Operation'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5820(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'speedFactor', module.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect5821(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Medium Drone Operation'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5822(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Medium Drone Operation'),
                                     'hp', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5823(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Medium Drone Operation'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5824(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Medium Drone Operation'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusRole7'))


class Effect5825(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect5826(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect5827(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusAF'), skill='Amarr Frigate')


class Effect5829(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining'),
                                      'duration', ship.getModifiedItemAttr('shipBonusORE3'), skill='Mining Barge')


class Effect5832(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Mining') or mod.item.requiresSkill('Ice Harvesting'),
            'maxRange', ship.getModifiedItemAttr('shipBonusORE2'), skill='Mining Barge')


class Effect5839(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for damageType in ('em', 'thermal', 'explosive', 'kinetic'):
            fit.ship.boostItemAttr('shield{}DamageResonance'.format(damageType.capitalize()),
                                   ship.getModifiedItemAttr('eliteBonusBarge1'), skill='Exhumers')


class Effect5840(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining'),
                                      'duration', ship.getModifiedItemAttr('eliteBonusBarge2'), skill='Exhumers')


class Effect5852(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining'),
                                      'miningAmount', module.getModifiedItemAttr('eliteBonusExpedition1'),
                                      skill='Expedition Frigates')


class Effect5853(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('signatureRadius', ship.getModifiedItemAttr('eliteBonusExpedition2'),
                               skill='Expedition Frigates')


class Effect5862(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'emDamage', ship.getModifiedItemAttr('shipBonusCB'), skill='Caldari Battleship')


class Effect5863(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'kineticDamage', ship.getModifiedItemAttr('shipBonusCB'),
                                        skill='Caldari Battleship')


class Effect5864(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'thermalDamage', ship.getModifiedItemAttr('shipBonusCB'),
                                        skill='Caldari Battleship')


class Effect5865(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'explosiveDamage', ship.getModifiedItemAttr('shipBonusCB'),
                                        skill='Caldari Battleship')


class Effect5866(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler',
                                      'maxRange', ship.getModifiedItemAttr('shipBonusGB'), skill='Gallente Battleship')


class Effect5867(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'explosionDelay', ship.getModifiedItemAttr('shipBonusRole8'))


class Effect5868(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('capacity', module.getModifiedItemAttr('drawback'))


class Effect5869(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', ship.getModifiedItemAttr('eliteBonusIndustrial1'),
                               skill='Transport Ships')


class Effect5870(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusCI2'), skill='Caldari Industrial')


class Effect5871(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', ship.getModifiedItemAttr('shipBonusMI2'), skill='Minmatar Industrial')


class Effect5872(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('shipBonusAI2'),
                                      skill='Amarr Industrial')


class Effect5873(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', ship.getModifiedItemAttr('shipBonusGI2'),
                                      skill='Gallente Industrial')


class Effect5874(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('fleetHangarCapacity', ship.getModifiedItemAttr('eliteBonusIndustrial1'),
                               skill='Transport Ships')


class Effect5881(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for damageType in ('em', 'thermal', 'explosive', 'kinetic'):
            fit.ship.boostItemAttr('shield{}DamageResonance'.format(damageType.capitalize()),
                                   ship.getModifiedItemAttr('eliteBonusIndustrial2'), skill='Transport Ships')


class Effect5888(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for damageType in ('em', 'thermal', 'explosive', 'kinetic'):
            fit.ship.boostItemAttr('armor{}DamageResonance'.format(damageType.capitalize()),
                                   ship.getModifiedItemAttr('eliteBonusIndustrial2'), skill='Transport Ships')


class Effect5889(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'),
                                      'overloadSpeedFactorBonus', ship.getModifiedItemAttr('roleBonusOverheatDST'))


class Effect5890(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
                                      'overloadSpeedFactorBonus', ship.getModifiedItemAttr('roleBonusOverheatDST'))


class Effect5891(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'),
                                      'overloadHardeningBonus', ship.getModifiedItemAttr('roleBonusOverheatDST'))


class Effect5892(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'),
                                      'overloadSelfDurationBonus', ship.getModifiedItemAttr('roleBonusOverheatDST'))


class Effect5893(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Tactical Shield Manipulation'),
                                      'overloadHardeningBonus', ship.getModifiedItemAttr('roleBonusOverheatDST'))


class Effect5896(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'overloadShieldBonus', ship.getModifiedItemAttr('roleBonusOverheatDST'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'overloadSelfDurationBonus', ship.getModifiedItemAttr('roleBonusOverheatDST'))


class Effect5899(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'overloadArmorDamageAmount', ship.getModifiedItemAttr('roleBonusOverheatDST'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'overloadSelfDurationBonus', ship.getModifiedItemAttr('roleBonusOverheatDST'))


class Effect5900(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('warpSpeedMultiplier', module.getModifiedItemAttr('warpSpeedAdd'))


class Effect5901(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Reinforced Bulkhead',
                                      'cpu', ship.getModifiedItemAttr('cpuNeedBonus'))


class Effect5911(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('jumpDriveConsumptionAmount',
                               module.getModifiedItemAttr('consumptionQuantityBonusPercentage'), stackingPenalties=True)


class Effect5912(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Remote Capacitor Transmitter',
                                         'powerTransferAmount', beacon.getModifiedItemAttr('energyTransferAmountBonus'),
                                         stackingPenalties=True, penaltyGroup='postMul')


class Effect5913(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr('armorHP', beacon.getModifiedItemAttr('armorHPMultiplier'))


class Effect5914(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Energy Neutralizer',
                                         'energyNeutralizerAmount',
                                         beacon.getModifiedItemAttr('energyWarfareStrengthMultiplier'),
                                         stackingPenalties=True, penaltyGroup='postMul')


class Effect5915(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                         'powerTransferAmount',
                                         beacon.getModifiedItemAttr('energyWarfareStrengthMultiplier'),
                                         stackingPenalties=True, penaltyGroup='postMul')


class Effect5916(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                           'explosiveDamage', beacon.getModifiedItemAttr('smartbombDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5917(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                           'kineticDamage', beacon.getModifiedItemAttr('smartbombDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5918(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                           'thermalDamage', beacon.getModifiedItemAttr('smartbombDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5919(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                           'emDamage', beacon.getModifiedItemAttr('smartbombDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5920(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                           'aoeCloudSize', beacon.getModifiedItemAttr('aoeCloudSizeMultiplier'))


class Effect5921(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Target Painting'),
                                         'signatureRadiusBonus',
                                         beacon.getModifiedItemAttr('targetPainterStrengthMultiplier'),
                                         stackingPenalties=True, penaltyGroup='postMul')


class Effect5922(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Stasis Web',
                                         'speedFactor', beacon.getModifiedItemAttr('stasisWebStrengthMultiplier'),
                                         stackingPenalties=True, penaltyGroup='postMul')


class Effect5923(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                           'energyNeutralizerAmount',
                                           beacon.getModifiedItemAttr('smartbombDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5924(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                           'scanGravimetricStrengthBonus',
                                           beacon.getModifiedItemAttr('smartbombDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5925(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                           'scanLadarStrengthBonus',
                                           beacon.getModifiedItemAttr('smartbombDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5926(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                           'scanMagnetometricStrengthBonus',
                                           beacon.getModifiedItemAttr('smartbombDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5927(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Bomb Deployment'),
                                           'scanRadarStrengthBonus',
                                           beacon.getModifiedItemAttr('smartbombDamageMultiplier'),
                                           stackingPenalties=True, penaltyGroup='postMul')


class Effect5929(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.drones.filteredItemMultiply(lambda drone: True,
                                        'trackingSpeed', beacon.getModifiedItemAttr('trackingSpeedMultiplier'),
                                        stackingPenalties=True, penaltyGroup='postMul')


class Effect5934(EffectDef):

    runTime = 'early'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context):
        if 'projected' not in context:
            return

        fit.ship.increaseItemAttr('warpScrambleStatus', module.getModifiedItemAttr('warpScrambleStrength'))

        # this is such a dirty hack
        for mod in fit.modules:
            if not mod.isEmpty and mod.state > FittingModuleState.ONLINE and (
                    mod.item.requiresSkill('Micro Jump Drive Operation') or
                    mod.item.requiresSkill('High Speed Maneuvering')
            ):
                mod.state = FittingModuleState.ONLINE
            if not mod.isEmpty and mod.item.requiresSkill('Micro Jump Drive Operation') and mod.state > FittingModuleState.ONLINE:
                mod.state = FittingModuleState.ONLINE


class Effect5938(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Rockets') or mod.charge.requiresSkill('Light Missiles'),
            'aoeCloudSize', ship.getModifiedItemAttr('shipBonusCF2'), skill='Caldari Frigate')


class Effect5939(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Rocket',
                                      'speed', ship.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect5940(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'speed', ship.getModifiedItemAttr('eliteBonusInterdictors1'), skill='Interdictors')


class Effect5944(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'speed', ship.getModifiedItemAttr('shipBonusAD1'), skill='Amarr Destroyer')


class Effect5945(EffectDef):

    runTime = 'early'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        # Set flag which is used to determine if ship is cloaked or not
        # This is used to apply cloak-only bonuses, like Black Ops' speed bonus
        # Doesn't apply to covops cloaks
        fit.extraAttributes['cloaked'] = True
        # Apply speed penalty
        fit.ship.multiplyItemAttr('maxVelocity', module.getModifiedItemAttr('maxVelocityModifier'))


class Effect5951(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', module.getModifiedItemAttr('drawback'), stackingPenalties=True)


class Effect5956(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect5957(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusHeavyInterdictors1'),
                                      skill='Heavy Interdiction Cruisers')


class Effect5958(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect5959(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusHeavyInterdictors1'),
                                      skill='Heavy Interdiction Cruisers')


class Effect5994(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
            tgtAttr = '{}DamageResonance'.format(dmgType)
            fit.ship.forceItemAttr(tgtAttr, module.getModifiedItemAttr('resistanceKillerHull'))


class Effect5995(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for layer in ('armor', 'shield'):
            for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
                tgtAttr = '{}{}DamageResonance'.format(layer, dmgType.capitalize())
                fit.ship.forceItemAttr(tgtAttr, module.getModifiedItemAttr('resistanceKiller'))


class Effect5998(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        # todo: stacking?
        fit.ship.boostItemAttr('agility', ship.getModifiedItemAttr('freighterBonusO2'), skill='ORE Freighter',
                               stackingPenalties=True)


class Effect6001(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('shipMaintenanceBayCapacity', ship.getModifiedItemAttr('freighterBonusO1'),
                               skill='ORE Freighter')


class Effect6006(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusTacticalDestroyerAmarr1'),
                                      skill='Amarr Tactical Destroyer')


class Effect6007(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusTacticalDestroyerAmarr2'),
                                      skill='Amarr Tactical Destroyer')


class Effect6008(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      ship.getModifiedItemAttr('shipBonusTacticalDestroyerAmarr3'),
                                      skill='Amarr Tactical Destroyer')


class Effect6009(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Astrometrics'), 'cpu', src.getModifiedItemAttr('roleBonusT3ProbeCPU'))


class Effect6010(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr(
            'maxTargetRange',
            1 / module.getModifiedItemAttr('modeMaxTargetRangePostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6011(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('Small Energy Turret'),
            'maxRange',
            1 / module.getModifiedItemAttr('modeMaxRangePostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6012(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for scanType in ('Gravimetric', 'Magnetometric', 'Radar', 'Ladar'):
            fit.ship.multiplyItemAttr(
                'scan{}Strength'.format(scanType),
                1 / (module.getModifiedItemAttr('mode{}StrengthPostDiv'.format(scanType)) or 1),
                stackingPenalties=True,
                penaltyGroup='postDiv'
            )


class Effect6014(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('signatureRadius', 1 / module.getModifiedItemAttr('modeSignatureRadiusPostDiv'),
                                  stackingPenalties=True, penaltyGroup='postDiv')


class Effect6015(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for srcResType, tgtResType in (
                ('Em', 'Em'),
                ('Explosive', 'Explosive'),
                ('Kinetic', 'Kinetic'),
                ('Thermic', 'Thermal')
        ):
            fit.ship.multiplyItemAttr(
                'armor{0}DamageResonance'.format(tgtResType),
                1 / module.getModifiedItemAttr('mode{0}ResistancePostDiv'.format(srcResType)),
                stackingPenalties=True,
                penaltyGroup='postDiv'
            )


class Effect6016(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr(
            'agility',
            1 / module.getModifiedItemAttr('modeAgilityPostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6017(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr(
            'maxVelocity',
            1 / module.getModifiedItemAttr('modeVelocityPostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6020(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'maxRange',
                                      src.getModifiedItemAttr('eliteBonusReconShip3'), skill='Recon Ships')


class Effect6021(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'maxRange',
                                      src.getModifiedItemAttr('eliteBonusReconShip3'), skill='Recon Ships')


class Effect6025(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('eliteBonusReconShip1'), skill='Recon Ships')


class Effect6027(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('eliteBonusReconShip1'),
                                      skill='Recon Ships')


class Effect6032(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Capacitor Transmitter',
                                      'power', ship.getModifiedItemAttr('powerTransferPowerNeedBonus'))


class Effect6036(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      ship.getModifiedItemAttr('shipBonusTacticalDestroyerMinmatar3'),
                                      skill='Minmatar Tactical Destroyer')


class Effect6037(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusTacticalDestroyerMinmatar1'),
                                      skill='Minmatar Tactical Destroyer')


class Effect6038(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusTacticalDestroyerMinmatar2'),
                                      skill='Minmatar Tactical Destroyer')


class Effect6039(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
            'trackingSpeed',
            1 / module.getModifiedItemAttr('modeTrackingPostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6040(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
            'signatureRadiusBonus',
            1 / module.getModifiedItemAttr('modeMWDSigPenaltyPostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6041(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for srcResType, tgtResType in (
                ('Em', 'Em'),
                ('Explosive', 'Explosive'),
                ('Kinetic', 'Kinetic'),
                ('Thermic', 'Thermal')
        ):
            fit.ship.multiplyItemAttr(
                'shield{0}DamageResonance'.format(tgtResType),
                1 / module.getModifiedItemAttr('mode{0}ResistancePostDiv'.format(srcResType)),
                stackingPenalties=True,
                penaltyGroup='postDiv'
            )


class Effect6045(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusGC3'), skill='Gallente Cruiser')


class Effect6046(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'hp', ship.getModifiedItemAttr('shipBonusGC3'), skill='Gallente Cruiser')


class Effect6047(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusGC3'), skill='Gallente Cruiser')


class Effect6048(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Sentry Drone Interfacing'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusGC3'), skill='Gallente Cruiser')


class Effect6051(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Light Drone Operation'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6052(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Medium Drone Operation'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6053(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'damageMultiplier', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6054(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'hp', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6055(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6056(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Heavy Drone Operation'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6057(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Medium Drone Operation'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6058(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Medium Drone Operation'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6059(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Medium Drone Operation'),
                                     'hp', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6060(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Light Drone Operation'),
                                     'hp', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6061(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Light Drone Operation'),
                                     'armorHP', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6062(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Light Drone Operation'),
                                     'shieldCapacity', ship.getModifiedItemAttr('shipBonusGC2'), skill='Gallente Cruiser')


class Effect6063(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.forceItemAttr('disallowAssistance', module.getModifiedItemAttr('disallowAssistance'))
        for scanType in ('Gravimetric', 'Magnetometric', 'Radar', 'Ladar'):
            fit.ship.boostItemAttr(
                'scan{}Strength'.format(scanType),
                module.getModifiedItemAttr('scan{}StrengthPercent'.format(scanType)),
                stackingPenalties=True
            )


class Effect6076(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredChargeMultiply(
            lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
            'maxVelocity',
            1 / module.getModifiedItemAttr('modeMaxRangePostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6077(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      ship.getModifiedItemAttr('shipBonusTacticalDestroyerCaldari3'),
                                      skill='Caldari Tactical Destroyer')


class Effect6083(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for damageType in ('em', 'explosive', 'kinetic', 'thermal'):
            fit.modules.filteredChargeBoost(
                lambda mod: mod.charge.requiresSkill('Rockets') or mod.charge.requiresSkill('Light Missiles'),
                '{0}Damage'.format(damageType), ship.getModifiedItemAttr('shipBonusRole7'))


class Effect6085(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'speed', ship.getModifiedItemAttr('shipBonusTacticalDestroyerCaldari1'),
                                      skill='Caldari Tactical Destroyer')


class Effect6088(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for damageType in ('em', 'explosive', 'kinetic', 'thermal'):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                            '{0}Damage'.format(damageType), ship.getModifiedItemAttr('shipBonusMC2'),
                                            skill='Minmatar Cruiser')


class Effect6093(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for damageType in ('em', 'explosive', 'kinetic', 'thermal'):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                            '{0}Damage'.format(damageType), ship.getModifiedItemAttr('shipBonusMC2'),
                                            skill='Minmatar Cruiser')


class Effect6096(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        for damageType in ('em', 'explosive', 'kinetic', 'thermal'):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                            '{0}Damage'.format(damageType), ship.getModifiedItemAttr('shipBonusMC2'),
                                            skill='Minmatar Cruiser')


class Effect6098(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'),
                                      'reloadTime', ship.getModifiedItemAttr('shipBonusTacticalDestroyerCaldari2'),
                                      skill='Caldari Tactical Destroyer')


class Effect6104(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Infomorph Psychology'),
                                         'duration', ship.getModifiedItemAttr('entosisDurationMultiplier') or 1)


class Effect6110(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', module.getModifiedItemAttr('missileVelocityBonus'),
                                        stackingPenalties=True)


class Effect6111(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'explosionDelay', module.getModifiedItemAttr('explosionDelayBonus'),
                                        stackingPenalties=True)


class Effect6112(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'aoeCloudSize', module.getModifiedItemAttr('aoeCloudSizeBonus'),
                                        stackingPenalties=True)


class Effect6113(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'aoeVelocity', module.getModifiedItemAttr('aoeVelocityBonus'),
                                        stackingPenalties=True)


class Effect6128(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('aoeCloudSizeBonus', module.getModifiedChargeAttr('aoeCloudSizeBonusBonus'))


class Effect6129(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('aoeVelocityBonus', module.getModifiedChargeAttr('aoeVelocityBonusBonus'))


class Effect6130(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('missileVelocityBonus', module.getModifiedChargeAttr('missileVelocityBonusBonus'))


class Effect6131(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('explosionDelayBonus', module.getModifiedChargeAttr('explosionDelayBonusBonus'))


class Effect6135(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, container, context):
        for srcAttr, tgtAttr in (
                ('aoeCloudSizeBonus', 'aoeCloudSize'),
                ('aoeVelocityBonus', 'aoeVelocity'),
                ('missileVelocityBonus', 'maxVelocity'),
                ('explosionDelayBonus', 'explosionDelay'),
        ):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                            tgtAttr, container.getModifiedItemAttr(srcAttr),
                                            stackingPenalties=True)


class Effect6144(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        for tgtAttr in (
                'aoeCloudSizeBonus',
                'explosionDelayBonus',
                'missileVelocityBonus',
                'maxVelocityModifier',
                'aoeVelocityBonus'
        ):
            module.boostItemAttr(tgtAttr, module.getModifiedItemAttr('overloadTrackingModuleStrengthBonus'))


class Effect6148(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'heatDamage',
                                      ship.getModifiedItemAttr('shipBonusTacticalDestroyerGallente3'),
                                      skill='Gallente Tactical Destroyer')


class Effect6149(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'speed', ship.getModifiedItemAttr('shipBonusTacticalDestroyerGallente1'),
                                      skill='Gallente Tactical Destroyer')


class Effect6150(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusTacticalDestroyerGallente2'),
                                      skill='Gallente Tactical Destroyer')


class Effect6151(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        for srcResType, tgtResType in (
                ('Em', 'em'),
                ('Explosive', 'explosive'),
                ('Kinetic', 'kinetic'),
                ('Thermic', 'thermal')
        ):
            fit.ship.multiplyItemAttr(
                '{0}DamageResonance'.format(tgtResType),
                1 / module.getModifiedItemAttr('mode{0}ResistancePostDiv'.format(srcResType))
            )


class Effect6152(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
            'maxRange',
            1 / module.getModifiedItemAttr('modeMaxRangePostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6153(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
            'capacitorNeed',
            1 / module.getModifiedItemAttr('modeMWDCapPostDiv')
        )


class Effect6154(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('High Speed Maneuvering'),
            'speedFactor',
            1 / module.getModifiedItemAttr('modeMWDVelocityPostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6155(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('Repair Systems'),
            'duration',
            1 / module.getModifiedItemAttr('modeArmorRepDurationPostDiv')
        )


class Effect6163(EffectDef):

    runtime = 'late'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.extraAttributes['speedLimit'] = src.getModifiedItemAttr('speedLimit')


class Effect6164(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr('maxVelocity', beacon.getModifiedItemAttr('maxVelocityMultiplier'), stackingPenalties=True)


class Effect6166(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Propulsion Jamming'),
                                      'speedFactorBonus', ship.getModifiedItemAttr('shipBonusAT'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Propulsion Jamming'),
                                      'speedBoostFactorBonus', ship.getModifiedItemAttr('shipBonusAT'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Propulsion Jamming'),
                                      'massBonusPercentage', ship.getModifiedItemAttr('shipBonusAT'))


class Effect6170(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Infomorph Psychology'),
                                         'entosisCPUAdd', ship.getModifiedItemAttr('entosisCPUPenalty'))


class Effect6171(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.increaseItemAttr('cpu', module.getModifiedItemAttr('entosisCPUAdd'))


class Effect6172(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'maxRange', ship.getModifiedItemAttr('roleBonusCBC'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'falloff', ship.getModifiedItemAttr('roleBonusCBC'))


class Effect6173(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'maxRange', ship.getModifiedItemAttr('roleBonusCBC'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'falloff', ship.getModifiedItemAttr('roleBonusCBC'))


class Effect6174(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'maxRange', ship.getModifiedItemAttr('roleBonusCBC'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'falloff', ship.getModifiedItemAttr('roleBonusCBC'))


class Effect6175(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'maxVelocity', skill.getModifiedItemAttr('roleBonusCBC'))


class Effect6176(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'maxVelocity', ship.getModifiedItemAttr('roleBonusCBC'))


class Effect6177(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusCBC2'),
                                      skill='Caldari Battlecruiser')


class Effect6178(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusMBC2'),
                                      skill='Minmatar Battlecruiser')


class Effect6184(EffectDef):

    runTime = 'late'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, src, context, **kwargs):
        if 'projected' in context:
            amount = src.getModifiedItemAttr('powerTransferAmount')
            duration = src.getModifiedItemAttr('duration')

            if 'effect' in kwargs:
                from eos.modifiedAttributeDict import ModifiedAttributeDict
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            fit.addDrain(src, duration, -amount, 0)


class Effect6185(EffectDef):

    runTime = 'late'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context):
        if 'projected' not in context:
            return
        bonus = module.getModifiedItemAttr('structureDamageAmount')
        duration = module.getModifiedItemAttr('duration') / 1000.0
        fit.extraAttributes.increase('hullRepair', bonus / duration)


class Effect6186(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, container, context, **kwargs):
        if 'projected' in context:
            bonus = container.getModifiedItemAttr('shieldBonus')
            duration = container.getModifiedItemAttr('duration') / 1000.0
            fit.extraAttributes.increase('shieldRepair', bonus / duration, **kwargs)


class Effect6187(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, src, context, **kwargs):
        if 'projected' in context and ((hasattr(src, 'state') and src.state >= FittingModuleState.ACTIVE) or
                                       hasattr(src, 'amountActive')):
            amount = src.getModifiedItemAttr('energyNeutralizerAmount')

            if 'effect' in kwargs:
                from eos.modifiedAttributeDict import ModifiedAttributeDict
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            time = src.getModifiedItemAttr('duration')

            fit.addDrain(src, time, amount, 0)


class Effect6188(EffectDef):

    runTime = 'late'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, container, context, **kwargs):
        if 'projected' in context:
            bonus = container.getModifiedItemAttr('armorDamageAmount')
            duration = container.getModifiedItemAttr('duration') / 1000.0
            rps = bonus / duration
            fit.extraAttributes.increase('armorRepair', rps)
            fit.extraAttributes.increase('armorRepairPreSpool', rps)
            fit.extraAttributes.increase('armorRepairFullSpool', rps)


class Effect6195(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', src.getModifiedItemAttr('eliteBonusExpedition1'),
                               skill='Expedition Frigates')
        fit.ship.boostItemAttr('shieldKineticDamageResonance', src.getModifiedItemAttr('eliteBonusExpedition1'),
                               skill='Expedition Frigates')
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', src.getModifiedItemAttr('eliteBonusExpedition1'),
                               skill='Expedition Frigates')
        fit.ship.boostItemAttr('shieldEmDamageResonance', src.getModifiedItemAttr('eliteBonusExpedition1'),
                               skill='Expedition Frigates')


class Effect6196(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting'), 'duration',
                                      src.getModifiedItemAttr('eliteBonusExpedition2'), skill='Expedition Frigates')


class Effect6197(EffectDef):

    runTime = 'late'
    type = 'active', 'projected'

    @staticmethod
    def handler(fit, src, context, **kwargs):
        amount = src.getModifiedItemAttr('powerTransferAmount')
        time = src.getModifiedItemAttr('duration')

        if 'effect' in kwargs and 'projected' in context:
            from eos.modifiedAttributeDict import ModifiedAttributeDict
            amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

        if 'projected' in context:
            fit.addDrain(src, time, amount, 0)
        elif 'module' in context:
            src.itemModifiedAttributes.force('capacitorNeed', -amount)


class Effect6201(EffectDef):

    type = 'active'


class Effect6208(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('signatureRadius', module.getModifiedItemAttr('signatureRadiusBonusPercent'),
                               stackingPenalties=True)


class Effect6214(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Leadership'), 'power',
                                      src.getModifiedItemAttr('roleBonusCD'))


class Effect6216(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, src, context, **kwargs):
        amount = 0
        if 'projected' in context:
            if (hasattr(src, 'state') and src.state >= FittingModuleState.ACTIVE) or hasattr(src, 'amountActive'):
                amount = src.getModifiedItemAttr('energyNeutralizerAmount')

                if 'effect' in kwargs:
                    from eos.modifiedAttributeDict import ModifiedAttributeDict
                    amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

                time = src.getModifiedItemAttr('duration')

                fit.addDrain(src, time, amount, 0)


class Effect6222(EffectDef):

    runTime = 'early'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context):
        if 'projected' in context:
            fit.ship.increaseItemAttr('warpScrambleStatus', module.getModifiedItemAttr('warpScrambleStrength'))
            if module.charge is not None and module.charge.ID == 47336:
                for mod in fit.modules:
                    if not mod.isEmpty and mod.item.requiresSkill('High Speed Maneuvering') and mod.state > FittingModuleState.ONLINE:
                        mod.state = FittingModuleState.ONLINE
                    if not mod.isEmpty and mod.item.requiresSkill('Micro Jump Drive Operation') and mod.state > FittingModuleState.ONLINE:
                        mod.state = FittingModuleState.ONLINE


class Effect6230(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'maxRange',
                                      src.getModifiedItemAttr('eliteBonusReconShip1'), skill='Recon Ships')


class Effect6232(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('eliteBonusReconShip2'), skill='Recon Ships')


class Effect6233(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('eliteBonusReconShip3'), skill='Recon Ships')


class Effect6234(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'maxRange',
                                      src.getModifiedItemAttr('eliteBonusReconShip1'), skill='Recon Ships')


class Effect6237(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('eliteBonusReconShip2'), skill='Recon Ships')


class Effect6238(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('eliteBonusReconShip3'), skill='Recon Ships')


class Effect6239(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting'), 'duration',
                                      src.getModifiedItemAttr('shipBonusOREfrig2'), skill='Mining Frigate')


class Effect6241(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonusAD1'), skill='Amarr Destroyer')


class Effect6242(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'maxRange',
                                      src.getModifiedItemAttr('shipBonusAD2'), skill='Amarr Destroyer')


class Effect6245(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'maxRange',
                                      src.getModifiedItemAttr('shipBonusAD2'), skill='Amarr Destroyer')


class Effect6246(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonusAD1'), skill='Amarr Destroyer')


class Effect6253(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'maxRange',
                                      src.getModifiedItemAttr('shipBonusAB'), skill='Amarr Battleship')


class Effect6256(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonusAB2'), skill='Amarr Battleship')


class Effect6257(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'maxRange',
                                      src.getModifiedItemAttr('shipBonusAB'), skill='Amarr Battleship')


class Effect6260(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonusAB2'), skill='Amarr Battleship')


class Effect6267(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'maxRange',
                                      src.getModifiedItemAttr('eliteBonusElectronicAttackShip1'),
                                      skill='Electronic Attack Ships')


class Effect6272(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('eliteBonusElectronicAttackShip3'),
                                      skill='Electronic Attack Ships')


class Effect6273(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'maxRange',
                                      src.getModifiedItemAttr('eliteBonusElectronicAttackShip1'),
                                      skill='Electronic Attack Ships')


class Effect6278(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('eliteBonusElectronicAttackShip3'),
                                      skill='Electronic Attack Ships')


class Effect6281(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'maxRange',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect6285(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonus3AF'), skill='Amarr Frigate')


class Effect6287(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'maxRange',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect6291(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonus3AF'), skill='Amarr Frigate')


class Effect6294(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'maxRange',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect6299(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonusAC3'), skill='Amarr Cruiser')


class Effect6300(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'maxRange',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect6301(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'maxRange',
                                      src.getModifiedItemAttr('shipBonusAC2'), skill='Amarr Cruiser')


class Effect6305(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonusAC3'), skill='Amarr Cruiser')


class Effect6307(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusMD1'), skill='Minmatar Destroyer')


class Effect6308(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusMD1'), skill='Minmatar Destroyer')


class Effect6309(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusMD1'), skill='Minmatar Destroyer')


class Effect6310(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'explosiveDamage', src.getModifiedItemAttr('shipBonusMD1'),
                                        skill='Minmatar Destroyer')


class Effect6315(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'buffDuration',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')


class Effect6316(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'buffDuration',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')


class Effect6317(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Micro Jump Drive Operation'), 'duration',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer2'), skill='Command Destroyers')


class Effect6318(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldEmDamageResonance', src.getModifiedItemAttr('shipBonusMD2'),
                               skill='Minmatar Destroyer')


class Effect6319(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldKineticDamageResonance', src.getModifiedItemAttr('shipBonusMD2'),
                               skill='Minmatar Destroyer')


class Effect6320(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', src.getModifiedItemAttr('shipBonusMD2'),
                               skill='Minmatar Destroyer')


class Effect6321(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusMD2'),
                               skill='Minmatar Destroyer')


class Effect6322(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr('scanGravimetricStrengthBonus', src.getModifiedChargeAttr('scanGravimetricStrengthBonusBonus'))


class Effect6323(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr('scanLadarStrengthBonus', src.getModifiedChargeAttr('scanLadarStrengthBonusBonus'))


class Effect6324(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr('scanMagnetometricStrengthBonus', src.getModifiedChargeAttr('scanMagnetometricStrengthBonusBonus'))


class Effect6325(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr('scanRadarStrengthBonus', src.getModifiedChargeAttr('scanRadarStrengthBonusBonus'))


class Effect6326(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusCD1'), skill='Caldari Destroyer')


class Effect6327(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusCD1'), skill='Caldari Destroyer')


class Effect6328(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusCD1'), skill='Caldari Destroyer')


class Effect6329(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                        'explosiveDamage', src.getModifiedItemAttr('shipBonusCD1'),
                                        skill='Caldari Destroyer')


class Effect6330(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldEmDamageResonance', src.getModifiedItemAttr('shipBonusCD2'),
                               skill='Caldari Destroyer')


class Effect6331(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', src.getModifiedItemAttr('shipBonusCD2'),
                               skill='Caldari Destroyer')


class Effect6332(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldKineticDamageResonance', src.getModifiedItemAttr('shipBonusCD2'),
                               skill='Caldari Destroyer')


class Effect6333(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusCD2'),
                               skill='Caldari Destroyer')


class Effect6334(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'buffDuration',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')


class Effect6335(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', src.getModifiedItemAttr('shipBonusAD2'),
                               skill='Amarr Destroyer')


class Effect6336(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance', src.getModifiedItemAttr('shipBonusAD2'),
                               skill='Amarr Destroyer')


class Effect6337(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', src.getModifiedItemAttr('shipBonusAD2'), skill='Amarr Destroyer')


class Effect6338(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusAD2'),
                               skill='Amarr Destroyer')


class Effect6339(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'buffDuration',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('eliteBonusCommandDestroyer1'), skill='Command Destroyers')


class Effect6340(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', src.getModifiedItemAttr('shipBonusGD2'),
                               skill='Gallente Destroyer')


class Effect6341(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', src.getModifiedItemAttr('shipBonusGD2'),
                               skill='Gallente Destroyer')


class Effect6342(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance', src.getModifiedItemAttr('shipBonusGD2'),
                               skill='Gallente Destroyer')


class Effect6343(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusGD2'),
                               skill='Gallente Destroyer')


class Effect6350(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill('Light Missiles') or mod.charge.requiresSkill('Rockets'), 'kineticDamage',
            src.getModifiedItemAttr('shipBonus3CF'), skill='Caldari Frigate')


class Effect6351(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusCC3'), skill='Caldari Cruiser')


class Effect6352(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'falloffEffectiveness',
                                      src.getModifiedItemAttr('roleBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'maxRange',
                                      src.getModifiedItemAttr('roleBonus'))


class Effect6353(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'cpu',
                                      src.getModifiedItemAttr('roleBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'capacitorNeed',
                                      src.getModifiedItemAttr('roleBonus'))


class Effect6354(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'trackingSpeedBonus',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'explosionDelayBonus',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'maxRangeBonus',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'falloffBonus',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'missileVelocityBonus',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'aoeVelocityBonus',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'aoeCloudSizeBonus',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect6355(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'capacitorNeed',
                                      src.getModifiedItemAttr('roleBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'cpu', src.getModifiedItemAttr('roleBonus'))


class Effect6356(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('roleBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'maxRange',
                                      src.getModifiedItemAttr('roleBonus'))


class Effect6357(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Navigation'), 'maxRange',
                                      src.getModifiedItemAttr('shipBonusGF2'), skill='Gallente Frigate')


class Effect6358(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Navigation'),
                                         'warpScrambleStrength', ship.getModifiedItemAttr('roleBonus'))


class Effect6359(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'), 'aoeVelocity',
                                        src.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect6360(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusMF2'), skill='Minmatar Frigate')


class Effect6361(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonus3MF'), skill='Minmatar Frigate')


class Effect6362(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web', 'maxRange',
                                      src.getModifiedItemAttr('roleBonus'))


class Effect6368(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Shield Booster', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('falloffBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Ancillary Remote Shield Booster',
                                      'falloffEffectiveness', src.getModifiedItemAttr('falloffBonus'))


class Effect6369(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect6370(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'falloffEffectiveness',
                                      src.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect6371(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'falloffEffectiveness', src.getModifiedItemAttr('shipBonusGC'),
                                      skill='Gallente Cruiser')


class Effect6372(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'falloffEffectiveness', src.getModifiedItemAttr('shipBonusAC2'),
                                      skill='Amarr Cruiser')


class Effect6373(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Armor Repairer', 'falloffEffectiveness',
                                      src.getModifiedItemAttr('falloffBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Ancillary Remote Armor Repairer',
                                      'falloffEffectiveness', src.getModifiedItemAttr('falloffBonus'))


class Effect6374(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == 'Logistic Drone', 'structureDamageAmount',
                                     src.getModifiedItemAttr('droneArmorDamageAmountBonus'))


class Effect6377(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('eliteBonusLogiFrig1'), skill='Logistics Frigates')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'duration',
                                      src.getModifiedItemAttr('eliteBonusLogiFrig1'), skill='Logistics Frigates')


class Effect6378(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'duration',
                                      src.getModifiedItemAttr('eliteBonusLogiFrig1'), skill='Logistics Frigates')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'), 'capacitorNeed',
                                      src.getModifiedItemAttr('eliteBonusLogiFrig1'), skill='Logistics Frigates')


class Effect6379(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorHP', src.getModifiedItemAttr('eliteBonusLogiFrig2'), skill='Logistics Frigates')


class Effect6380(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldCapacity', src.getModifiedItemAttr('eliteBonusLogiFrig2'), skill='Logistics Frigates')


class Effect6381(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('signatureRadius', src.getModifiedItemAttr('eliteBonusLogiFrig2'),
                               skill='Logistics Frigates')


class Effect6384(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        for tgtAttr in (
                'aoeCloudSizeBonus',
                'explosionDelayBonus',
                'missileVelocityBonus',
                'aoeVelocityBonus'
        ):
            module.boostItemAttr(tgtAttr, module.getModifiedItemAttr('overloadTrackingModuleStrengthBonus'))


class Effect6385(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemForce(lambda mod: mod.item.group.name == 'Cloaking Device',
                                      'maxVelocityModifier', src.getModifiedItemAttr('velocityPenaltyReduction'))


class Effect6386(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        level = src.level if 'skill' in context else 1
        for attr in (
                'explosionDelayBonus',
                'aoeVelocityBonus',
                'aoeCloudSizeBonus',
                'missileVelocityBonus'
        ):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'),
                                          attr, src.getModifiedItemAttr('scanSkillEwStrengthBonus') * level)


class Effect6395(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'missileVelocityBonus',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'aoeVelocityBonus',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'maxRangeBonus',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'explosionDelayBonus',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'aoeCloudSizeBonus',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'trackingSpeedBonus',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Weapon Disruption'), 'falloffBonus',
                                      src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect6396(EffectDef):

    type = 'passive', 'structure'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Structure Anti-Capital Missile', 'Structure Anti-Subcapital Missile', 'Structure Guided Bomb')
        for damageType in ('em', 'thermal', 'explosive', 'kinetic'):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                            '%sDamage' % damageType, src.getModifiedItemAttr('damageMultiplierBonus'),
                                            skill='Structure Missile Systems')


class Effect6400(EffectDef):

    type = 'passive', 'structure'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Structure Warp Scrambler', 'Structure Disruption Battery', 'Structure Stasis Webifier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'capacitorNeed', src.getModifiedItemAttr('capNeedBonus'),
                                      skill='Structure Electronic Systems')


class Effect6401(EffectDef):

    type = 'passive', 'structure'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Structure Energy Neutralizer', 'Structure Area Denial Module')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'capacitorNeed', src.getModifiedItemAttr('capNeedBonus'),
                                      skill='Structure Engineering Systems')


class Effect6402(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Structure Anti-Subcapital Missile', 'Structure Anti-Capital Missile')

        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                      'aoeVelocity', src.getModifiedItemAttr('structureRigMissileExploVeloBonus'),
                                      stackingPenalties=True)


class Effect6403(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Structure Anti-Subcapital Missile', 'Structure Anti-Capital Missile')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                      'maxVelocity', src.getModifiedItemAttr('structureRigMissileVelocityBonus'),
                                      stackingPenalties=True)


class Effect6404(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Structure Energy Neutralizer',
                                      'maxRange', src.getModifiedItemAttr('structureRigEwarOptimalBonus'),
                                      stackingPenalties=True)

        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Structure Energy Neutralizer',
                                      'falloffEffectiveness', src.getModifiedItemAttr('structureRigEwarFalloffBonus'),
                                      stackingPenalties=True)


class Effect6405(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Structure Energy Neutralizer',
                                      'capacitorNeed', src.getModifiedItemAttr('structureRigEwarCapUseBonus'),
                                      stackingPenalties=True)


class Effect6406(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Structure ECM Battery', 'Structure Disruption Battery')

        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'falloff', src.getModifiedItemAttr('structureRigEwarFalloffBonus'),
                                      stackingPenalties=True)

        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'maxRange', src.getModifiedItemAttr('structureRigEwarOptimalBonus'),
                                      stackingPenalties=True)

        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'falloffEffectiveness', src.getModifiedItemAttr('structureRigEwarFalloffBonus'),
                                      stackingPenalties=True)


class Effect6407(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Structure ECM Battery', 'Structure Disruption Battery')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'capacitorNeed', src.getModifiedItemAttr('structureRigEwarCapUseBonus'),
                                      stackingPenalties=True)


class Effect6408(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.extraAttributes.increase('maxTargetsLockedFromSkills', src.getModifiedItemAttr('structureRigMaxTargetBonus'))


class Effect6409(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('scanResolution', src.getModifiedItemAttr('structureRigScanResBonus'),
                               stackingPenalties=True)


class Effect6410(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == 'Structure Guided Bomb',
                                        'aoeCloudSize', src.getModifiedItemAttr('structureRigMissileExplosionRadiusBonus'),
                                        stackingPenalties=True)


class Effect6411(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == 'Structure Guided Bomb',
                                        'maxVelocity', src.getModifiedItemAttr('structureRigMissileVelocityBonus'),
                                        stackingPenalties=True)


class Effect6412(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Structure Area Denial Module',
                                      'empFieldRange', src.getModifiedItemAttr('structureRigPDRangeBonus'),
                                      stackingPenalties=True)


class Effect6413(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Structure Area Denial Module',
                                      'capacitorNeed', src.getModifiedItemAttr('structureRigPDCapUseBonus'),
                                      stackingPenalties=True)


class Effect6417(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == 'Structure Doomsday Weapon',
                                         'lightningWeaponDamageLossTarget',
                                         src.getModifiedItemAttr('structureRigDoomsdayDamageLossTargetBonus'))


class Effect6422(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' not in context:
            return

        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRangeBonus'),
                               stackingPenalties=True, *args, **kwargs)

        fit.ship.boostItemAttr('scanResolution', module.getModifiedItemAttr('scanResolutionBonus'),
                               stackingPenalties=True, *args, **kwargs)


class Effect6423(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' in context:
            for srcAttr, tgtAttr in (
                    ('aoeCloudSizeBonus', 'aoeCloudSize'),
                    ('aoeVelocityBonus', 'aoeVelocity'),
                    ('missileVelocityBonus', 'maxVelocity'),
                    ('explosionDelayBonus', 'explosionDelay'),
            ):
                fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                                tgtAttr, module.getModifiedItemAttr(srcAttr),
                                                stackingPenalties=True, *args, **kwargs)


class Effect6424(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' in context:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'trackingSpeed', module.getModifiedItemAttr('trackingSpeedBonus'),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'maxRange', module.getModifiedItemAttr('maxRangeBonus'),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'falloff', module.getModifiedItemAttr('falloffBonus'),
                                          stackingPenalties=True, *args, **kwargs)


class Effect6425(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, container, context, *args, **kwargs):
        if 'projected' in context:
            fit.ship.boostItemAttr('signatureRadius', container.getModifiedItemAttr('signatureRadiusBonus'),
                                   stackingPenalties=True, *args, **kwargs)


class Effect6426(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' not in context:
            return
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('speedFactor'),
                               stackingPenalties=True, *args, **kwargs)


class Effect6427(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context):
        if 'projected' not in context:
            return

        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRangeBonus'),
                               stackingPenalties=True)
        fit.ship.boostItemAttr('scanResolution', module.getModifiedItemAttr('scanResolutionBonus'),
                               stackingPenalties=True)

        for scanType in ('Gravimetric', 'Magnetometric', 'Radar', 'Ladar'):
            fit.ship.boostItemAttr(
                'scan{}Strength'.format(scanType),
                module.getModifiedItemAttr('scan{}StrengthPercent'.format(scanType)),
                stackingPenalties=True
            )


class Effect6428(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        if 'projected' in context:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'trackingSpeed', module.getModifiedItemAttr('trackingSpeedBonus'),
                                          stackingPenalties=True, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'maxRange', module.getModifiedItemAttr('maxRangeBonus'),
                                          stackingPenalties=True, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'falloff', module.getModifiedItemAttr('falloffBonus'),
                                          stackingPenalties=True, **kwargs)


class Effect6431(EffectDef):

    displayName = 'Missile Attack'
    hasCharges = True
    prefix = 'fighterAbilityMissiles'
    type = 'active'


class Effect6434(EffectDef):

    displayName = 'Energy Neutralizer'
    grouped = True
    prefix = 'fighterAbilityEnergyNeutralizer'
    type = 'active', 'projected'

    @classmethod
    def handler(cls, fit, src, context, **kwargs):
        if 'projected' in context:
            amount = src.getModifiedItemAttr('{}Amount'.format(cls.prefix)) * src.amountActive
            time = src.getModifiedItemAttr('{}Duration'.format(cls.prefix))

            if 'effect' in kwargs:
                from eos.modifiedAttributeDict import ModifiedAttributeDict
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            fit.addDrain(src, time, amount, 0)


class Effect6435(EffectDef):

    displayName = 'Stasis Webifier'
    grouped = True
    prefix = 'fighterAbilityStasisWebifier'
    type = 'active', 'projected'

    @classmethod
    def handler(cls, fit, src, context):
        if 'projected' not in context:
            return
        fit.ship.boostItemAttr('maxVelocity', src.getModifiedItemAttr('{}SpeedPenalty'.format(cls.prefix)) * src.amountActive,
                               stackingPenalties=True)


class Effect6436(EffectDef):

    displayName = 'Warp Disruption'
    grouped = True
    prefix = 'fighterAbilityWarpDisruption'
    type = 'active', 'projected'

    @classmethod
    def handler(cls, fit, src, context):
        if 'projected' not in context:
            return
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('{}PointStrength'.format(cls.prefix)) * src.amountActive)


class Effect6437(EffectDef):

    displayName = 'ECM'
    grouped = True
    prefix = 'fighterAbilityECM'
    type = 'projected', 'active'

    @classmethod
    def handler(cls, fit, module, context, **kwargs):
        if 'projected' not in context:
            return
        # jam formula: 1 - (1- (jammer str/ship str))^(# of jam mods with same str))
        strModifier = 1 - (module.getModifiedItemAttr('{}Strength{}'.format(cls.prefix, fit.scanType)) * module.amountActive) / fit.scanStrength

        if 'effect' in kwargs:
            from eos.modifiedAttributeDict import ModifiedAttributeDict
            strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

        fit.ecmProjectedStr *= strModifier


class Effect6439(EffectDef):

    displayName = 'Evasive Maneuvers'
    grouped = True
    prefix = 'fighterAbilityEvasiveManeuvers'
    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, container, context):
        container.boostItemAttr('maxVelocity',
                                container.getModifiedItemAttr('fighterAbilityEvasiveManeuversSpeedBonus'))
        container.boostItemAttr('signatureRadius',
                                container.getModifiedItemAttr('fighterAbilityEvasiveManeuversSignatureRadiusBonus'),
                                stackingPenalties=True)

        # These may not have stacking penalties, but there's nothing else that affects the attributes yet to check.
        container.multiplyItemAttr('shieldEmDamageResonance',
                                   container.getModifiedItemAttr('fighterAbilityEvasiveManeuversEmResonance'),
                                   stackingPenalties=True)
        container.multiplyItemAttr('shieldThermalDamageResonance',
                                   container.getModifiedItemAttr('fighterAbilityEvasiveManeuversThermResonance'),
                                   stackingPenalties=True)
        container.multiplyItemAttr('shieldKineticDamageResonance',
                                   container.getModifiedItemAttr('fighterAbilityEvasiveManeuversKinResonance'),
                                   stackingPenalties=True)
        container.multiplyItemAttr('shieldExplosiveDamageResonance',
                                   container.getModifiedItemAttr('fighterAbilityEvasiveManeuversExpResonance'),
                                   stackingPenalties=True)


class Effect6441(EffectDef):

    displayName = 'Microwarpdrive'
    grouped = True
    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        module.boostItemAttr('maxVelocity', module.getModifiedItemAttr('fighterAbilityMicroWarpDriveSpeedBonus'),
                             stackingPenalties=True)
        module.boostItemAttr('signatureRadius',
                             module.getModifiedItemAttr('fighterAbilityMicroWarpDriveSignatureRadiusBonus'),
                             stackingPenalties=True)


class Effect6443(EffectDef):

    type = 'active'


class Effect6447(EffectDef):

    type = 'active'


class Effect6448(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        missileGroups = ('Structure Anti-Capital Missile', 'Structure Anti-Subcapital Missile')
        for srcAttr, tgtAttr in (
                ('aoeCloudSizeBonus', 'aoeCloudSize'),
                ('aoeVelocityBonus', 'aoeVelocity'),
                ('missileVelocityBonus', 'maxVelocity'),
                ('explosionDelayBonus', 'explosionDelay'),
        ):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in missileGroups,
                                            tgtAttr, container.getModifiedItemAttr(srcAttr),
                                            stackingPenalties=True)


class Effect6449(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        missileGroups = ('Structure Anti-Capital Missile', 'Structure Anti-Subcapital Missile')

        for dmgType in ('em', 'kinetic', 'explosive', 'thermal'):
            fit.modules.filteredChargeMultiply(lambda mod: mod.charge.group.name in missileGroups,
                                               '%sDamage' % dmgType,
                                               module.getModifiedItemAttr('missileDamageMultiplierBonus'),
                                               stackingPenalties=True)

        launcherGroups = ('Structure XL Missile Launcher', 'Structure Multirole Missile Launcher')
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name in launcherGroups,
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect6465(EffectDef):

    displayName = 'Turret Attack'
    prefix = 'fighterAbilityAttackMissile'
    type = 'active'


class Effect6470(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        if 'projected' in context:
            # jam formula: 1 - (1- (jammer str/ship str))^(# of jam mods with same str))
            strModifier = 1 - module.getModifiedItemAttr('scan{0}StrengthBonus'.format(fit.scanType)) / fit.scanStrength

            if 'effect' in kwargs:
                from eos.modifiedAttributeDict import ModifiedAttributeDict
                strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            fit.ecmProjectedStr *= strModifier


class Effect6472(EffectDef):

    type = 'active'


class Effect6473(EffectDef):

    type = 'active'


class Effect6474(EffectDef):

    type = 'active'


class Effect6475(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == 'Structure Doomsday Weapon',
                                         'lightningWeaponTargetAmount',
                                         src.getModifiedItemAttr('structureRigDoomsdayTargetAmountBonus'))


class Effect6476(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' not in context:
            return
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('speedFactor'),
                               stackingPenalties=True, *args, **kwargs)


class Effect6477(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, src, context, **kwargs):
        if 'projected' in context and ((hasattr(src, 'state') and src.state >= FittingModuleState.ACTIVE) or
                                       hasattr(src, 'amountActive')):
            amount = src.getModifiedItemAttr('energyNeutralizerAmount')

            if 'effect' in kwargs:
                from eos.modifiedAttributeDict import ModifiedAttributeDict
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            time = src.getModifiedItemAttr('duration')

            fit.addDrain(src, time, amount, 0)


class Effect6478(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, container, context, *args, **kwargs):
        if 'projected' in context:
            fit.ship.boostItemAttr('signatureRadius', container.getModifiedItemAttr('signatureRadiusBonus'),
                                   stackingPenalties=True, *args, **kwargs)


class Effect6479(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' in context:
            for srcAttr, tgtAttr in (
                    ('aoeCloudSizeBonus', 'aoeCloudSize'),
                    ('aoeVelocityBonus', 'aoeVelocity'),
                    ('missileVelocityBonus', 'maxVelocity'),
                    ('explosionDelayBonus', 'explosionDelay'),
            ):
                fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                                tgtAttr, module.getModifiedItemAttr(srcAttr),
                                                stackingPenalties=True, *args, **kwargs)

            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'trackingSpeed', module.getModifiedItemAttr('trackingSpeedBonus'),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'maxRange', module.getModifiedItemAttr('maxRangeBonus'),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'falloff', module.getModifiedItemAttr('falloffBonus'),
                                          stackingPenalties=True, *args, **kwargs)


class Effect6481(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' not in context:
            return

        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRangeBonus'),
                               stackingPenalties=True, *args, **kwargs)

        fit.ship.boostItemAttr('scanResolution', module.getModifiedItemAttr('scanResolutionBonus'),
                               stackingPenalties=True, *args, **kwargs)


class Effect6482(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context):
        return


class Effect6484(EffectDef):

    runtime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, src, context):
        for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
            fit.ship.multiplyItemAttr('{}DamageResonance'.format(dmgType),
                                      src.getModifiedItemAttr('hull{}DamageResonance'.format(dmgType.title())),
                                      stackingPenalties=True, penaltyGroup='postMul')


class Effect6485(EffectDef):

    displayName = 'Bomb'
    hasCharges = True
    prefix = 'fighterAbilityLaunchBomb'
    type = 'active'


class Effect6487(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('energyWarfareResistance',
                               module.getModifiedItemAttr('energyWarfareResistanceBonus'),
                               stackingPenalties=True)


class Effect6488(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        for scanType in ('Gravimetric', 'Magnetometric', 'Radar', 'Ladar'):
            module.boostItemAttr('scan{}StrengthPercent'.format(scanType),
                                 module.getModifiedChargeAttr('sensorStrengthBonusBonus'))


class Effect6501(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Energy Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtA1'), skill='Amarr Dreadnought')


class Effect6502(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusDreadnoughtA2'),
                               skill='Amarr Dreadnought')
        fit.ship.boostItemAttr('armorEmDamageResonance', src.getModifiedItemAttr('shipBonusDreadnoughtA2'),
                               skill='Amarr Dreadnought')
        fit.ship.boostItemAttr('armorThermalDamageResonance', src.getModifiedItemAttr('shipBonusDreadnoughtA2'),
                               skill='Amarr Dreadnought')
        fit.ship.boostItemAttr('armorKineticDamageResonance', src.getModifiedItemAttr('shipBonusDreadnoughtA2'),
                               skill='Amarr Dreadnought')


class Effect6503(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Energy Turret'), 'capacitorNeed',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtA3'), skill='Amarr Dreadnought')


class Effect6504(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusDreadnoughtC1'), skill='Caldari Dreadnought')


class Effect6505(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', src.getModifiedItemAttr('shipBonusDreadnoughtC2'),
                               skill='Caldari Dreadnought')
        fit.ship.boostItemAttr('shieldKineticDamageResonance', src.getModifiedItemAttr('shipBonusDreadnoughtC2'),
                               skill='Caldari Dreadnought')
        fit.ship.boostItemAttr('shieldEmDamageResonance', src.getModifiedItemAttr('shipBonusDreadnoughtC2'),
                               skill='Caldari Dreadnought')
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusDreadnoughtC2'),
                               skill='Caldari Dreadnought')


class Effect6506(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Hybrid Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtG1'), skill='Gallente Dreadnought')


class Effect6507(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Hybrid Turret'), 'speed',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtG2'), skill='Gallente Dreadnought')


class Effect6508(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Repair Systems'), 'duration',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtG3'), skill='Gallente Dreadnought')


class Effect6509(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Projectile Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtM1'), skill='Minmatar Dreadnought')


class Effect6510(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Projectile Turret'), 'speed',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtM2'), skill='Minmatar Dreadnought')


class Effect6511(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Operation'), 'duration',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtM2'), skill='Minmatar Dreadnought')


class Effect6513(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        if 'projected' in context:
            # jam formula: 1 - (1- (jammer str/ship str))^(# of jam mods with same str))
            strModifier = 1 - module.getModifiedItemAttr('scan{0}StrengthBonus'.format(fit.scanType)) / fit.scanStrength

            if 'effect' in kwargs:
                from eos.modifiedAttributeDict import ModifiedAttributeDict
                strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            fit.ecmProjectedStr *= strModifier


class Effect6526(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capacitor Emission Systems') or
                                                  mod.item.requiresSkill('Capital Capacitor Emission Systems'),
                                      'powerTransferAmount', src.getModifiedItemAttr('shipBonusForceAuxiliaryA1'),
                                      skill='Amarr Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems') or
                                                  mod.item.requiresSkill('Capital Remote Armor Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('shipBonusForceAuxiliaryA1'),
                                      skill='Amarr Carrier')


class Effect6527(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', src.getModifiedItemAttr('shipBonusForceAuxiliaryA2'),
                               skill='Amarr Carrier')
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusForceAuxiliaryA2'),
                               skill='Amarr Carrier')
        fit.ship.boostItemAttr('armorEmDamageResonance', src.getModifiedItemAttr('shipBonusForceAuxiliaryA2'),
                               skill='Amarr Carrier')
        fit.ship.boostItemAttr('armorThermalDamageResonance', src.getModifiedItemAttr('shipBonusForceAuxiliaryA2'),
                               skill='Amarr Carrier')


class Effect6533(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command') or
                                                  mod.item.requiresSkill('Information Command'),
                                      'warfareBuff4Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryA4'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command') or
                                                  mod.item.requiresSkill('Information Command'),
                                      'warfareBuff3Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryA4'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command') or
                                                  mod.item.requiresSkill('Information Command'),
                                      'warfareBuff1Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryA4'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command') or
                                                  mod.item.requiresSkill('Information Command'),
                                      'buffDuration', src.getModifiedItemAttr('shipBonusForceAuxiliaryA4'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command') or
                                                  mod.item.requiresSkill('Information Command'),
                                      'warfareBuff2Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryA4'), skill='Amarr Carrier')


class Effect6534(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryM4'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryM4'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryM4'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusForceAuxiliaryM4'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryM4'), skill='Minmatar Carrier')


class Effect6535(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryG4'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryG4'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusForceAuxiliaryG4'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryG4'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryG4'), skill='Gallente Carrier')


class Effect6536(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryC4'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryC4'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryC4'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusForceAuxiliaryC4'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusForceAuxiliaryC4'), skill='Caldari Carrier')


class Effect6537(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Leadership'), 'cpu',
                                      src.getModifiedItemAttr('shipBonusRole1'))


class Effect6545(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        if src.getModifiedItemAttr('shipBonusForceAuxiliaryC1') is None:
            return  # See GH Issue 1321

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capacitor Emission Systems') or
                                                  mod.item.requiresSkill('Capital Capacitor Emission Systems'),
                                      'powerTransferAmount', src.getModifiedItemAttr('shipBonusForceAuxiliaryC1'),
                                      skill='Caldari Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems') or
                                                  mod.item.requiresSkill('Capital Shield Emission Systems'),
                                      'shieldBonus', src.getModifiedItemAttr('shipBonusForceAuxiliaryC1'),
                                      skill='Caldari Carrier')


class Effect6546(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldEmDamageResonance', src.getModifiedItemAttr('shipBonusForceAuxiliaryC2'),
                               skill='Caldari Carrier')
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusForceAuxiliaryC2'),
                               skill='Caldari Carrier')
        fit.ship.boostItemAttr('shieldKineticDamageResonance', src.getModifiedItemAttr('shipBonusForceAuxiliaryC2'),
                               skill='Caldari Carrier')
        fit.ship.boostItemAttr('shieldThermalDamageResonance', src.getModifiedItemAttr('shipBonusForceAuxiliaryC2'),
                               skill='Caldari Carrier')


class Effect6548(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems') or
                                                  mod.item.requiresSkill('Capital Shield Emission Systems'),
                                      'duration', src.getModifiedItemAttr('shipBonusForceAuxiliaryG1'),
                                      skill='Gallente Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems') or
                                                  mod.item.requiresSkill('Capital Remote Armor Repair Systems'),
                                      'duration', src.getModifiedItemAttr('shipBonusForceAuxiliaryG1'),
                                      skill='Gallente Carrier')


class Effect6549(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'), 'armorDamageAmount',
                                      src.getModifiedItemAttr('shipBonusForceAuxiliaryG2'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Repair Systems'), 'armorDamageAmount',
                                      src.getModifiedItemAttr('shipBonusForceAuxiliaryG2'), skill='Gallente Carrier')


class Effect6551(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems') or
                                                  mod.item.requiresSkill('Capital Shield Emission Systems'),
                                      'duration', src.getModifiedItemAttr('shipBonusForceAuxiliaryM1'),
                                      skill='Minmatar Carrier')

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems') or
                                                  mod.item.requiresSkill('Capital Remote Armor Repair Systems'),
                                      'duration', src.getModifiedItemAttr('shipBonusForceAuxiliaryM1'),
                                      skill='Minmatar Carrier')


class Effect6552(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Operation'), 'shieldBonus',
                                      src.getModifiedItemAttr('shipBonusForceAuxiliaryM2'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'), 'shieldBonus',
                                      src.getModifiedItemAttr('shipBonusForceAuxiliaryM2'), skill='Minmatar Carrier')


class Effect6555(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'maxVelocity',
                                       src.getModifiedItemAttr('speedFactor'), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'maxVelocity',
                                     src.getModifiedItemAttr('speedFactor'), stackingPenalties=True)


class Effect6556(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('droneDamageBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('droneDamageBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('droneDamageBonus'), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'damageMultiplier',
                                     src.getModifiedItemAttr('droneDamageBonus'), stackingPenalties=True)


class Effect6557(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretRangeFalloff', src.getModifiedItemAttr('falloffBonus'),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesExplosionVelocity',
                                       src.getModifiedItemAttr('aoeVelocityBonus'), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'trackingSpeed',
                                     src.getModifiedItemAttr('trackingSpeedBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileExplosionRadius',
                                       src.getModifiedItemAttr('aoeCloudSizeBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretTrackingSpeed',
                                       src.getModifiedItemAttr('trackingSpeedBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesExplosionRadius',
                                       src.getModifiedItemAttr('aoeCloudSizeBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'fighterAbilityMissilesRange',
                                       src.getModifiedItemAttr('maxRangeBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileRangeOptimal', src.getModifiedItemAttr('maxRangeBonus'),
                                       stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'falloff',
                                     src.getModifiedItemAttr('falloffBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileExplosionVelocity',
                                       src.getModifiedItemAttr('aoeVelocityBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileRangeFalloff', src.getModifiedItemAttr('falloffBonus'),
                                       stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'maxRange',
                                     src.getModifiedItemAttr('maxRangeBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretRangeOptimal', src.getModifiedItemAttr('maxRangeBonus'),
                                       stackingPenalties=True)


class Effect6558(EffectDef):

    type = 'overheat'

    @staticmethod
    def handler(fit, module, context):
        overloadBonus = module.getModifiedItemAttr('overloadTrackingModuleStrengthBonus')
        module.boostItemAttr('maxRangeBonus', overloadBonus)
        module.boostItemAttr('falloffBonus', overloadBonus)
        module.boostItemAttr('trackingSpeedBonus', overloadBonus)
        module.boostItemAttr('aoeCloudSizeBonus', overloadBonus)
        module.boostItemAttr('aoeVelocityBonus', overloadBonus)


class Effect6559(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileExplosionRadius',
                                       src.getModifiedItemAttr('aoeCloudSizeBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileRangeOptimal', src.getModifiedItemAttr('maxRangeBonus'),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretRangeFalloff', src.getModifiedItemAttr('falloffBonus'),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesExplosionRadius',
                                       src.getModifiedItemAttr('aoeCloudSizeBonus'), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'falloff',
                                     src.getModifiedItemAttr('falloffBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileRangeFalloff', src.getModifiedItemAttr('falloffBonus'),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretTrackingSpeed',
                                       src.getModifiedItemAttr('trackingSpeedBonus'), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'maxRange',
                                     src.getModifiedItemAttr('maxRangeBonus'), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'trackingSpeed',
                                     src.getModifiedItemAttr('trackingSpeedBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretRangeOptimal', src.getModifiedItemAttr('maxRangeBonus'),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesExplosionVelocity',
                                       src.getModifiedItemAttr('aoeVelocityBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileExplosionVelocity',
                                       src.getModifiedItemAttr('aoeVelocityBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'fighterAbilityMissilesRange',
                                       src.getModifiedItemAttr('maxRangeBonus'), stackingPenalties=True)


class Effect6560(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('damageMultiplierBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('damageMultiplierBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('damageMultiplierBonus') * lvl)


class Effect6561(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Light Fighters'), 'maxVelocity',
                                       src.getModifiedItemAttr('maxVelocityBonus') * lvl)


class Effect6562(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Support Fighters'), 'shieldCapacity',
                                       src.getModifiedItemAttr('shieldBonus') * lvl)


class Effect6563(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Heavy Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('damageMultiplierBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Heavy Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('damageMultiplierBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Heavy Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('damageMultiplierBonus') * lvl)


class Effect6565(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context):

        for attr in [
            'structureRigDoomsdayDamageLossTargetBonus',
            'structureRigScanResBonus',
            'structureRigPDRangeBonus',
            'structureRigPDCapUseBonus',
            'structureRigMissileExploVeloBonus',
            'structureRigMissileVelocityBonus',
            'structureRigEwarOptimalBonus',
            'structureRigEwarFalloffBonus',
            'structureRigEwarCapUseBonus',
            'structureRigMissileExplosionRadiusBonus'
        ]:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Jury Rigging'),
                                      attr, src.getModifiedItemAttr('structureRoleBonus'))


class Effect6566(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Fighters'), 'shieldCapacity',
                                       src.getModifiedItemAttr('fighterBonusShieldCapacityPercent'))
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Fighters'), 'maxVelocity',
                                       src.getModifiedItemAttr('fighterBonusVelocityPercent'), stackingPenalties=True, penaltyGroup='postMul')
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDuration',
                                       src.getModifiedItemAttr('fighterBonusROFPercent'), stackingPenalties=True, penaltyGroup='postMul')
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Fighters'), 'fighterAbilityAttackTurretDuration',
                                       src.getModifiedItemAttr('fighterBonusROFPercent'), stackingPenalties=True, penaltyGroup='postMul')
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Fighters'), 'fighterAbilityMissilesDuration',
                                       src.getModifiedItemAttr('fighterBonusROFPercent'), stackingPenalties=True, penaltyGroup='postMul')
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Fighters'), 'shieldRechargeRate',
                                       src.getModifiedItemAttr('fighterBonusShieldRechargePercent'))


class Effect6567(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('scanResolution', src.getModifiedItemAttr('scanResolutionBonus'), stackingPenalties=True)

        for scanType in ('Magnetometric', 'Ladar', 'Gravimetric', 'Radar'):
            attr = 'scan{}Strength'.format(scanType)
            bonus = src.getModifiedItemAttr('scan{}StrengthPercent'.format(scanType))
            fit.ship.boostItemAttr(attr, bonus, stackingPenalties=True)
            fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), attr, bonus,
                                           stackingPenalties=True)

        # EW cap need increase
        groups = [
            'Burst Jammer',
            'Weapon Disruptor',
            'ECM',
            'Stasis Grappler',
            'Sensor Dampener',
            'Target Painter']

        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups or
                                                  mod.item.requiresSkill('Propulsion Jamming'),
                                      'capacitorNeed', src.getModifiedItemAttr('ewCapacitorNeedBonus'))


class Effect6570(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.ship.boostItemAttr('fighterCapacity', src.getModifiedItemAttr('skillBonusFighterHangarSize') * lvl)


class Effect6571(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Autocannon Specialization'),
                                      'damageMultiplier', src.getModifiedItemAttr('damageMultiplierBonus') * lvl)


class Effect6572(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Artillery Specialization'),
                                      'damageMultiplier', src.getModifiedItemAttr('damageMultiplierBonus') * lvl)


class Effect6573(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Blaster Specialization'),
                                      'damageMultiplier', src.getModifiedItemAttr('damageMultiplierBonus') * lvl)


class Effect6574(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Railgun Specialization'),
                                      'damageMultiplier', src.getModifiedItemAttr('damageMultiplierBonus') * lvl)


class Effect6575(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Pulse Laser Specialization'),
                                      'damageMultiplier', src.getModifiedItemAttr('damageMultiplierBonus') * lvl)


class Effect6576(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Beam Laser Specialization'),
                                      'damageMultiplier', src.getModifiedItemAttr('damageMultiplierBonus') * lvl)


class Effect6577(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('XL Cruise Missile Specialization'), 'speed',
                                      src.getModifiedItemAttr('rofBonus') * lvl)


class Effect6578(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('XL Torpedo Specialization'), 'speed',
                                      src.getModifiedItemAttr('rofBonus') * lvl)


class Effect6580(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Drone Operation'), 'structureDamageAmount',
                                     src.getModifiedItemAttr('shipBonusRole2'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Drone Operation'), 'armorDamageAmount',
                                     src.getModifiedItemAttr('shipBonusRole2'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Drone Operation'), 'shieldBonus',
                                     src.getModifiedItemAttr('shipBonusRole2'))


class Effect6581(EffectDef):

    runTime = 'early'
    type = 'active'

    @staticmethod
    def handler(fit, src, context):
        # Remote effect bonuses (duration / amount / range / fallout)
        for skill, amtAttr, stack in (
                ('Capital Remote Armor Repair Systems', 'armorDamageAmount', True),
                ('Capital Shield Emission Systems', 'shieldBonus', True),
                ('Capital Capacitor Emission Systems', 'powerTransferAmount', False),
                ('Capital Remote Hull Repair Systems', 'structureDamageAmount', False)):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), 'duration',
                                          src.getModifiedItemAttr('siegeRemoteLogisticsDurationBonus'))
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), amtAttr,
                                          src.getModifiedItemAttr('siegeRemoteLogisticsAmountBonus'),
                                          stackingPenalties=stack)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), 'maxRange',
                                          src.getModifiedItemAttr('siegeRemoteLogisticsRangeBonus'), stackingPenalties=True)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), 'falloffEffectiveness',
                                          src.getModifiedItemAttr('siegeRemoteLogisticsRangeBonus'), stackingPenalties=True)

        # Local armor/shield rep effects (duration / amoutn)
        for skill, amtAttr in (
                ('Capital Shield Operation', 'shieldBonus'),
                ('Capital Repair Systems', 'armorDamageAmount')):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), 'duration',
                                          src.getModifiedItemAttr('siegeLocalLogisticsDurationBonus'))
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), amtAttr,
                                          src.getModifiedItemAttr('siegeLocalLogisticsAmountBonus'))

        # Speed bonus
        fit.ship.boostItemAttr('maxVelocity', src.getModifiedItemAttr('speedFactor'), stackingPenalties=True)

        # Scan resolution multiplier
        fit.ship.multiplyItemAttr('scanResolution', src.getModifiedItemAttr('scanResolutionMultiplier'),
                                  stackingPenalties=True)

        # Mass multiplier
        fit.ship.multiplyItemAttr('mass', src.getModifiedItemAttr('siegeMassMultiplier'), stackingPenalties=True)

        # Max locked targets
        fit.ship.increaseItemAttr('maxLockedTargets', src.getModifiedItemAttr('maxLockedTargetsBonus'))

        # EW cap need increase
        groups = [
            'Burst Jammer',
            'Weapon Disruptor',
            'ECM',
            'Stasis Grappler',
            'Sensor Dampener',
            'Target Painter']

        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups or
                                                  mod.item.requiresSkill('Propulsion Jamming'),
                                      'capacitorNeed', src.getModifiedItemAttr('ewCapacitorNeedBonus'))

        # todo: test for April 2016 release
        # Block EWAR & projected effects
        fit.ship.forceItemAttr('disallowOffensiveModifiers', src.getModifiedItemAttr('disallowOffensiveModifiers'))
        fit.ship.forceItemAttr('disallowAssistance', src.getModifiedItemAttr('disallowAssistance'))

        # new in April 2016 release
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'damageMultiplier',
                                     src.getModifiedItemAttr('droneDamageBonus'), stackingPenalties=True)

        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('siegeModeWarpStatus'))
        fit.ship.boostItemAttr('sensorDampenerResistance', src.getModifiedItemAttr('sensorDampenerResistanceBonus'))
        fit.ship.boostItemAttr('remoteAssistanceImpedance', src.getModifiedItemAttr('remoteAssistanceImpedanceBonus'))
        fit.ship.boostItemAttr('remoteRepairImpedance', src.getModifiedItemAttr('remoteRepairImpedanceBonus'))

        fit.ship.forceItemAttr('disallowTethering', src.getModifiedItemAttr('disallowTethering'))
        fit.ship.forceItemAttr('disallowDocking', src.getModifiedItemAttr('disallowDocking'))


class Effect6582(EffectDef):

    runTime = 'early'
    type = 'active'

    @staticmethod
    def handler(fit, src, context):
        # Turrets
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Energy Turret') or
                                                  mod.item.requiresSkill('Capital Hybrid Turret') or
                                                  mod.item.requiresSkill('Capital Projectile Turret'),
                                      'damageMultiplier', src.getModifiedItemAttr('siegeTurretDamageBonus'))

        # Missiles
        for type in ('kinetic', 'thermal', 'explosive', 'em'):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes') or
                                                        mod.charge.requiresSkill('XL Cruise Missiles') or
                                                        mod.charge.requiresSkill('Torpedoes'),
                                            '%sDamage' % type, src.getModifiedItemAttr('siegeMissileDamageBonus'))

        # Reppers
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Operation') or
                                                  mod.item.requiresSkill('Capital Repair Systems'),
                                      'duration', src.getModifiedItemAttr('siegeLocalLogisticsDurationBonus'))

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Operation'),
                                      'shieldBonus', src.getModifiedItemAttr('siegeLocalLogisticsAmountBonus'),
                                      stackingPenalties=True)

        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('siegeLocalLogisticsAmountBonus'),
                                      stackingPenalties=True)

        # Speed penalty
        fit.ship.boostItemAttr('maxVelocity', src.getModifiedItemAttr('speedFactor'))

        # Mass
        fit.ship.multiplyItemAttr('mass', src.getModifiedItemAttr('siegeMassMultiplier'),
                                  stackingPenalties=True, penaltyGroup='postMul')

        # @ todo: test for April 2016 release
        # Block Hostile EWAR and friendly effects
        fit.ship.forceItemAttr('disallowOffensiveModifiers', src.getModifiedItemAttr('disallowOffensiveModifiers'))
        fit.ship.forceItemAttr('disallowAssistance', src.getModifiedItemAttr('disallowAssistance'))

        # new in April 2016 release
        # missile ROF bonus
        for group in ('Missile Launcher XL Torpedo', 'Missile Launcher Rapid Torpedo', 'Missile Launcher XL Cruise'):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == group, 'speed',
                                          src.getModifiedItemAttr('siegeLauncherROFBonus'))

        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'maxVelocity',
                                        src.getModifiedItemAttr('siegeTorpedoVelocityBonus'), stackingPenalties=True)

        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('siegeModeWarpStatus'))
        fit.ship.boostItemAttr('remoteRepairImpedance', src.getModifiedItemAttr('remoteRepairImpedanceBonus'))
        fit.ship.boostItemAttr('sensorDampenerResistance', src.getModifiedItemAttr('sensorDampenerResistanceBonus'))
        fit.ship.boostItemAttr('remoteAssistanceImpedance', src.getModifiedItemAttr('remoteAssistanceImpedanceBonus'))
        fit.ship.boostItemAttr('weaponDisruptionResistance', src.getModifiedItemAttr('weaponDisruptionResistanceBonus'))

        fit.ship.forceItemAttr('disallowDocking', src.getModifiedItemAttr('disallowDocking'))
        fit.ship.forceItemAttr('disallowTethering', src.getModifiedItemAttr('disallowTethering'))


class Effect6591(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('shipBonusSupercarrierA3'),
                                  skill='Amarr Carrier')


class Effect6592(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('shipBonusSupercarrierC3'),
                                  skill='Caldari Carrier')


class Effect6593(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('shipBonusSupercarrierG3'),
                                  skill='Gallente Carrier')


class Effect6594(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('shipBonusSupercarrierM3'),
                                  skill='Minmatar Carrier')


class Effect6595(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusCarrierA4'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusCarrierA4'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusCarrierA4'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusCarrierA4'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusCarrierA4'), skill='Amarr Carrier')


class Effect6596(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusCarrierC4'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusCarrierC4'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusCarrierC4'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusCarrierC4'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusCarrierC4'), skill='Caldari Carrier')


class Effect6597(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusCarrierG4'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusCarrierG4'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusCarrierG4'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusCarrierG4'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusCarrierG4'), skill='Gallente Carrier')


class Effect6598(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusCarrierM4'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusCarrierM4'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusCarrierM4'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusCarrierM4'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusCarrierM4'), skill='Minmatar Carrier')


class Effect6599(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', src.getModifiedItemAttr('shipBonusCarrierA1'),
                               skill='Amarr Carrier')
        fit.ship.boostItemAttr('armorEmDamageResonance', src.getModifiedItemAttr('shipBonusCarrierA1'),
                               skill='Amarr Carrier')
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusCarrierA1'),
                               skill='Amarr Carrier')
        fit.ship.boostItemAttr('armorThermalDamageResonance', src.getModifiedItemAttr('shipBonusCarrierA1'),
                               skill='Amarr Carrier')


class Effect6600(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', src.getModifiedItemAttr('shipBonusCarrierC1'),
                               skill='Caldari Carrier')
        fit.ship.boostItemAttr('shieldEmDamageResonance', src.getModifiedItemAttr('shipBonusCarrierC1'),
                               skill='Caldari Carrier')
        fit.ship.boostItemAttr('shieldKineticDamageResonance', src.getModifiedItemAttr('shipBonusCarrierC1'),
                               skill='Caldari Carrier')
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusCarrierC1'),
                               skill='Caldari Carrier')


class Effect6601(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusCarrierG1'), skill='Gallente Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusCarrierG1'), skill='Gallente Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusCarrierG1'), skill='Gallente Carrier')


class Effect6602(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusCarrierM1'), skill='Minmatar Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusCarrierM1'), skill='Minmatar Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusCarrierM1'), skill='Minmatar Carrier')


class Effect6603(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierA1'), skill='Amarr Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierA1'), skill='Amarr Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierA1'), skill='Amarr Carrier')


class Effect6604(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierC1'), skill='Caldari Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierC1'), skill='Caldari Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierC1'), skill='Caldari Carrier')


class Effect6605(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierG1'), skill='Gallente Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierG1'), skill='Gallente Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierG1'), skill='Gallente Carrier')


class Effect6606(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierM1'), skill='Minmatar Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierM1'), skill='Minmatar Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusSupercarrierM1'), skill='Minmatar Carrier')


class Effect6607(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusSupercarrierA5'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusSupercarrierA5'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusSupercarrierA5'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusSupercarrierA5'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Armored Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusSupercarrierA5'), skill='Amarr Carrier')


class Effect6608(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusSupercarrierC5'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusSupercarrierC5'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusSupercarrierC5'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusSupercarrierC5'), skill='Caldari Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Shield Command') or mod.item.requiresSkill('Information Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusSupercarrierC5'), skill='Caldari Carrier')


class Effect6609(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusSupercarrierG5'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusSupercarrierG5'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusSupercarrierG5'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusSupercarrierG5'), skill='Gallente Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Armored Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusSupercarrierG5'), skill='Gallente Carrier')


class Effect6610(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff4Value', src.getModifiedItemAttr('shipBonusSupercarrierM5'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff1Value', src.getModifiedItemAttr('shipBonusSupercarrierM5'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff3Value', src.getModifiedItemAttr('shipBonusSupercarrierM5'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'buffDuration', src.getModifiedItemAttr('shipBonusSupercarrierM5'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill('Skirmish Command') or mod.item.requiresSkill('Shield Command'),
            'warfareBuff2Value', src.getModifiedItemAttr('shipBonusSupercarrierM5'), skill='Minmatar Carrier')


class Effect6611(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'), 'speedFactor',
                                      src.getModifiedItemAttr('shipBonusSupercarrierC2'), skill='Caldari Carrier')


class Effect6612(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesExplosionVelocity',
                                       src.getModifiedItemAttr('shipBonusSupercarrierA2'), skill='Amarr Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileExplosionVelocity',
                                       src.getModifiedItemAttr('shipBonusSupercarrierA2'), skill='Amarr Carrier')


class Effect6613(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Leadership'), 'maxGroupActive',
                                         src.getModifiedItemAttr('shipBonusRole1'))


class Effect6614(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'), 'armorHPBonusAdd',
                                      src.getModifiedItemAttr('shipBonusRole2'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Upgrades'), 'capacityBonus',
                                      src.getModifiedItemAttr('shipBonusRole2'))


class Effect6615(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation'),
                                      'durationWeaponDisruptionBurstProjector',
                                      src.getModifiedItemAttr('shipBonusSupercarrierA4'), skill='Amarr Carrier')


class Effect6616(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation'),
                                      'durationECMJammerBurstProjector', src.getModifiedItemAttr('shipBonusSupercarrierC4'),
                                      skill='Caldari Carrier')


class Effect6617(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation'),
                                      'durationSensorDampeningBurstProjector',
                                      src.getModifiedItemAttr('shipBonusSupercarrierG4'), skill='Gallente Carrier')


class Effect6618(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation'),
                                      'durationTargetIlluminationBurstProjector',
                                      src.getModifiedItemAttr('shipBonusSupercarrierM4'), skill='Minmatar Carrier')


class Effect6619(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Leadership'), 'maxGroupActive',
                                         src.getModifiedItemAttr('shipBonusRole1'))


class Effect6620(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Missile Launcher Operation'), 'reloadTime',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtC3'), skill='Caldari Dreadnought')


class Effect6621(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusSupercarrierA2'),
                               skill='Amarr Carrier')
        fit.ship.boostItemAttr('armorEmDamageResonance', src.getModifiedItemAttr('shipBonusSupercarrierA2'),
                               skill='Amarr Carrier')
        fit.ship.boostItemAttr('armorThermalDamageResonance', src.getModifiedItemAttr('shipBonusSupercarrierA2'),
                               skill='Amarr Carrier')
        fit.ship.boostItemAttr('armorKineticDamageResonance', src.getModifiedItemAttr('shipBonusSupercarrierA2'),
                               skill='Amarr Carrier')


class Effect6622(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldThermalDamageResonance', src.getModifiedItemAttr('shipBonusSupercarrierC2'),
                               skill='Caldari Carrier')
        fit.ship.boostItemAttr('shieldEmDamageResonance', src.getModifiedItemAttr('shipBonusSupercarrierC2'),
                               skill='Caldari Carrier')
        fit.ship.boostItemAttr('shieldKineticDamageResonance', src.getModifiedItemAttr('shipBonusSupercarrierC2'),
                               skill='Caldari Carrier')
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusSupercarrierC2'),
                               skill='Caldari Carrier')


class Effect6623(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'shieldCapacity',
                                       src.getModifiedItemAttr('shipBonusSupercarrierG2'), skill='Gallente Carrier')


class Effect6624(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'maxVelocity',
                                       src.getModifiedItemAttr('shipBonusSupercarrierM2'), skill='Minmatar Carrier')


class Effect6625(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Support Fighters'), 'fighterSquadronOrbitRange',
                                       src.getModifiedItemAttr('shipBonusCarrierA2'), skill='Amarr Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Support Fighters'),
                                       'fighterAbilityEnergyNeutralizerOptimalRange',
                                       src.getModifiedItemAttr('shipBonusCarrierA2'), skill='Amarr Carrier')


class Effect6626(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Support Fighters'), 'fighterSquadronOrbitRange',
                                       src.getModifiedItemAttr('shipBonusCarrierC2'), skill='Caldari Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Support Fighters'),
                                       'fighterAbilityECMRangeOptimal', src.getModifiedItemAttr('shipBonusCarrierC2'),
                                       skill='Caldari Carrier')


class Effect6627(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Support Fighters'), 'fighterSquadronOrbitRange',
                                       src.getModifiedItemAttr('shipBonusCarrierG2'), skill='Gallente Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Support Fighters'),
                                       'fighterAbilityWarpDisruptionRange', src.getModifiedItemAttr('shipBonusCarrierG2'),
                                       skill='Gallente Carrier')


class Effect6628(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Support Fighters'), 'fighterSquadronOrbitRange',
                                       src.getModifiedItemAttr('shipBonusCarrierM2'), skill='Minmatar Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Support Fighters'),
                                       'fighterAbilityStasisWebifierOptimalRange',
                                       src.getModifiedItemAttr('shipBonusCarrierM2'), skill='Minmatar Carrier')


class Effect6629(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        src.boostItemAttr('emDamageResistanceBonus', src.getModifiedChargeAttr('emDamageResistanceBonusBonus'))
        src.boostItemAttr('explosiveDamageResistanceBonus',
                          src.getModifiedChargeAttr('explosiveDamageResistanceBonusBonus'))
        src.boostItemAttr('kineticDamageResistanceBonus', src.getModifiedChargeAttr('kineticDamageResistanceBonusBonus'))
        src.boostItemAttr('thermalDamageResistanceBonus', src.getModifiedChargeAttr('thermalDamageResistanceBonusBonus'))


class Effect6634(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Energy Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusTitanA1'), skill='Amarr Titan')


class Effect6635(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC1'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC1'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC1'), skill='Caldari Titan')


class Effect6636(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Hybrid Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusTitanG1'), skill='Gallente Titan')


class Effect6637(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Projectile Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusTitanM1'), skill='Minmatar Titan')


class Effect6638(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher XL Cruise', 'speed',
                                      src.getModifiedItemAttr('shipBonusTitanC2'), skill='Caldari Titan')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Rapid Torpedo', 'speed',
                                      src.getModifiedItemAttr('shipBonusTitanC2'), skill='Caldari Titan')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher XL Torpedo', 'speed',
                                      src.getModifiedItemAttr('shipBonusTitanC2'), skill='Caldari Titan')


class Effect6639(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesExplosionRadius',
                                       src.getModifiedItemAttr('shipBonusSupercarrierA4'), skill='Amarr Carrier')
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileExplosionRadius',
                                       src.getModifiedItemAttr('shipBonusSupercarrierA4'), skill='Amarr Carrier')


class Effect6640(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Leadership'), 'maxGroupActive',
                                         src.getModifiedItemAttr('shipBonusRole1'))


class Effect6641(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'), 'armorHPBonusAdd',
                                      src.getModifiedItemAttr('shipBonusRole2'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Upgrades'), 'capacityBonus',
                                      src.getModifiedItemAttr('shipBonusRole2'))


class Effect6642(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Doomsday Operation'), 'duration',
                                      src.getModifiedItemAttr('rofBonus') * lvl)


class Effect6647(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('shipBonusTitanA3'), skill='Amarr Titan')


class Effect6648(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('shipBonusTitanC3'), skill='Caldari Titan')


class Effect6649(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('shipBonusTitanG3'), skill='Gallente Titan')


class Effect6650(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('shipBonusTitanM3'), skill='Minmatar Titan')


class Effect6651(EffectDef):

    runTime = 'late'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        if 'projected' not in context:
            return

        if module.charge and module.charge.name == 'Nanite Repair Paste':
            multiplier = 3
        else:
            multiplier = 1

        amount = module.getModifiedItemAttr('armorDamageAmount') * multiplier
        speed = module.getModifiedItemAttr('duration') / 1000.0
        rps = amount / speed
        fit.extraAttributes.increase('armorRepair', rps)
        fit.extraAttributes.increase('armorRepairPreSpool', rps)
        fit.extraAttributes.increase('armorRepairFullSpool', rps)


class Effect6652(EffectDef):

    runTime = 'late'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        if 'projected' not in context:
            return
        amount = module.getModifiedItemAttr('shieldBonus')
        speed = module.getModifiedItemAttr('duration') / 1000.0
        fit.extraAttributes.increase('shieldRepair', amount / speed, **kwargs)


class Effect6653(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Energy Turret'), 'capacitorNeed',
                                      src.getModifiedItemAttr('shipBonusTitanA2'), skill='Amarr Titan')


class Effect6654(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Hybrid Turret'), 'speed',
                                      src.getModifiedItemAttr('shipBonusTitanG2'), skill='Gallente Titan')


class Effect6655(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Projectile Turret'), 'speed',
                                      src.getModifiedItemAttr('shipBonusTitanM2'), skill='Minmatar Titan')


class Effect6656(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'maxVelocity',
                                        src.getModifiedItemAttr('shipBonusRole3'))


class Effect6657(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC5'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC5'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC5'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC5'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC5'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Cruise Missiles'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC5'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC5'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC5'), skill='Caldari Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('XL Torpedoes'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusTitanC5'), skill='Caldari Titan')


class Effect6658(EffectDef):

    runTime = 'early'
    type = 'active'

    @staticmethod
    def handler(fit, src, context):
        # Resistances
        for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
            for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
                bonus = '%s%sDamageResonance' % (attrPrefix, damageType)
                bonus = '%s%s' % (bonus[0].lower(), bonus[1:])
                booster = '%s%sDamageResonance' % (layer, damageType)
                penalize = False if layer == 'hull' else True
                fit.ship.multiplyItemAttr(bonus, src.getModifiedItemAttr(booster),
                                          stackingPenalties=penalize, penaltyGroup='preMul')

        # Turrets
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret') or
                                                  mod.item.requiresSkill('Large Hybrid Turret') or
                                                  mod.item.requiresSkill('Large Projectile Turret'),
                                      'maxRange', src.getModifiedItemAttr('maxRangeBonus'),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret') or
                                                  mod.item.requiresSkill('Large Hybrid Turret') or
                                                  mod.item.requiresSkill('Large Projectile Turret'),
                                      'falloff', src.getModifiedItemAttr('falloffBonus'),
                                      stackingPenalties=True)

        # Missiles
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes') or
                                                    mod.charge.requiresSkill('Cruise Missiles') or
                                                    mod.charge.requiresSkill('Heavy Missiles'),
                                        'maxVelocity', src.getModifiedItemAttr('missileVelocityBonus'))

        # Tanking
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('armorDamageAmountBonus'),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', src.getModifiedItemAttr('shieldBoostMultiplier'),
                                      stackingPenalties=True)

        # Speed penalty
        fit.ship.boostItemAttr('maxVelocity', src.getModifiedItemAttr('speedFactor'))

        # @todo: test these for April 2016 release
        # Max locked targets
        fit.ship.forceItemAttr('maxLockedTargets', src.getModifiedItemAttr('maxLockedTargets'))

        # Block Hostile ewar
        fit.ship.forceItemAttr('disallowOffensiveModifiers', src.getModifiedItemAttr('disallowOffensiveModifiers'))

        # new with April 2016 release
        for scanType in ('Magnetometric', 'Ladar', 'Gravimetric', 'Radar'):
            fit.ship.boostItemAttr('scan{}Strength'.format(scanType),
                                   src.getModifiedItemAttr('scan{}StrengthPercent'.format(scanType)),
                                   stackingPenalties=True)

        fit.ship.boostItemAttr('remoteRepairImpedance', src.getModifiedItemAttr('remoteRepairImpedanceBonus'))
        fit.ship.boostItemAttr('remoteAssistanceImpedance', src.getModifiedItemAttr('remoteAssistanceImpedanceBonus'))
        fit.ship.boostItemAttr('sensorDampenerResistance', src.getModifiedItemAttr('sensorDampenerResistanceBonus'))
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Micro Jump Drive Operation'),
                                         'activationBlocked', src.getModifiedItemAttr('activationBlockedStrenght'))
        fit.ship.boostItemAttr('targetPainterResistance', src.getModifiedItemAttr('targetPainterResistanceBonus'))
        fit.ship.boostItemAttr('weaponDisruptionResistance', src.getModifiedItemAttr('weaponDisruptionResistanceBonus'))
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('siegeModeWarpStatus'))

        fit.ship.forceItemAttr('disallowDocking', src.getModifiedItemAttr('disallowDocking'))
        fit.ship.forceItemAttr('disallowTethering', src.getModifiedItemAttr('disallowTethering'))


class Effect6661(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'maxVelocity',
                                       src.getModifiedItemAttr('shipBonusCarrierM3'), skill='Minmatar Carrier')


class Effect6662(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'shieldCapacity',
                                       src.getModifiedItemAttr('shipBonusCarrierG3'), skill='Gallente Carrier')


class Effect6663(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'damageMultiplier',
                                     src.getModifiedItemAttr('damageMultiplierBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('damageMultiplierBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('damageMultiplierBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('damageMultiplierBonus') * lvl)
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Mining Drone Operation'), 'miningDroneAmountPercent',
                                     src.getModifiedItemAttr('miningAmountBonus') * lvl)


class Effect6664(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'maxRange',
                                     src.getModifiedItemAttr('rangeSkillBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'fighterAbilityMissilesRange',
                                       src.getModifiedItemAttr('rangeSkillBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretRangeOptimal',
                                       src.getModifiedItemAttr('rangeSkillBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileRangeOptimal',
                                       src.getModifiedItemAttr('rangeSkillBonus') * lvl)


class Effect6665(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'hp',
                                     src.getModifiedItemAttr('hullHpBonus') * lvl)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'armorHP',
                                     src.getModifiedItemAttr('armorHpBonus') * lvl)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'shieldCapacity',
                                     src.getModifiedItemAttr('shieldCapacityBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'shieldCapacity',
                                       src.getModifiedItemAttr('shieldCapacityBonus') * lvl)


class Effect6667(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'maxVelocity',
                                     src.getModifiedItemAttr('maxVelocityBonus') * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'maxVelocity',
                                       src.getModifiedItemAttr('maxVelocityBonus') * lvl)


class Effect6669(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'armorHP',
                                     src.getModifiedItemAttr('hullHpBonus'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'hp',
                                     src.getModifiedItemAttr('hullHpBonus'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'shieldCapacity',
                                     src.getModifiedItemAttr('hullHpBonus'))
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'shieldCapacity',
                                       src.getModifiedItemAttr('hullHpBonus'))
        fit.ship.boostItemAttr('cpuOutput', src.getModifiedItemAttr('drawback'))


class Effect6670(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'maxRange',
                                     src.getModifiedItemAttr('rangeSkillBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'fighterAbilityMissilesRange',
                                       src.getModifiedItemAttr('rangeSkillBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackTurretRangeOptimal', src.getModifiedItemAttr('rangeSkillBonus'),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'),
                                       'fighterAbilityAttackMissileRangeOptimal',
                                       src.getModifiedItemAttr('rangeSkillBonus'), stackingPenalties=True)
        fit.ship.boostItemAttr('cpuOutput', src.getModifiedItemAttr('drawback'))


class Effect6671(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'maxVelocity',
                                     src.getModifiedItemAttr('droneMaxVelocityBonus'), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'maxVelocity',
                                       src.getModifiedItemAttr('droneMaxVelocityBonus'), stackingPenalties=True)
        fit.ship.boostItemAttr('cpuOutput', src.getModifiedItemAttr('drawback'))


class Effect6672(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        secModifier = module.getModifiedItemAttr('securityModifier')
        module.multiplyItemAttr('structureRigDoomsdayDamageLossTargetBonus', secModifier)
        module.multiplyItemAttr('structureRigScanResBonus', secModifier)
        module.multiplyItemAttr('structureRigPDRangeBonus', secModifier)
        module.multiplyItemAttr('structureRigPDCapUseBonus', secModifier)
        module.multiplyItemAttr('structureRigMissileExploVeloBonus', secModifier)
        module.multiplyItemAttr('structureRigMissileVelocityBonus', secModifier)
        module.multiplyItemAttr('structureRigEwarOptimalBonus', secModifier)
        module.multiplyItemAttr('structureRigEwarFalloffBonus', secModifier)
        module.multiplyItemAttr('structureRigEwarCapUseBonus', secModifier)
        module.multiplyItemAttr('structureRigMissileExplosionRadiusBonus', secModifier)
        module.multiplyItemAttr('structureRigMaxTargetRangeBonus', secModifier)


class Effect6679(EffectDef):

    type = 'passive', 'structure'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Structure Doomsday Weapon',
                                      'duration', src.getModifiedItemAttr('durationBonus'),
                                      skill='Structure Doomsday Operation')


class Effect6681(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Leadership'), 'maxGroupActive',
                                         src.getModifiedItemAttr('shipBonusRole3'))


class Effect6682(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' not in context:
            return
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('speedFactor'),
                               stackingPenalties=True, *args, **kwargs)


class Effect6683(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, container, context, *args, **kwargs):
        if 'projected' in context:
            fit.ship.boostItemAttr('signatureRadius', container.getModifiedItemAttr('signatureRadiusBonus'),
                                   stackingPenalties=True, *args, **kwargs)


class Effect6684(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' not in context:
            return

        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRangeBonus'),
                               stackingPenalties=True, *args, **kwargs)

        fit.ship.boostItemAttr('scanResolution', module.getModifiedItemAttr('scanResolutionBonus'),
                               stackingPenalties=True, *args, **kwargs)


class Effect6685(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context):
        if 'projected' in context:
            # jam formula: 1 - (1- (jammer str/ship str))^(# of jam mods with same str))
            strModifier = 1 - module.getModifiedItemAttr('scan{0}StrengthBonus'.format(fit.scanType)) / fit.scanStrength

            fit.ecmProjectedStr *= strModifier


class Effect6686(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' in context:
            for srcAttr, tgtAttr in (
                    ('aoeCloudSizeBonus', 'aoeCloudSize'),
                    ('aoeVelocityBonus', 'aoeVelocity'),
                    ('missileVelocityBonus', 'maxVelocity'),
                    ('explosionDelayBonus', 'explosionDelay'),
            ):
                fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                                tgtAttr, module.getModifiedItemAttr(srcAttr),
                                                stackingPenalties=True, *args, **kwargs)

            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'trackingSpeed', module.getModifiedItemAttr('trackingSpeedBonus'),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'maxRange', module.getModifiedItemAttr('maxRangeBonus'),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'falloff', module.getModifiedItemAttr('falloffBonus'),
                                          stackingPenalties=True, *args, **kwargs)


class Effect6687(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, container, context):
        if 'projected' in context:
            bonus = container.getModifiedItemAttr('armorDamageAmount')
            duration = container.getModifiedItemAttr('duration') / 1000.0
            rps = bonus / duration
            fit.extraAttributes.increase('armorRepair', rps)
            fit.extraAttributes.increase('armorRepairPreSpool', rps)
            fit.extraAttributes.increase('armorRepairFullSpool', rps)


class Effect6688(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, container, context):
        if 'projected' in context:
            bonus = container.getModifiedItemAttr('shieldBonus')
            duration = container.getModifiedItemAttr('duration') / 1000.0
            fit.extraAttributes.increase('shieldRepair', bonus / duration)


class Effect6689(EffectDef):

    runTime = 'late'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context):
        if 'projected' not in context:
            return
        bonus = module.getModifiedItemAttr('structureDamageAmount')
        duration = module.getModifiedItemAttr('duration') / 1000.0
        fit.extraAttributes.increase('hullRepair', bonus / duration)


class Effect6690(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' not in context:
            return
        fit.ship.boostItemAttr('maxVelocity', module.getModifiedItemAttr('speedFactor'),
                               stackingPenalties=True, *args, **kwargs)


class Effect6691(EffectDef):

    type = 'active', 'projected'

    @staticmethod
    def handler(fit, src, context, **kwargs):
        if 'projected' in context and ((hasattr(src, 'state') and src.state >= FittingModuleState.ACTIVE) or
                                       hasattr(src, 'amountActive')):
            amount = src.getModifiedItemAttr('energyNeutralizerAmount')
            time = src.getModifiedItemAttr('energyNeutralizerDuration')

            if 'effect' in kwargs:
                from eos.modifiedAttributeDict import ModifiedAttributeDict
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            fit.addDrain(src, time, amount, 0)


class Effect6692(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, container, context, *args, **kwargs):
        if 'projected' in context:
            fit.ship.boostItemAttr('signatureRadius', container.getModifiedItemAttr('signatureRadiusBonus'),
                                   stackingPenalties=True, *args, **kwargs)


class Effect6693(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' not in context:
            return

        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('maxTargetRangeBonus'),
                               stackingPenalties=True, *args, **kwargs)

        fit.ship.boostItemAttr('scanResolution', module.getModifiedItemAttr('scanResolutionBonus'),
                               stackingPenalties=True, *args, **kwargs)


class Effect6694(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, *args, **kwargs):
        if 'projected' in context:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'trackingSpeed', module.getModifiedItemAttr('trackingSpeedBonus'),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'maxRange', module.getModifiedItemAttr('maxRangeBonus'),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Gunnery'),
                                          'falloff', module.getModifiedItemAttr('falloffBonus'),
                                          stackingPenalties=True, *args, **kwargs)


class Effect6695(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        if 'projected' in context:
            # jam formula: 1 - (1- (jammer str/ship str))^(# of jam mods with same str))
            strModifier = 1 - module.getModifiedItemAttr('scan{0}StrengthBonus'.format(fit.scanType)) / fit.scanStrength

            if 'effect' in kwargs:
                from eos.modifiedAttributeDict import ModifiedAttributeDict
                strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            fit.ecmProjectedStr *= strModifier


class Effect6697(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Armor', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Resource Processing', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)


class Effect6698(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Navigation', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Anchor', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)


class Effect6699(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Drones', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)


class Effect6700(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Electronic Systems', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Scanning', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Targeting', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)


class Effect6701(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Projectile Weapon', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)


class Effect6702(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Energy Weapon', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)


class Effect6703(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Hybrid Weapon', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)


class Effect6704(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Launcher', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)


class Effect6705(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Rig Shield', 'drawback',
                                      src.getModifiedItemAttr('rigDrawbackBonus') * lvl)


class Effect6706(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Cybernetics'),
                                                 'armorRepairBonus', src.getModifiedItemAttr('implantSetSerpentis2'))


class Effect6708(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('armorRepairBonus'))


class Effect6709(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Hybrid Turret'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusRole1'))


class Effect6710(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web', 'speedFactor',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtM1'), skill='Minmatar Dreadnought')


class Effect6711(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Hybrid Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusRole3'))


class Effect6712(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web', 'speedFactor',
                                      src.getModifiedItemAttr('shipBonusTitanM1'), skill='Minmatar Titan')


class Effect6713(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Burst Projector Operation'), 'speedFactor',
                                      src.getModifiedItemAttr('shipBonusSupercarrierM1'), skill='Minmatar Carrier')


class Effect6714(EffectDef):

    type = 'projected', 'active'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        if 'projected' in context:
            # jam formula: 1 - (1- (jammer str/ship str))^(# of jam mods with same str))
            strModifier = 1 - module.getModifiedItemAttr('scan{0}StrengthBonus'.format(fit.scanType)) / fit.scanStrength

            if 'effect' in kwargs:
                from eos.modifiedAttributeDict import ModifiedAttributeDict
                strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            fit.ecmProjectedStr *= strModifier


class Effect6717(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining'), 'capacitorNeed',
                                      src.getModifiedItemAttr('miningDurationRoleBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining'), 'duration',
                                      src.getModifiedItemAttr('miningDurationRoleBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting'), 'duration',
                                      src.getModifiedItemAttr('miningDurationRoleBonus'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting'), 'capacitorNeed',
                                      src.getModifiedItemAttr('miningDurationRoleBonus'))


class Effect6720(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'shieldBonus',
                                     src.getModifiedItemAttr('shipBonusMC'), skill='Minmatar Cruiser')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'structureDamageAmount',
                                     src.getModifiedItemAttr('shipBonusMC'), skill='Minmatar Cruiser')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'armorDamageAmount',
                                     src.getModifiedItemAttr('shipBonusMC'), skill='Minmatar Cruiser')


class Effect6721(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'falloffEffectiveness',
                                      src.getModifiedItemAttr('eliteBonusLogistics1'),
                                      skill='Logistics Cruisers')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'maxRange',
                                      src.getModifiedItemAttr('eliteBonusLogistics1'),
                                      skill='Logistics Cruisers')


class Effect6722(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'falloffEffectiveness',
                                      src.getModifiedItemAttr('roleBonusRepairRange'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'maxRange',
                                      src.getModifiedItemAttr('roleBonusRepairRange'))


class Effect6723(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Cloaking'), 'cpu',
                                      src.getModifiedItemAttr('shipBonusMC2'), skill='Minmatar Cruiser')


class Effect6724(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'duration',
                                      src.getModifiedItemAttr('eliteBonusLogistics3'), skill='Logistics Cruisers')


class Effect6725(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'), 'falloff',
                                      src.getModifiedItemAttr('shipBonus2AF'), skill='Amarr Frigate')


class Effect6726(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Cloaking'), 'cpu',
                                      src.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect6727(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Energy Nosferatu', 'Energy Neutralizer'),
                                      'falloffEffectiveness', src.getModifiedItemAttr('eliteBonusCovertOps1'),
                                      stackingPenalties=True, skill='Covert Ops')


class Effect6730(EffectDef):

    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('mass', module.getModifiedItemAttr('massAddition'))
        speedBoost = module.getModifiedItemAttr('speedFactor')
        mass = fit.ship.getModifiedItemAttr('mass')
        thrust = module.getModifiedItemAttr('speedBoostFactor')
        fit.ship.boostItemAttr('maxVelocity', speedBoost * thrust / mass)
        fit.ship.boostItemAttr('signatureRadius', module.getModifiedItemAttr('signatureRadiusBonus'),
                               stackingPenalties=True)


class Effect6731(EffectDef):

    runTime = 'late'
    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('mass', module.getModifiedItemAttr('massAddition'))
        speedBoost = module.getModifiedItemAttr('speedFactor')
        mass = fit.ship.getModifiedItemAttr('mass')
        thrust = module.getModifiedItemAttr('speedBoostFactor')
        fit.ship.boostItemAttr('maxVelocity', speedBoost * thrust / mass)


class Effect6732(EffectDef):

    type = 'active', 'gang'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr('warfareBuff{}ID'.format(x)):
                value = module.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = module.getModifiedChargeAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])


class Effect6733(EffectDef):

    type = 'active', 'gang'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr('warfareBuff{}ID'.format(x)):
                value = module.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = module.getModifiedChargeAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])


class Effect6734(EffectDef):

    type = 'active', 'gang'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr('warfareBuff{}ID'.format(x)):
                value = module.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = module.getModifiedChargeAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])


class Effect6735(EffectDef):

    type = 'active', 'gang'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr('warfareBuff{}ID'.format(x)):
                value = module.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = module.getModifiedChargeAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])


class Effect6736(EffectDef):

    type = 'active', 'gang'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr('warfareBuff{}ID'.format(x)):
                value = module.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = module.getModifiedChargeAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])


class Effect6737(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        for x in range(1, 4):
            value = module.getModifiedChargeAttr('warfareBuff{}Multiplier'.format(x))
            module.multiplyItemAttr('warfareBuff{}Value'.format(x), value)


class Effect6753(EffectDef):

    type = 'active', 'gang'

    @staticmethod
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedItemAttr('warfareBuff{}ID'.format(x)):
                value = module.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = module.getModifiedItemAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])


class Effect6762(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Drone Specialization'), 'miningAmount',
                                     src.getModifiedItemAttr('miningAmountBonus') * lvl)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Drone Specialization'), 'maxVelocity',
                                     src.getModifiedItemAttr('maxVelocityBonus') * lvl)


class Effect6763(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level if 'skill' in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting Drone Operation'), 'duration', src.getModifiedItemAttr('rofBonus') * lvl)


class Effect6764(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting Drone Specialization'), 'duration',
                                     src.getModifiedItemAttr('rofBonus') * lvl)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting Drone Specialization'),
                                     'maxVelocity', src.getModifiedItemAttr('maxVelocityBonus') * lvl)


class Effect6765(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Spatial Phenomena Generation'), 'buffDuration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)


class Effect6766(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Leadership'), 'maxGroupActive',
                                         src.getModifiedItemAttr('maxGangModules'))
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Leadership'), 'maxGroupOnline',
                                         src.getModifiedItemAttr('maxGangModules'))


class Effect6769(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Leadership'), 'maxRange',
                                      src.getModifiedItemAttr('areaOfEffectBonus') * src.level)


class Effect6770(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'buffDuration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)


class Effect6771(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'buffDuration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)


class Effect6772(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'buffDuration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)


class Effect6773(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'buffDuration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)


class Effect6774(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'buffDuration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)


class Effect6776(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff1Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff2Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff4Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Armored Command'), 'warfareBuff3Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)


class Effect6777(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff3Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff1Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff2Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff4Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)


class Effect6778(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff2Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff1Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff3Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Information Command'), 'warfareBuff4Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)


class Effect6779(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff3Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff4Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff1Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Skirmish Command'), 'warfareBuff2Multiplier',
                                        src.getModifiedItemAttr('commandStrengthBonus') * lvl)


class Effect6780(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff4Value', src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff3Value', src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff2Value', src.getModifiedItemAttr('commandStrengthBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff1Value', src.getModifiedItemAttr('commandStrengthBonus') * lvl)


class Effect6782(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Leadership'),
                                      'reloadTime',
                                      src.getModifiedItemAttr('reloadTimeBonus') * lvl)


class Effect6783(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Leadership'), 'maxRange',
                                      src.getModifiedItemAttr('roleBonusCommandBurstAoERange'))


class Effect6786(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff4Multiplier',
                                      src.getModifiedItemAttr('shipBonusICS3'), skill='Industrial Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff1Multiplier',
                                      src.getModifiedItemAttr('shipBonusICS3'), skill='Industrial Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff2Multiplier',
                                      src.getModifiedItemAttr('shipBonusICS3'), skill='Industrial Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff3Multiplier',
                                      src.getModifiedItemAttr('shipBonusICS3'), skill='Industrial Command Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'buffDuration',
                                      src.getModifiedItemAttr('shipBonusICS3'), skill='Industrial Command Ships')


class Effect6787(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier',
                                     src.getModifiedItemAttr('shipBonusICS4'),
                                     skill='Industrial Command Ships'
                                     )

        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'shieldCapacity',
                                     src.getModifiedItemAttr('shipBonusICS4'),
                                     skill='Industrial Command Ships'
                                     )

        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'armorHP',
                                     src.getModifiedItemAttr('shipBonusICS4'),
                                     skill='Industrial Command Ships'
                                     )

        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'hp',
                                     src.getModifiedItemAttr('shipBonusICS4'),
                                     skill='Industrial Command Ships'
                                     )

        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Mining Drone Operation'),
                                     'miningAmount',
                                     src.getModifiedItemAttr('shipBonusICS4'),
                                     skill='Industrial Command Ships'
                                     )


class Effect6788(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Ice Harvesting Drone Operation'),
                                     'duration',
                                     src.getModifiedItemAttr('shipBonusICS5'),
                                     skill='Industrial Command Ships'
                                     )


class Effect6789(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier',
                                     src.getModifiedItemAttr('industrialBonusDroneDamage'))


class Effect6790(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Ice Harvesting Drone Operation'), 'duration',
                                     src.getModifiedItemAttr('roleBonusDroneIceHarvestingSpeed'))


class Effect6792(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'damageMultiplier',
                                     src.getModifiedItemAttr('shipBonusORECapital4'),
                                     skill='Capital Industrial Ships'
                                     )

        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'shieldCapacity',
                                     src.getModifiedItemAttr('shipBonusORECapital4'),
                                     skill='Capital Industrial Ships'
                                     )

        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'armorHP',
                                     src.getModifiedItemAttr('shipBonusORECapital4'),
                                     skill='Capital Industrial Ships'
                                     )

        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Drones'),
                                     'hp',
                                     src.getModifiedItemAttr('shipBonusORECapital4'),
                                     skill='Capital Industrial Ships'
                                     )

        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Mining Drone Operation'),
                                     'miningAmount',
                                     src.getModifiedItemAttr('shipBonusORECapital4'),
                                     skill='Capital Industrial Ships'
                                     )


class Effect6793(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('shipBonusORECapital2'), skill='Capital Industrial Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('shipBonusORECapital2'), skill='Capital Industrial Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('shipBonusORECapital2'), skill='Capital Industrial Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('shipBonusORECapital2'), skill='Capital Industrial Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Mining Foreman'), 'buffDuration',
                                      src.getModifiedItemAttr('shipBonusORECapital2'), skill='Capital Industrial Ships')


class Effect6794(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff4Value',
                                      src.getModifiedItemAttr('shipBonusORECapital3'), skill='Capital Industrial Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'buffDuration',
                                      src.getModifiedItemAttr('shipBonusORECapital3'), skill='Capital Industrial Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff1Value',
                                      src.getModifiedItemAttr('shipBonusORECapital3'), skill='Capital Industrial Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff3Value',
                                      src.getModifiedItemAttr('shipBonusORECapital3'), skill='Capital Industrial Ships')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Command'), 'warfareBuff2Value',
                                      src.getModifiedItemAttr('shipBonusORECapital3'), skill='Capital Industrial Ships')


class Effect6795(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill('Ice Harvesting Drone Operation'),
                                     'duration',
                                     src.getModifiedItemAttr('shipBonusORECapital5'),
                                     skill='Capital Industrial Ships'
                                     )


class Effect6796(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('Small Hybrid Turret'),
            'damageMultiplier',
            1 / module.getModifiedItemAttr('modeDamageBonusPostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6797(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
            'damageMultiplier',
            1 / module.getModifiedItemAttr('modeDamageBonusPostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6798(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('Small Energy Turret'),
            'damageMultiplier',
            1 / module.getModifiedItemAttr('modeDamageBonusPostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6799(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        types = ('thermal', 'em', 'explosive', 'kinetic')
        for type in types:
            fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill('Rockets') or mod.charge.requiresSkill('Light Missiles'),
                                               '{}Damage'.format(type),
                                               1 / module.getModifiedItemAttr('modeDamageBonusPostDiv'),
                                               stackingPenalties=True,
                                               penaltyGroup='postDiv')


class Effect6800(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('weaponDisruptionResistance', 1 / module.getModifiedItemAttr('modeEwarResistancePostDiv'))
        fit.ship.multiplyItemAttr('sensorDampenerResistance', 1 / module.getModifiedItemAttr('modeEwarResistancePostDiv'))


class Effect6801(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill('High Speed Maneuvering') or mod.item.requiresSkill('Afterburner'),
            'speedFactor',
            1 / module.getModifiedItemAttr('modeVelocityPostDiv'),
            stackingPenalties=True,
            penaltyGroup='postDiv'
        )


class Effect6807(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Invulnerability Core Operation'), 'buffDuration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Invulnerability Core Operation'), 'duration',
                                      src.getModifiedItemAttr('durationBonus') * lvl)


class Effect6844(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Defender Missiles'),
                                        'maxVelocity', skill.getModifiedItemAttr('missileVelocityBonus') * skill.level)


class Effect6845(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Defender Missiles'),
                                      'moduleReactivationDelay', ship.getModifiedItemAttr('shipBonusRole1'))


class Effect6851(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Energy Turret'), 'damageMultiplier', src.getModifiedItemAttr('shipBonusRole3'))


class Effect6852(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'maxRange', src.getModifiedItemAttr('shipBonusTitanM1'), skill='Minmatar Titan')


class Effect6853(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'powerTransferAmount', src.getModifiedItemAttr('shipBonusTitanA1'), skill='Amarr Titan')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer',
                                      'energyNeutralizerAmount', src.getModifiedItemAttr('shipBonusTitanA1'), skill='Amarr Titan')


class Effect6855(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'powerTransferAmount', src.getModifiedItemAttr('shipBonusDreadnoughtA1'), skill='Amarr Dreadnought')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer',
                                      'energyNeutralizerAmount', src.getModifiedItemAttr('shipBonusDreadnoughtA1'), skill='Amarr Dreadnought')


class Effect6856(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'maxRange', src.getModifiedItemAttr('shipBonusDreadnoughtM1'), skill='Minmatar Dreadnought')


class Effect6857(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'maxRange', src.getModifiedItemAttr('shipBonusForceAuxiliaryA1'), skill='Amarr Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'falloffEffectiveness', src.getModifiedItemAttr('shipBonusForceAuxiliaryA1'), skill='Amarr Carrier')


class Effect6858(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu',
                                      'powerTransferAmount', src.getModifiedItemAttr('shipBonusForceAuxiliaryA1'), skill='Amarr Carrier')


class Effect6859(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Nosferatu', 'cpu', src.getModifiedItemAttr('shipBonusRole4'))


class Effect6860(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'power',
                                      src.getModifiedItemAttr('shipBonusRole5'))


class Effect6861(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Remote Armor Repair Systems'), 'power', src.getModifiedItemAttr('shipBonusRole5'))


class Effect6862(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'duration', src.getModifiedItemAttr('shipBonusForceAuxiliaryM1'), skill='Minmatar Carrier')


class Effect6865(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', src.getModifiedItemAttr('eliteBonusCovertOps1'), skill='Covert Ops')


class Effect6866(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Rockets'),
                                        'explosionDelay', src.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Light Missiles'),
                                        'explosionDelay', src.getModifiedItemAttr('shipBonusCF'), skill='Caldari Frigate')


class Effect6867(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Projectile Turret'),
                                      'speed', src.getModifiedItemAttr('shipBonusMF'), skill='Minmatar Frigate')


class Effect6871(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):

        # Get pilot sec status bonus directly here, instead of going through the intermediary effects
        # via https://forums.eveonline.com/default.aspx?g=posts&t=515826
        try:
            bonus = max(0, min(50.0, (src.parent.character.secStatus * 10)))
        except:
            bonus = None

        if bonus is not None:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', bonus, stackingPenalties=True)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'shieldBonus', bonus, stackingPenalties=True)


class Effect6872(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web', 'maxRange', src.getModifiedItemAttr('eliteBonusReconShip1'), skill='Recon Ships')


class Effect6873(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', src.getModifiedItemAttr('eliteBonusReconShip3'), skill='Recon Ships')


class Effect6874(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'explosionDelay', src.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'explosionDelay', src.getModifiedItemAttr('shipBonusCC2'), skill='Caldari Cruiser')


class Effect6877(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', src.getModifiedItemAttr('eliteBonusBlackOps1'), stackingPenalties=True, skill='Black Ops')


class Effect6878(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler', 'maxRange',
                                      src.getModifiedItemAttr('eliteBonusBlackOps4'), stackingPenalties=True, skill='Black Ops')


class Effect6879(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web', 'maxRange',
                                      src.getModifiedItemAttr('eliteBonusBlackOps3'), stackingPenalties=True, skill='Black Ops')


class Effect6880(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Cruise', 'speed',
                                      src.getModifiedItemAttr('shipBonus2CB'), skill='Caldari Battleship')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Torpedo', 'speed',
                                      src.getModifiedItemAttr('shipBonus2CB'), skill='Caldari Battleship')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Rapid Heavy', 'speed',
                                      src.getModifiedItemAttr('shipBonus2CB'), skill='Caldari Battleship')


class Effect6881(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'explosionDelay',
                                        src.getModifiedItemAttr('shipBonusCB'), skill='Caldari Battleship')
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'), 'explosionDelay',
                                        src.getModifiedItemAttr('shipBonusCB'), skill='Caldari Battleship')


class Effect6883(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('shipBonusForceAuxiliaryM2'), skill='Minmatar Carrier')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Repair Systems'),
                                      'armorDamageAmount', src.getModifiedItemAttr('shipBonusForceAuxiliaryM2'), skill='Minmatar Carrier')


class Effect6894(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Energy Nosferatu', 'Energy Neutralizer'),
        'cpu', src.getModifiedItemAttr('subsystemEnergyNeutFittingReduction'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Energy Nosferatu', 'Energy Neutralizer'),
                                      'power', src.getModifiedItemAttr('subsystemEnergyNeutFittingReduction'))


class Effect6895(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'cpu', src.getModifiedItemAttr('subsystemMETFittingReduction'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Energy Turret'),
                                      'power', src.getModifiedItemAttr('subsystemMETFittingReduction'))


class Effect6896(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'cpu', src.getModifiedItemAttr('subsystemMHTFittingReduction'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'),
                                      'power', src.getModifiedItemAttr('subsystemMHTFittingReduction'))


class Effect6897(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'power', src.getModifiedItemAttr('subsystemMPTFittingReduction'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Projectile Turret'),
                                      'cpu', src.getModifiedItemAttr('subsystemMPTFittingReduction'))


class Effect6898(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems') and
                                                  mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                      'cpu', src.getModifiedItemAttr('subsystemMRARFittingReduction'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems') and
                                                  mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                      'power', src.getModifiedItemAttr('subsystemMRARFittingReduction'))


class Effect6899(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems') and
                                                  mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                      'cpu', src.getModifiedItemAttr('subsystemMRSBFittingReduction'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems') and
                                                  mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                      'power', src.getModifiedItemAttr('subsystemMRSBFittingReduction'))


class Effect6900(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Missile Launcher Heavy', 'Missile Launcher Rapid Light', 'Missile Launcher Heavy Assault')
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'cpu', src.getModifiedItemAttr('subsystemMMissileFittingReduction'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      'power', src.getModifiedItemAttr('subsystemMMissileFittingReduction'))


class Effect6908(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'moduleRepairRate',
                                      ship.getModifiedItemAttr('shipBonusStrategicCruiserCaldari2'),
                                      skill='Caldari Strategic Cruiser')


class Effect6909(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'moduleRepairRate',
                                      ship.getModifiedItemAttr('shipBonusStrategicCruiserAmarr2'),
                                      skill='Amarr Strategic Cruiser')


class Effect6910(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'moduleRepairRate',
                                      ship.getModifiedItemAttr('shipBonusStrategicCruiserGallente2'),
                                      skill='Gallente Strategic Cruiser')


class Effect6911(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, 'moduleRepairRate',
                                      ship.getModifiedItemAttr('shipBonusStrategicCruiserMinmatar2'),
                                      skill='Minmatar Strategic Cruiser')


class Effect6920(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.increaseItemAttr('hp', module.getModifiedItemAttr('structureHPBonusAdd') or 0)


class Effect6921(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'),
                                        'baseSensorStrength', src.getModifiedItemAttr('subsystemBonusAmarrDefensive2'),
                                        skill='Amarr Defensive Systems')


class Effect6923(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles') or mod.charge.requiresSkill('Heavy Assault Missiles'),
                                      'maxVelocity', container.getModifiedItemAttr('subsystemBonusMinmatarOffensive'),
                                      skill='Minmatar Offensive Systems')


class Effect6924(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'),
                                      'aoeVelocity', container.getModifiedItemAttr('subsystemBonusMinmatarOffensive3'),
                                      skill='Minmatar Offensive Systems')


class Effect6925(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'maxVelocity', src.getModifiedItemAttr('subsystemBonusGallenteOffensive2'),
                                     skill='Gallente Offensive Systems')
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'),
                                     'trackingSpeed', src.getModifiedItemAttr('subsystemBonusGallenteOffensive2'),
                                     skill='Gallente Offensive Systems')


class Effect6926(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpCapacitorNeed', src.getModifiedItemAttr('subsystemBonusAmarrPropulsion'), skill='Amarr Propulsion Systems')


class Effect6927(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpCapacitorNeed', src.getModifiedItemAttr('subsystemBonusMinmatarPropulsion'),
                               skill='Minmatar Propulsion Systems')


class Effect6928(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner') or mod.item.requiresSkill('High Speed Maneuvering'),
                                      'overloadSpeedFactorBonus', src.getModifiedItemAttr('subsystemBonusCaldariPropulsion2'),
                                      skill='Caldari Propulsion Systems')


class Effect6929(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner') or mod.item.requiresSkill('High Speed Maneuvering'),
                                      'overloadSpeedFactorBonus', src.getModifiedItemAttr('subsystemBonusGallentePropulsion2'),
                                      skill='Gallente Propulsion Systems')


class Effect6930(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('energyWarfareResistance', src.getModifiedItemAttr('subsystemBonusAmarrCore2'), skill='Amarr Core Systems')


class Effect6931(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('energyWarfareResistance', src.getModifiedItemAttr('subsystemBonusMinmatarCore2'),
                               skill='Minmatar Core Systems')


class Effect6932(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('energyWarfareResistance', src.getModifiedItemAttr('subsystemBonusGallenteCore2'),
                               skill='Gallente Core Systems')


class Effect6933(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('energyWarfareResistance', src.getModifiedItemAttr('subsystemBonusCaldariCore2'),
                               skill='Caldari Core Systems')


class Effect6934(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('maxLockedTargets', src.getModifiedItemAttr('maxLockedTargetsBonus'))


class Effect6935(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Energy Nosferatu', 'Energy Neutralizer'), 'overloadSelfDurationBonus',
                                      src.getModifiedItemAttr('subsystemBonusAmarrCore3'), skill='Amarr Core Systems')


class Effect6936(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web',
                                      'overloadRangeBonus', src.getModifiedItemAttr('subsystemBonusMinmatarCore3'),
                                      skill='Minmatar Core Systems')


class Effect6937(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler', 'overloadRangeBonus',
                                      src.getModifiedItemAttr('subsystemBonusGallenteCore3'), skill='Gallente Core Systems')


class Effect6938(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'ECM', 'overloadECMStrengthBonus',
                                      src.getModifiedItemAttr('subsystemBonusCaldariCore3'), skill='Caldari Core Systems')


class Effect6939(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'), 'overloadSelfDurationBonus',
                                      src.getModifiedItemAttr('subsystemBonusAmarrDefensive2'), skill='Amarr Defensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'), 'overloadHardeningBonus',
                                      src.getModifiedItemAttr('subsystemBonusAmarrDefensive2'), skill='Amarr Defensive Systems')


class Effect6940(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'), 'overloadHardeningBonus',
                                      src.getModifiedItemAttr('subsystemBonusGallenteDefensive2'), skill='Gallente Defensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'), 'overloadSelfDurationBonus',
                                      src.getModifiedItemAttr('subsystemBonusGallenteDefensive2'), skill='Gallente Defensive Systems')


class Effect6941(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Tactical Shield Manipulation'),
                                      'overloadHardeningBonus', src.getModifiedItemAttr('subsystemBonusCaldariDefensive2'),
                                      skill='Caldari Defensive Systems')


class Effect6942(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'), 'overloadSelfDurationBonus',
                                      src.getModifiedItemAttr('subsystemBonusMinmatarDefensive2'), skill='Minmatar Defensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Hull Upgrades'), 'overloadHardeningBonus',
                                      src.getModifiedItemAttr('subsystemBonusMinmatarDefensive2'), skill='Minmatar Defensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Tactical Shield Manipulation'), 'overloadHardeningBonus',
                                      src.getModifiedItemAttr('subsystemBonusMinmatarDefensive2'), skill='Minmatar Defensive Systems')


class Effect6943(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'overloadSelfDurationBonus', src.getModifiedItemAttr('subsystemBonusAmarrDefensive3'),
                                      skill='Amarr Defensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'overloadArmorDamageAmount', src.getModifiedItemAttr('subsystemBonusAmarrDefensive3'),
                                      skill='Amarr Defensive Systems')


class Effect6944(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'overloadSelfDurationBonus', src.getModifiedItemAttr('subsystemBonusGallenteDefensive3'),
                                      skill='Gallente Defensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'),
                                      'overloadArmorDamageAmount', src.getModifiedItemAttr('subsystemBonusGallenteDefensive3'),
                                      skill='Gallente Defensive Systems')


class Effect6945(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'overloadShieldBonus', src.getModifiedItemAttr('subsystemBonusCaldariDefensive3'),
                                      skill='Caldari Defensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Operation'),
                                      'overloadSelfDurationBonus', src.getModifiedItemAttr('subsystemBonusCaldariDefensive3'),
                                      skill='Caldari Defensive Systems')


class Effect6946(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems') or mod.item.requiresSkill('Shield Operation'),
                                      'overloadArmorDamageAmount', src.getModifiedItemAttr('subsystemBonusMinmatarDefensive3'),
                                      skill='Minmatar Defensive Systems')
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems') or mod.item.requiresSkill('Shield Operation'),
                                      'overloadSelfDurationBonus', src.getModifiedItemAttr('subsystemBonusMinmatarDefensive3'),
                                      skill='Minmatar Defensive Systems')


class Effect6947(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'),
                                        'baseSensorStrength', src.getModifiedItemAttr('subsystemBonusCaldariDefensive2'),
                                        skill='Caldari Defensive Systems')


class Effect6949(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'), 'baseSensorStrength',
                                        src.getModifiedItemAttr('subsystemBonusGallenteDefensive2'), skill='Gallente Defensive Systems')


class Effect6951(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'), 'baseSensorStrength',
                                        src.getModifiedItemAttr('subsystemBonusMinmatarDefensive2'), skill='Minmatar Defensive Systems')


class Effect6953(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        module.multiplyItemAttr('power', module.getModifiedItemAttr('mediumRemoteRepFittingMultiplier'))
        module.multiplyItemAttr('cpu', module.getModifiedItemAttr('mediumRemoteRepFittingMultiplier'))


class Effect6954(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Leadership'), 'power',
                                      src.getModifiedItemAttr('subsystemCommandBurstFittingReduction'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Leadership'), 'cpu',
                                      src.getModifiedItemAttr('subsystemCommandBurstFittingReduction'))


class Effect6955(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Remote Shield Booster', 'Ancillary Remote Shield Booster'),
                                      'falloffEffectiveness', src.getModifiedItemAttr('remoteShieldBoosterFalloffBonus'))


class Effect6956(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Remote Armor Repairer', 'Ancillary Remote Armor Repairer'),
                                      'maxRange', src.getModifiedItemAttr('remoteArmorRepairerOptimalBonus'))


class Effect6957(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Remote Armor Repairer', 'Ancillary Remote Armor Repairer'),
                                      'falloffEffectiveness', src.getModifiedItemAttr('remoteArmorRepairerFalloffBonus'))


class Effect6958(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'overloadSelfDurationBonus',
                                      src.getModifiedItemAttr('subsystemBonusAmarrOffensive3'), skill='Amarr Offensive Systems')


class Effect6959(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'), 'overloadSelfDurationBonus',
                                      src.getModifiedItemAttr('subsystemBonusGallenteOffensive3'), skill='Gallente Offensive Systems')


class Effect6960(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems'),
                                      'overloadSelfDurationBonus', src.getModifiedItemAttr('subsystemBonusCaldariOffensive3'),
                                      skill='Caldari Offensive Systems')


class Effect6961(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Shield Emission Systems') or mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'overloadSelfDurationBonus', src.getModifiedItemAttr('subsystemBonusMinmatarOffensive3'),
                                      skill='Minmatar Offensive Systems')


class Effect6962(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', src.getModifiedItemAttr('subsystemBonusAmarrPropulsion2'),
                               skill='Amarr Propulsion Systems')


class Effect6963(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', src.getModifiedItemAttr('subsystemBonusMinmatarPropulsion2'),
                               skill='Minmatar Propulsion Systems')


class Effect6964(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('baseWarpSpeed', module.getModifiedItemAttr('subsystemBonusGallentePropulsion'),
                               skill='Gallente Propulsion Systems')


class Effect6981(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Torpedoes'), 'thermalDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG1'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Torpedoes'), 'kineticDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG1'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Torpedoes'), 'thermalDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG1'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Torpedoes'), 'kineticDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG1'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Cruise Missiles'), 'thermalDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG1'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Cruise Missiles'), 'kineticDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG1'), skill='Gallente Titan')


class Effect6982(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Torpedoes'), 'explosiveDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG2'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Torpedoes'), 'emDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG2'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Torpedoes'), 'emDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG2'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Torpedoes'), 'explosiveDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG2'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Cruise Missiles'), 'emDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG2'), skill='Gallente Titan')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Cruise Missiles'), 'explosiveDamage',
                                      src.getModifiedItemAttr('shipBonusTitanG2'), skill='Gallente Titan')


class Effect6983(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldKineticDamageResonance', src.getModifiedItemAttr('shipBonusTitanC1'), skill='Caldari Titan')
        fit.ship.boostItemAttr('shieldEmDamageResonance', src.getModifiedItemAttr('shipBonusTitanC1'), skill='Caldari Titan')
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', src.getModifiedItemAttr('shipBonusTitanC1'), skill='Caldari Titan')
        fit.ship.boostItemAttr('shieldThermalDamageResonance', src.getModifiedItemAttr('shipBonusTitanC1'), skill='Caldari Titan')


class Effect6984(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'shieldCapacity',
                                       src.getModifiedItemAttr('shipBonusRole4'))
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'fighterAbilityAttackTurretDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusRole4'))
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'fighterAbilityAttackMissileDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusRole4'))
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill('Fighters'), 'fighterAbilityMissilesDamageMultiplier',
                                       src.getModifiedItemAttr('shipBonusRole4'))


class Effect6985(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Torpedoes'), 'kineticDamage',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtG1'), skill='Gallente Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('Torpedoes'), 'thermalDamage',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtG1'), skill='Gallente Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Torpedoes'), 'kineticDamage',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtG1'), skill='Gallente Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Torpedoes'), 'thermalDamage',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtG1'), skill='Gallente Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Cruise Missiles'), 'thermalDamage',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtG1'), skill='Gallente Dreadnought')
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill('XL Cruise Missiles'), 'kineticDamage',
                                      src.getModifiedItemAttr('shipBonusDreadnoughtG1'), skill='Gallente Dreadnought')


class Effect6986(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capital Shield Emission Systems'), 'shieldBonus',
                                      src.getModifiedItemAttr('shipBonusForceAuxiliaryG1'), skill='Gallente Carrier')


class Effect6987(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Drone Operation'),
                                        'structureDamageAmount', src.getModifiedItemAttr('shipBonusRole2'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Drone Operation'),
                                        'shieldBonus', src.getModifiedItemAttr('shipBonusRole2'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Drone Operation'),
                                        'armorDamageAmount', src.getModifiedItemAttr('shipBonusRole2'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Drone Operation'),
                                        'armorHP', src.getModifiedItemAttr('shipBonusRole2'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Drone Operation'),
                                        'shieldCapacity', src.getModifiedItemAttr('shipBonusRole2'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Drone Operation'),
                                        'hp', src.getModifiedItemAttr('shipBonusRole2'))


class Effect6992(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'), 'damageMultiplier', src.getModifiedItemAttr('shipBonusRole1'))


class Effect6993(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterMissileAOECloudPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterCapacitorCapacityPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterAOEVelocityPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterArmorRepairAmountPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterMissileVelocityPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterTurretTrackingPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterShieldCapacityPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterTurretOptimalRangePenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterShieldBoostAmountPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterTurretFalloffPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterArmorHPPenalty', src.getModifiedItemAttr('shipBonusRole2'))
        fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == 'Booster', 'boosterMaxVelocityPenalty', src.getModifiedItemAttr('shipBonusRole2'))


class Effect6994(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Hybrid Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('eliteBonusReconShip1'), skill='Recon Ships')


class Effect6995(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, module, context):
        # Set reload time to 1 second
        module.reloadTime = 1000


class Effect6996(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'), 'armorDamageAmount',
                                      src.getModifiedItemAttr('eliteBonusReconShip3'), skill='Recon Ships')


class Effect6997(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Repair Systems'), 'armorDamageAmount',
                                      src.getModifiedItemAttr('eliteBonusCovertOps4'), skill='Covert Ops')


class Effect6999(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Missile Launcher Torpedo',
                                         'cpu', ship.getModifiedItemAttr('stealthBomberLauncherCPU'))


class Effect7000(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'), 'falloff',
                                      src.getModifiedItemAttr('shipBonusGF'), skill='Gallente Frigate')


class Effect7001(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Missile Launcher Torpedo', 'speed', src.getModifiedItemAttr('shipBonusRole1'))


class Effect7002(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Bomb Deployment'), 'power', src.getModifiedItemAttr('shipBonusRole3'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Bomb Deployment'), 'cpu', src.getModifiedItemAttr('shipBonusRole3'))


class Effect7003(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Hybrid Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('eliteBonusCovertOps3'), skill='Covert Ops')


class Effect7008(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.multiplyItemAttr('shieldCapacity', src.getModifiedItemAttr('structureFullPowerStateHitpointMultiplier') or 0)
        fit.ship.multiplyItemAttr('armorHP', src.getModifiedItemAttr('structureFullPowerStateHitpointMultiplier') or 0)


class Effect7009(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.forceItemAttr('structureFullPowerStateHitpointMultiplier', src.getModifiedItemAttr('serviceModuleFullPowerStateHitpointMultiplier'))


class Effect7012(EffectDef):

    runTime = 'early'
    type = 'active'

    @staticmethod
    def handler(fit, src, context):
        for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
            for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
                bonus = '%s%sDamageResonance' % (attrPrefix, damageType)
                bonus = '%s%s' % (bonus[0].lower(), bonus[1:])
                booster = '%s%sDamageResonance' % (layer, damageType)

                src.forceItemAttr(booster, src.getModifiedItemAttr('resistanceMultiplier'))


class Effect7013(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'kineticDamage',
                                        src.getModifiedItemAttr('eliteBonusGunship1'), skill='Assault Frigates')


class Effect7014(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'thermalDamage',
                                        src.getModifiedItemAttr('eliteBonusGunship1'), skill='Assault Frigates')


class Effect7015(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'emDamage',
                                        src.getModifiedItemAttr('eliteBonusGunship1'), skill='Assault Frigates')


class Effect7016(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'explosiveDamage',
                                        src.getModifiedItemAttr('eliteBonusGunship1'), skill='Assault Frigates')


class Effect7017(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Missile Launcher Operation'), 'aoeVelocity',
                                        src.getModifiedItemAttr('eliteBonusGunship2'), stackingPenalties=True, skill='Assault Frigates')


class Effect7018(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Energy Turret'), 'speed',
                                      src.getModifiedItemAttr('shipBonusAF'), stackingPenalties=False, skill='Amarr Frigate')


class Effect7020(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Stasis Web', 'maxRange',
                                      src.getModifiedItemAttr('stasisWebRangeBonus'), stackingPenalties=False)


class Effect7021(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.boostItemAttr('maxTargetRange', module.getModifiedItemAttr('structureRigMaxTargetRangeBonus'))


class Effect7024(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'trackingSpeed',
                                     src.getModifiedItemAttr('eliteBonusGunship2'), skill='Assault Frigates')


class Effect7026(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr('maxRange', src.getModifiedChargeAttr('warpScrambleRangeBonus'))


class Effect7027(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.increaseItemAttr('capacitorCapacity', ship.getModifiedItemAttr('capacitorBonus'))


class Effect7028(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr('rechargeRate', module.getModifiedItemAttr('capacitorRechargeRateMultiplier'))


class Effect7029(EffectDef):

    runTime = 'early'
    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('hiddenArmorHPMultiplier', src.getModifiedItemAttr('armorHpBonus'), stackingPenalties=True)


class Effect7030(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Structure Guided Bomb Launcher',
                                      'speed', ship.getModifiedItemAttr('structureAoERoFRoleBonus'))
        for attr in ['duration', 'durationTargetIlluminationBurstProjector', 'durationWeaponDisruptionBurstProjector',
                     'durationECMJammerBurstProjector', 'durationSensorDampeningBurstProjector', 'capacitorNeed']:
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Structure Burst Projector',
                                          attr, ship.getModifiedItemAttr('structureAoERoFRoleBonus'))


class Effect7031(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusCBC2'), skill='Caldari Battlecruiser')


class Effect7032(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusCBC2'), skill='Caldari Battlecruiser')


class Effect7033(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'),
                                        'emDamage', src.getModifiedItemAttr('shipBonusCBC2'), skill='Caldari Battlecruiser')


class Effect7034(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusCBC2'), skill='Caldari Battlecruiser')


class Effect7035(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusCBC2'), skill='Caldari Battlecruiser')


class Effect7036(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusCBC2'), skill='Caldari Battlecruiser')


class Effect7037(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'thermalDamage', src.getModifiedItemAttr('shipBonusCBC2'), skill='Caldari Battlecruiser')


class Effect7038(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Assault Missiles'),
                                        'kineticDamage', src.getModifiedItemAttr('shipBonusCBC2'), skill='Caldari Battlecruiser')


class Effect7039(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        groups = ('Structure Anti-Subcapital Missile', 'Structure Anti-Capital Missile')
        for dmgType in ('em', 'kinetic', 'explosive', 'thermal'):
            fit.modules.filteredChargeMultiply(lambda mod: mod.item.group.name in groups,
                                               '%sDamage' % dmgType,
                                               src.getModifiedItemAttr('hiddenMissileDamageMultiplier'))


class Effect7040(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.multiplyItemAttr('armorHP', src.getModifiedItemAttr('hiddenArmorHPMultiplier') or 0)


class Effect7042(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('armorHP', src.getModifiedItemAttr('shipBonusAC'), skill='Amarr Cruiser')


class Effect7043(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('shieldCapacity', src.getModifiedItemAttr('shipBonusCC'), skill='Caldari Cruiser')


class Effect7044(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('agility', src.getModifiedItemAttr('shipBonusGC'), skill='Gallente Cruiser')


class Effect7045(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('signatureRadius', src.getModifiedItemAttr('shipBonusMC'), skill='Minmatar Cruiser')


class Effect7046(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('explosiveDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('shieldKineticDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('shieldExplosiveDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('armorThermalDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('thermalDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('shieldEmDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('armorEmDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('shieldThermalDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('kineticDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('armorKineticDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')
        fit.ship.boostItemAttr('emDamageResonance', src.getModifiedItemAttr('eliteBonusFlagCruisers1'), skill='Flag Cruisers')


class Effect7047(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Propulsion Module', 'Micro Jump Drive'),
                                      'power', src.getModifiedItemAttr('flagCruiserFittingBonusPropMods'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Propulsion Module', 'Micro Jump Drive'),
                                      'cpu', src.getModifiedItemAttr('flagCruiserFittingBonusPropMods'))

        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Target Painter', 'Scan Probe Launcher'),
                                      'cpu', src.getModifiedItemAttr('flagCruiserFittingBonusPainterProbes'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ('Target Painter', 'Scan Probe Launcher'),
                                      'power', src.getModifiedItemAttr('flagCruiserFittingBonusPainterProbes'))


class Effect7050(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive', 'gang')

    @staticmethod
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x)):
                value = beacon.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')


class Effect7051(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive', 'gang')

    @staticmethod
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x)):
                value = beacon.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')


class Effect7052(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter', 'signatureRadiusBonus',
                                      src.getModifiedItemAttr('targetPainterStrengthModifierFlagCruisers'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Target Painter', 'maxRange',
                                      src.getModifiedItemAttr('targetPainterRangeModifierFlagCruisers'))


class Effect7055(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Hybrid Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Projectile Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Energy Turret'), 'damageMultiplier',
                                      src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Heavy Missiles'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Torpedoes'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'), 'thermalDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'), 'explosiveDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'), 'kineticDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Cruise Missiles'), 'emDamage',
                                        src.getModifiedItemAttr('shipBonusRole7'))


class Effect7058(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive', 'gang')

    @staticmethod
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x)):
                value = beacon.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')


class Effect7059(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive', 'gang')

    @staticmethod
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x)):
                value = beacon.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')


class Effect7060(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive', 'gang')

    @staticmethod
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 5):
            if beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x)):
                value = beacon.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x))
                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')


class Effect7061(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive', 'gang')

    @staticmethod
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x)):
                value = beacon.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')


class Effect7062(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive', 'gang')

    @staticmethod
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x)):
                value = beacon.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')


class Effect7063(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive', 'gang')

    @staticmethod
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x)):
                value = beacon.getModifiedItemAttr('warfareBuff{}Value'.format(x))
                id = beacon.getModifiedItemAttr('warfareBuff{}ID'.format(x))

                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')


class Effect7064(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')


class Effect7071(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Precursor Weapon'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect7072(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Precursor Weapon'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect7073(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Precursor Weapon'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect7074(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Disintegrator Specialization'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect7075(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Disintegrator Specialization'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect7076(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, container, context):
        level = container.level if 'skill' in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Disintegrator Specialization'),
                                      'damageMultiplier', container.getModifiedItemAttr('damageMultiplierBonus') * level)


class Effect7077(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Precursor Weapon',
                                         'damageMultiplier', module.getModifiedItemAttr('damageMultiplier'),
                                         stackingPenalties=True)


class Effect7078(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == 'Precursor Weapon',
                                         'speed', module.getModifiedItemAttr('speedMultiplier'),
                                         stackingPenalties=True)


class Effect7079(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Precursor Weapon'),
                                      'speed', ship.getModifiedItemAttr('shipBonusPBS1'), skill='Precursor Battleship')


class Effect7080(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Large Precursor Weapon'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusPBS2'), skill='Precursor Battleship')


class Effect7085(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Precursor Weapon'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusPC1'), skill='Precursor Cruiser')


class Effect7086(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Precursor Weapon'),
                                      'trackingSpeed', ship.getModifiedItemAttr('shipBonusPC2'), skill='Precursor Cruiser')


class Effect7087(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Precursor Weapon'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusPF2'), skill='Precursor Frigate')


class Effect7088(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Precursor Weapon'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusPF1'), skill='Precursor Frigate')


class Effect7091(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Capacitor Emission Systems'), 'capacitorNeed', src.getModifiedItemAttr('shipBonusRole2'))


class Effect7092(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusRole2'))


class Effect7093(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Energy Pulse Weapons'),
                                      'capacitorNeed', ship.getModifiedItemAttr('shipBonusRole2'))


class Effect7094(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Remote Armor Repair Systems'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusRole1'))


class Effect7097(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Precursor Weapon',
                                      'damageMultiplier', skill.getModifiedItemAttr('damageMultiplierBonus') * skill.level)


class Effect7111(EffectDef):

    runTime = 'early'
    type = ('projected', 'passive')

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill('Small Precursor Weapon'),
                                         'damageMultiplier', module.getModifiedItemAttr('smallWeaponDamageMultiplier'),
                                         stackingPenalties=True)


class Effect7112(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Energy Neutralizer', 'capacitorNeed',
                                      src.getModifiedItemAttr('shipBonusRole2'))


class Effect7116(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill('Astrometrics'), 'baseSensorStrength',
                                        src.getModifiedItemAttr('eliteBonusReconShip2'), skill='Recon Ships')


class Effect7117(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.boostItemAttr('warpSpeedMultiplier', src.getModifiedItemAttr('shipRoleBonusWarpSpeed'))


class Effect7118(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Small Precursor Weapon'), 'damageMultiplierBonusPerCycle',
                                         src.getModifiedItemAttr('eliteBonusCovertOps3'), skill='Covert Ops')


class Effect7119(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('Medium Precursor Weapon'), 'damageMultiplierBonusPerCycle',
                                         src.getModifiedItemAttr('eliteBonusReconShip3'), skill='Recon Ships')


class Effect7142(EffectDef):

    type = 'active'

    @staticmethod
    def handler(fit, src, context):
        fit.ship.increaseItemAttr('warpScrambleStatus', src.getModifiedItemAttr('warpScrambleStrength'))
        fit.ship.boostItemAttr('mass', src.getModifiedItemAttr('massBonusPercentage'), stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'), 'speedFactor',
                                      src.getModifiedItemAttr('speedFactorBonus'), stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Afterburner'), 'speedBoostFactor',
                                      src.getModifiedItemAttr('speedBoostFactorBonus'))
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill('High Speed Maneuvering'), 'activationBlocked',
                                         src.getModifiedItemAttr('activationBlockedStrenght'))
        fit.ship.boostItemAttr('maxVelocity', src.getModifiedItemAttr('maxVelocityBonus'), stackingPenalties=True)


class Effect7154(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Precursor Weapon'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusPD1'),
                                      skill='Precursor Destroyer')


class Effect7155(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Precursor Weapon'),
                                      'damageMultiplier', ship.getModifiedItemAttr('shipBonusPBC1'),
                                      skill='Precursor Battlecruiser')


class Effect7156(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Precursor Weapon'),
                                      'maxRange', ship.getModifiedItemAttr('maxRangeBonus'))


class Effect7157(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Small Precursor Weapon'),
                                      'maxRange', ship.getModifiedItemAttr('shipBonusPD2'),
                                      skill='Precursor Destroyer')


class Effect7158(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorKineticDamageResonance', ship.getModifiedItemAttr('shipBonusPBC2'),
                               skill='Precursor Battlecruiser')


class Effect7159(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorThermalDamageResonance', ship.getModifiedItemAttr('shipBonusPBC2'),
                               skill='Precursor Battlecruiser')


class Effect7160(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorEmDamageResonance', ship.getModifiedItemAttr('shipBonusPBC2'),
                               skill='Precursor Battlecruiser')


class Effect7161(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.ship.boostItemAttr('armorExplosiveDamageResonance', ship.getModifiedItemAttr('shipBonusPBC2'),
                               skill='Precursor Battlecruiser')


class Effect7162(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill('Medium Precursor Weapon'),
                                      'maxRange', ship.getModifiedItemAttr('roleBonusCBC'))


class Effect7166(EffectDef):

    runTime = 'late'
    type = 'projected', 'active'

    @staticmethod
    def handler(fit, container, context, **kwargs):
        if 'projected' in context:
            repAmountBase = container.getModifiedItemAttr('armorDamageAmount')
            cycleTime = container.getModifiedItemAttr('duration') / 1000.0
            repSpoolMax = container.getModifiedItemAttr('repairMultiplierBonusMax')
            repSpoolPerCycle = container.getModifiedItemAttr('repairMultiplierBonusPerCycle')
            defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
            spoolType, spoolAmount = resolveSpoolOptions(SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False), container)
            rps = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, spoolType, spoolAmount)[0]) / cycleTime
            rpsPreSpool = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, SpoolType.SCALE, 0)[0]) / cycleTime
            rpsFullSpool = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, SpoolType.SCALE, 1)[0]) / cycleTime
            fit.extraAttributes.increase('armorRepair', rps, **kwargs)
            fit.extraAttributes.increase('armorRepairPreSpool', rpsPreSpool, **kwargs)
            fit.extraAttributes.increase('armorRepairFullSpool', rpsFullSpool, **kwargs)


class Effect7167(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Remote Capacitor Transmitter', 'maxRange', src.getModifiedItemAttr('shipBonusRole1'))


class Effect7168(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Mutadaptive Remote Armor Repairer', 'maxRange', src.getModifiedItemAttr('shipBonusRole3'))


class Effect7169(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Mutadaptive Remote Armor Repairer', 'armorDamageAmount', src.getModifiedItemAttr('shipBonusPC1'), skill='Precursor Cruiser')


class Effect7170(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Mutadaptive Remote Armor Repairer', 'capacitorNeed', src.getModifiedItemAttr('shipBonusPC2'), skill='Precursor Cruiser')


class Effect7171(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Mutadaptive Remote Armor Repairer', 'maxRange', src.getModifiedItemAttr('shipBonusPC1'), skill='Precursor Cruiser')


class Effect7172(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Mutadaptive Remote Armor Repairer', 'capacitorNeed', src.getModifiedItemAttr('eliteBonusLogistics1'), skill='Logistics Cruisers')


class Effect7173(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Mutadaptive Remote Armor Repairer', 'armorDamageAmount', src.getModifiedItemAttr('eliteBonusLogistics2'), skill='Logistics Cruisers')


class Effect7176(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'damageMultiplier',
                                     src.getModifiedItemAttr('damageMultiplierBonus'))


class Effect7177(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'hp',
                                     src.getModifiedItemAttr('hullHpBonus'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'armorHP',
                                     src.getModifiedItemAttr('armorHpBonus'))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill('Drones'), 'shieldCapacity',
                                     src.getModifiedItemAttr('shieldCapacityBonus'))


class Effect7179(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Strip Miner',
                                      'duration', module.getModifiedItemAttr('miningDurationMultiplier'))


class Effect7180(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Mining Laser',
                                      'duration', module.getModifiedItemAttr('miningDurationMultiplier'))


class Effect7183(EffectDef):

    type = 'passive'

    @staticmethod
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == 'Warp Scrambler', 'maxRange',
                                      src.getModifiedItemAttr('warpScrambleRangeBonus'), stackingPenalties=False)
