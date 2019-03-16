# hybridWeaponDamageMultiply
#
# Used by:
# Modules from group: Magnetic Field Stabilizer (15 of 15)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                     "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                     stackingPenalties=True)
