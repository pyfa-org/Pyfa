# triageModeEffect7
#
# Used by:
# Module: Triage Module II
type = "active"
runTime = "early"
def handler(fit, module, context):
    # Remote armor reps
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "duration", module.getModifiedItemAttr("remoteArmorDamageDurationBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "armorDamageAmount", module.getModifiedItemAttr("remoteArmorDamageAmountBonus"),
                                  stackingPenalties=True)

    # Remote hull reppers
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Hull Repair Systems"),
                                  "structureDamageAmount", module.getModifiedItemAttr("remoteHullDamageAmountBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Hull Repair Systems"),
                                  "duration", module.getModifiedItemAttr("remoteHullDamageDurationBonus"))

    # Shield Transporters
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "shieldBonus", module.getModifiedItemAttr("shieldTransportAmountBonus"),
                                  stackingPenalties=True)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "duration", module.getModifiedItemAttr("shieldTransportDurationBonus"))

    # Energy Transfer Arrays
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Capacitor Emission Systems"),
                                  "powerTransferAmount", module.getModifiedItemAttr("powerTransferAmountBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Capacitor Emission Systems"),
                                  "duration", module.getModifiedItemAttr("powerTransferDurationBonus"))

    # Shield boosters
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                  "shieldBonus", module.getModifiedItemAttr("shieldBoostMultiplier"),
                                  stackingPenalties=True)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                  "duration", module.getModifiedItemAttr("shieldBonusDurationBonus"))

    # Armor reps
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                  "armorDamageAmount", module.getModifiedItemAttr("armorDamageAmountBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                  "duration", module.getModifiedItemAttr("armorDamageDurationBonus"))

    # Speed bonus
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                           stackingPenalties=True)

    # Scan resolution multiplier
    fit.ship.multiplyItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionMultiplier"),
                              stackingPenalties=True)

    # Mass multiplier
    fit.ship.multiplyItemAttr("mass", module.getModifiedItemAttr("siegeMassMultiplier"),
                              stackingPenalties=True)

    # Lock range
    fit.ship.multiplyItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeMultiplier"),
                              stackingPenalties=True)

    # Max locked targets
    fit.ship.increaseItemAttr("maxLockedTargets", module.getModifiedItemAttr("maxLockedTargetsBonus"))

    # Block EWAR & projected effects
    fit.ship.forceItemAttr("disallowOffensiveModifiers", module.getModifiedItemAttr("disallowOffensiveModifiers"))
    fit.ship.forceItemAttr("disallowAssistance", module.getModifiedItemAttr("disallowAssistance"))

    # RR cap consumption
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "capacitorNeed", module.getModifiedItemAttr("triageRemoteModuleCapNeed"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Hull Repair Systems"),
                                  "capacitorNeed", module.getModifiedItemAttr("triageRemoteModuleCapNeed"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "capacitorNeed", module.getModifiedItemAttr("triageRemoteModuleCapNeed"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Capacitor Emission Systems"),
                                  "capacitorNeed", module.getModifiedItemAttr("triageRemoteModuleCapNeed"))

    # EW cap need increase
    groups = [
        'ECM Burst',
        'Burst Projectors',
        'Weapon Disruptor',
        'ECM',
        'Stasis Grappler',
        'Remote Sensor Damper',
        'Target Painter']

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups or
                                              mod.item.requiresSkill("Propulsion Jamming"),
                                  "capacitorNeed", module.getModifiedItemAttr("ewCapacitorNeedBonus"))
