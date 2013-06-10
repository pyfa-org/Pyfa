# Used by:
# Variations of module: Ice Harvester Upgrade I (6 of 6)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                  "cpu", module.getModifiedItemAttr("cpuPenaltyPercent"))