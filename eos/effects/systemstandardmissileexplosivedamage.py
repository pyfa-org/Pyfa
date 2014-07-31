# Used by:
# Celestials named like: Wolf Rayet Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, beacon, context):
    fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                       "explosiveDamage", beacon.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                       stackingPenalties = True)
