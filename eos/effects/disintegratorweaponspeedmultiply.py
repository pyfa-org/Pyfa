# disintegratorWeaponSpeedMultiply
#
# Used by:
# Modules from group: Entropic Suppressor (3 of 3)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Precursor Weapon",
                                     "speed", module.getModifiedItemAttr("speedMultiplier"),
                                     stackingPenalties=True)
