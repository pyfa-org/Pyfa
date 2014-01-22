# Used by:
# Variations of module: Large Auxiliary Nano Pump I (2 of 2)
# Variations of module: Large Nanobot Accelerator I (2 of 2)
# Variations of module: Medium Auxiliary Nano Pump I (2 of 2)
# Variations of module: Medium Nanobot Accelerator I (2 of 2)
# Variations of module: Small Auxiliary Nano Pump I (2 of 2)
# Variations of module: Small Nanobot Accelerator I (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "power", module.getModifiedItemAttr("drawback"))