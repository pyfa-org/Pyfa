# Used by:
# Celestials named like: Red Giant Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, beacon, context):
    fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                     "scanRadarStrengthBonus", beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                     penaltyGroup="postMul")
