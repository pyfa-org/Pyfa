# Used by:
# Celestials named like: Wolf Rayet Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                     "damageMultiplier", module.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                     stackingPenalties = True)
