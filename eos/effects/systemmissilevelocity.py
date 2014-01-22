# Used by:
# Celestials named like: Black Hole Effect Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, beacon, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", beacon.getModifiedItemAttr("missileVelocityMultiplier"))
