# Used by:
# Celestials named like: Cataclysmic Variable Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                     "shieldBonus", module.getModifiedItemAttr("shieldBonusMultiplierRemote"))
