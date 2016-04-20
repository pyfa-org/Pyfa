# Used by:
# Variations of module: Siege Module I (2 of 2)
type = "active"
runTime = "early"
def handler(fit, src, context):
    #Turrets
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret") or \
                                  mod.item.requiresSkill("Capital Hybrid Turret") or \
                                  mod.item.requiresSkill("Capital Projectile Turret"),
                                  "damageMultiplier", src.getModifiedItemAttr("siegeTurretDamageBonus"))

    #Missiles
    for type in ("kinetic", "thermal", "explosive", "em"):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes") or \
                                        mod.charge.requiresSkill("XL Cruise Missiles") or \
                                        mod.charge.requiresSkill("Torpedoes"),
                                        "%sDamage" % type, src.getModifiedItemAttr("siegeMissileDamageBonus"))

    # Reppers
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation") or \
                                  mod.item.requiresSkill("Capital Repair Systems"),
                                  "duration", src.getModifiedItemAttr("siegeLocalLogisticsDurationBonus"))

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                  "shieldBonus", src.getModifiedItemAttr("siegeLocalLogisticsAmountBonus"),
                                  stackingPenalties=True)

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                  "armorDamageAmount", src.getModifiedItemAttr("siegeLocalLogisticsAmountBonus"),
                                  stackingPenalties=True)

    #Speed penalty
    fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("speedFactor"))

    #Mass
    fit.ship.multiplyItemAttr("mass", src.getModifiedItemAttr("siegeMassMultiplier"),
                              stackingPenalties=True, penaltyGroup="postMul")

    # @ todo: test for April 2016 release
    #Block Hostile EWAR and friendly effects
    fit.ship.forceItemAttr("disallowOffensiveModifiers", src.getModifiedItemAttr("disallowOffensiveModifiers"))
    fit.ship.forceItemAttr("disallowAssistance", src.getModifiedItemAttr("disallowAssistance"))

    # new in April 2016 release
    for scanType in ('Magnetometric', 'Ladar', 'Gravimetric', 'Radar'):
        fit.ship.boostItemAttr("scan{}Strength".format(scanType),
                               src.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
                               stackingPenalties=True)

    # missile ROF bonus
    for group in ("Missile Launcher XL Torpedo", "Missile Launcher Rapid Torpedo", "Missile Launcher XL Cruise"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == group, "speed", src.getModifiedItemAttr("siegeLauncherROFBonus"), stackingPenalties=True)

    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "maxVelocity", src.getModifiedItemAttr("siegeTorpedoVelocityBonus"), stackingPenalties=True)

    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("siegeModeWarpStatus"))
    fit.ship.boostItemAttr("remoteRepairImpedance", src.getModifiedItemAttr("remoteRepairImpedanceBonus"))
    fit.ship.boostItemAttr("sensorDampenerResistance", src.getModifiedItemAttr("sensorDampenerResistanceBonus"))
    fit.ship.boostItemAttr("remoteAssistanceImpedance", src.getModifiedItemAttr("remoteAssistanceImpedanceBonus"))
    fit.ship.boostItemAttr("weaponDisruptionResistance", src.getModifiedItemAttr("weaponDisruptionResistanceBonus"))

    fit.ship.forceItemAttr("disallowDocking", src.getModifiedItemAttr("disallowDocking"))
    fit.ship.forceItemAttr("disallowTethering", src.getModifiedItemAttr("disallowTethering"))
