# systemArmorRepairAmount
#
# Used by:
# Celestials named like: Cataclysmic Variable Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Repair Systems") or
                                                 mod.item.requiresSkill("Capital Repair Systems"),
                                     "armorDamageAmount", module.getModifiedItemAttr("armorDamageAmountMultiplier"),
                                     stackingPenalties=True, penaltyGroup="postMul")
