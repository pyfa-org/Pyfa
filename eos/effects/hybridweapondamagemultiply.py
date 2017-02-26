# hybridWeaponDamageMultiply
#
# Used by:
# Modules from group: Magnetic Field Stabilizer (14 of 14)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                     "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                     stackingPenalties=True)
