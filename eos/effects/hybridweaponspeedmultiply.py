# hybridWeaponSpeedMultiply
#
# Used by:
# Modules from group: Magnetic Field Stabilizer (12 of 12)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                     "speed", module.getModifiedItemAttr("speedMultiplier"),
                                     stackingPenalties = True)