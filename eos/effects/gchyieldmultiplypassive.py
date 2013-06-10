# Used by:
# Ship: Venture
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Gas Cloud Harvesting"),
                                     "miningAmount", module.getModifiedItemAttr("miningAmountMultiplier"))