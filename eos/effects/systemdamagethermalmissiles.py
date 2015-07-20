# systemDamageThermalMissiles
#
# Used by:
# Celestials named like: Drifter Incursion (6 of 6)
# Celestials named like: Magnetar Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, beacon, context):
    fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                       "thermalDamage", beacon.getModifiedItemAttr("damageMultiplierMultiplier"),
                                       stackingPenalties=True, penaltyGroup="postMul")
