# GCHYieldMultiplyPassive
#
# Used by:
# Ship: Prospect
# Ship: Venture
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Gas Cloud Harvester",
                                     "miningAmount", module.getModifiedItemAttr("miningAmountMultiplier"))
