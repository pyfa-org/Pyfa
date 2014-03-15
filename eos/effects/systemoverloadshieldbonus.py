# Used by:
# Celestials named like: Red Giant Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: "overloadShieldBonus" in mod.itemModifiedAttributes,
                                     "overloadShieldBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))
