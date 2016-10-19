# moduleBonusBastionModule
#
# Used by:
# Module: Bastion Module I
type = "active"
runTime = "early"


def handler(fit, src, context):
    # Resistances
    for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
        for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
            bonus = "%s%sDamageResonance" % (attrPrefix, damageType)
            bonus = "%s%s" % (bonus[0].lower(), bonus[1:])
            booster = "%s%sDamageResonance" % (layer, damageType)
            penalize = False if layer == 'hull' else True
            fit.ship.multiplyItemAttr(bonus, src.getModifiedItemAttr(booster),
                                      stackingPenalties=penalize, penaltyGroup="preMul")

    # Turrets
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret") or \
                                              mod.item.requiresSkill("Large Hybrid Turret") or \
                                              mod.item.requiresSkill("Large Projectile Turret"),
                                  "maxRange", src.getModifiedItemAttr("maxRangeBonus"),
                                  stackingPenalties=True)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret") or \
                                              mod.item.requiresSkill("Large Hybrid Turret") or \
                                              mod.item.requiresSkill("Large Projectile Turret"),
                                  "falloff", src.getModifiedItemAttr("falloffBonus"),
                                  stackingPenalties=True)

    # Missiles
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes") or \
                                                mod.charge.requiresSkill("Cruise Missiles") or \
                                                mod.charge.requiresSkill("Heavy Missiles"),
                                    "maxVelocity", src.getModifiedItemAttr("missileVelocityBonus"))

    # Tanking
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", src.getModifiedItemAttr("armorDamageAmountBonus"),
                                  stackingPenalties=True)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", src.getModifiedItemAttr("shieldBoostMultiplier"),
                                  stackingPenalties=True)

    # Speed penalty
    fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("speedFactor"))

    # @todo: test these for April 2016 release
    # Max locked targets
    fit.ship.forceItemAttr("maxLockedTargets", src.getModifiedItemAttr("maxLockedTargets"))

    # Block Hostile ewar
    fit.ship.forceItemAttr("disallowOffensiveModifiers", src.getModifiedItemAttr("disallowOffensiveModifiers"))

    # new with April 2016 release
    for scanType in ('Magnetometric', 'Ladar', 'Gravimetric', 'Radar'):
        fit.ship.boostItemAttr("scan{}Strength".format(scanType),
                               src.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
                               stackingPenalties=True)

    fit.ship.boostItemAttr("remoteRepairImpedance", src.getModifiedItemAttr("remoteRepairImpedanceBonus"))
    fit.ship.boostItemAttr("remoteAssistanceImpedance", src.getModifiedItemAttr("remoteAssistanceImpedanceBonus"))
    fit.ship.boostItemAttr("sensorDampenerResistance", src.getModifiedItemAttr("sensorDampenerResistanceBonus"))
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Micro Jump Drive Operation"),
                                     "activationBlocked", src.getModifiedItemAttr("activationBlockedStrenght"))
    fit.ship.boostItemAttr("targetPainterResistance", src.getModifiedItemAttr("targetPainterResistanceBonus"))
    fit.ship.boostItemAttr("weaponDisruptionResistance", src.getModifiedItemAttr("weaponDisruptionResistanceBonus"))
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("siegeModeWarpStatus"))

    fit.ship.forceItemAttr("disallowDocking", src.getModifiedItemAttr("disallowDocking"))
    fit.ship.forceItemAttr("disallowTethering", src.getModifiedItemAttr("disallowTethering"))
