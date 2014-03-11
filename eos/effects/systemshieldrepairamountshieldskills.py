# Used by:
# Celestials named like: Cataclysmic Variable Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Capital Shield Operation"),
                                     "shieldBonus", module.getModifiedItemAttr("shieldBonusMultiplier"),
                                     stackingPenalties = True, penaltyGroup="postMul")
