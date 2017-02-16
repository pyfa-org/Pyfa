# energyWeaponDamageMultiply
#
# Used by:
# Modules from group: Heat Sink (18 of 18)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Weapon",
                                     "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                     stackingPenalties=True)
