# systemSmallPrecursorTurretDamage
#
# Used by:
# Celestials named like: Wolf Rayet Effect Beacon Class (5 of 6)
runTime = "early"
type = ("projected", "passive")


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                     "damageMultiplier", module.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                     stackingPenalties=True)
