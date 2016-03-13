# miningYieldMultiplyPassive
#
# Used by:
# Variations of ship: Procurer (2 of 2)
# Variations of ship: Retriever (2 of 2)
# Variations of ship: Venture (3 of 3)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Mining"),
                                     "miningAmount", module.getModifiedItemAttr("miningAmountMultiplier"))