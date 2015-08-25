runTime = "early"
type = ("projected", "offline")
def handler(fit, beacon, context):
    fit.ship.boostItemAttr("maxVelocity", beacon.getModifiedItemAttr("maxVelocityMultiplier"), stackingPenalties=True)
