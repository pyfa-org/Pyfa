# Used by:
# Module: Triage Module I
type = "active"
def handler(fit, module, context):
    # Remote armor reps
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "duration", module.getModifiedItemAttr("remoteArmorDamageDurationBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "armorDamageAmount", module.getModifiedItemAttr("remoteArmorDamageAmountBonus"))

    # Remote hull reppers
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Hull Repair Systems"),
                                  "structureDamageAmount", module.getModifiedItemAttr("remoteHullDamageAmountBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Hull Repair Systems"),
                                  "duration", module.getModifiedItemAttr("remoteHullDamageDurationBonus"))

    # Shield Transporters
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "shieldBonus", module.getModifiedItemAttr("shieldTransportAmountBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "duration", module.getModifiedItemAttr("shieldTransportDurationBonus"))

    # Energy Transfer Arrays
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Emission Systems"),
                                  "powerTransferAmount", module.getModifiedItemAttr("powerTransferAmountBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Emission Systems"),
                                  "duration", module.getModifiedItemAttr("powerTransferDurationBonus"))

    # Shield boosters
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                  "shieldBonus", module.getModifiedItemAttr("shieldBoostMultiplier"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                  "duration", module.getModifiedItemAttr("shieldBonusDurationBonus"))

    # Armor reps
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Repair Unit",
                                  "armorDamageAmount", module.getModifiedItemAttr("armorDamageAmountBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Repair Unit",
                                  "duration", module.getModifiedItemAttr("armorDamageDurationBonus"))

    # Speed bonus
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"))

    # Scan resolution multiplier
    fit.ship.multiplyItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionMultiplier"))

    # Mass multiplier
    fit.ship.multiplyItemAttr("mass", module.getModifiedItemAttr("massMultiplier"))

    # Lock range
    fit.ship.multiplyItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeMultiplier"))

    # Max locked targets
    fit.ship.increaseItemAttr("maxLockedTargets", module.getModifiedItemAttr("maxLockedTargetsBonus"))

    # Block EWAR & projected effects
    fit.ship.forceItemAttr("disallowOffensiveModifiers", module.getModifiedItemAttr("disallowOffensiveModifiers"))
    fit.ship.forceItemAttr("disallowAssistance", module.getModifiedItemAttr("disallowAssistance"))
