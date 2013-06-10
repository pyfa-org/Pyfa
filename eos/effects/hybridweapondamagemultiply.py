# Used by:
# Modules from group: Magnetic Field Stabilizer (19 of 19)
# Modules named like: QA Multiship Module Players (4 of 4)
# Module: QA Damage Module
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                      "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                      stackingPenalties = True)