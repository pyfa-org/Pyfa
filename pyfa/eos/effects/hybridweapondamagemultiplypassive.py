# hybridWeaponDamageMultiplyPassive
#
# Used by:
# Modules named like: Hybrid Collision Accelerator (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                     "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                     stackingPenalties = True)