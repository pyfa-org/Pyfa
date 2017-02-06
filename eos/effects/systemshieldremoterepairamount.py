# systemShieldRemoteRepairAmount
#
# Used by:
# Celestials named like: Cataclysmic Variable Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                     "shieldBonus", module.getModifiedItemAttr("shieldBonusMultiplierRemote"),
                                     stackingPenalties=True, penaltyGroup="postMul")
