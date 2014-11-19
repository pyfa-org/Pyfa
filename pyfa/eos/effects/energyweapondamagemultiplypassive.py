# energyWeaponDamageMultiplyPassive
#
# Used by:
# Modules named like: Energy Collision Accelerator (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Weapon",
                                     "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                     stackingPenalties = True)