# iceHarvestCycleTimeModulesRequiringIceHarvestingOnline
#
# Used by:
# Variations of module: Ice Harvester Upgrade I (5 of 5)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                  "duration", module.getModifiedItemAttr("iceHarvestCycleBonus"))