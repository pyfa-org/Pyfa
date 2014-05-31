# Used by:
# Ships from group: Exhumer (3 of 4)
# Variations of ship: Venture (2 of 2)
# Ship: Procurer
# Ship: Retriever
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Mining"),
                                     "miningAmount", module.getModifiedItemAttr("miningAmountMultiplier"))