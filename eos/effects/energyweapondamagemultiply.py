# energyWeaponDamageMultiply
#
# Used by:
# Modules from group: Heat Sink (17 of 17)
# Modules named like: QA Multiship Module Players (4 of 4)
# Module: QA Damage Module
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Weapon",
                                     "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                     stackingPenalties = True)