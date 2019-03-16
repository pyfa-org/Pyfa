# moduleBonusTriageModule
#
# Used by:
# Variations of module: Triage Module I (2 of 2)
type = "active"
runTime = "early"


def handler(fit, src, context):
    # Remote effect bonuses (duration / amount / range / fallout)
    for skill, amtAttr, stack in (
            ("Capital Remote Armor Repair Systems", "armorDamageAmount", True),
            ("Capital Shield Emission Systems", "shieldBonus", True),
            ("Capital Capacitor Emission Systems", "powerTransferAmount", False),
            ("Capital Remote Hull Repair Systems", "structureDamageAmount", False)):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "duration",
                                      src.getModifiedItemAttr("siegeRemoteLogisticsDurationBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), amtAttr,
                                      src.getModifiedItemAttr("siegeRemoteLogisticsAmountBonus"),
                                      stackingPenalties=stack)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "maxRange",
                                      src.getModifiedItemAttr("siegeRemoteLogisticsRangeBonus"), stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "falloffEffectiveness",
                                      src.getModifiedItemAttr("siegeRemoteLogisticsRangeBonus"), stackingPenalties=True)

    # Local armor/shield rep effects (duration / amoutn)
    for skill, amtAttr in (
            ("Capital Shield Operation", "shieldBonus"),
            ("Capital Repair Systems", "armorDamageAmount")):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "duration",
                                      src.getModifiedItemAttr("siegeLocalLogisticsDurationBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), amtAttr,
                                      src.getModifiedItemAttr("siegeLocalLogisticsAmountBonus"))

    # Speed bonus
    fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("speedFactor"), stackingPenalties=True)

    # Scan resolution multiplier
    fit.ship.multiplyItemAttr("scanResolution", src.getModifiedItemAttr("scanResolutionMultiplier"),
                              stackingPenalties=True)

    # Mass multiplier
    fit.ship.multiplyItemAttr("mass", src.getModifiedItemAttr("siegeMassMultiplier"), stackingPenalties=True)

    # Max locked targets
    fit.ship.increaseItemAttr("maxLockedTargets", src.getModifiedItemAttr("maxLockedTargetsBonus"))

    # EW cap need increase
    groups = [
        'Burst Jammer',
        'Weapon Disruptor',
        'ECM',
        'Stasis Grappler',
        'Sensor Dampener',
        'Target Painter']

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups or
                                              mod.item.requiresSkill("Propulsion Jamming"),
                                  "capacitorNeed", src.getModifiedItemAttr("ewCapacitorNeedBonus"))

    # todo: test for April 2016 release
    # Block EWAR & projected effects
    fit.ship.forceItemAttr("disallowOffensiveModifiers", src.getModifiedItemAttr("disallowOffensiveModifiers"))
    fit.ship.forceItemAttr("disallowAssistance", src.getModifiedItemAttr("disallowAssistance"))

    # new in April 2016 release
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                 src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)

    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("siegeModeWarpStatus"))
    fit.ship.boostItemAttr("sensorDampenerResistance", src.getModifiedItemAttr("sensorDampenerResistanceBonus"))
    fit.ship.boostItemAttr("remoteAssistanceImpedance", src.getModifiedItemAttr("remoteAssistanceImpedanceBonus"))
    fit.ship.boostItemAttr("remoteRepairImpedance", src.getModifiedItemAttr("remoteRepairImpedanceBonus"))

    fit.ship.forceItemAttr("disallowTethering", src.getModifiedItemAttr("disallowTethering"))
    fit.ship.forceItemAttr("disallowDocking", src.getModifiedItemAttr("disallowDocking"))
