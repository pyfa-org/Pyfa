# minerCpuUsageMultiplyPercent2
#
# Used by:
# Variations of module: Mining Laser Upgrade I (5 of 5)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "cpu", module.getModifiedItemAttr("cpuPenaltyPercent"))