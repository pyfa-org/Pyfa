# GCHYieldMultiplyPassive
#
# Used by:
# Variations of ship: Venture (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Gas Cloud Harvester",
                                     "miningAmount", module.getModifiedItemAttr("miningAmountMultiplier"))
