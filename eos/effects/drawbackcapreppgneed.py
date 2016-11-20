# drawbackCapRepPGNeed
#
# Used by:
# Variations of module: Capital Auxiliary Nano Pump I (2 of 2)
# Variations of module: Capital Nanobot Accelerator I (2 of 2)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                  "power", module.getModifiedItemAttr("drawback"))
