# systemMaxVelocityPercentage
#
# Used by:
# Celestials named like: Drifter Incursion (6 of 6)
runTime = "early"
type = ("projected", "passive")
def handler(fit, beacon, context):
    fit.ship.boostItemAttr("maxVelocity", beacon.getModifiedItemAttr("maxVelocityMultiplier"), stackingPenalties=True)
