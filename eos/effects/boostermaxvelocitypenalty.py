# boosterMaxVelocityPenalty
#
# Used by:
# Implants from group: Booster (12 of 49)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Velocity"

# Attribute that this effect targets
attr = "boosterMaxVelocityPenalty"


def handler(fit, booster, context):
    fit.ship.boostItemAttr("maxVelocity", booster.getModifiedItemAttr(attr))
