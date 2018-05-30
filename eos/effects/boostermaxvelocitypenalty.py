# boosterMaxVelocityPenalty
#
# Used by:
# Implants named like: Booster (12 of 33)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Velocity"

# Attribute that this effect targets
attr = "boosterMaxVelocityPenalty"


def handler(fit, booster, context):
    fit.ship.boostItemAttr("maxVelocity", booster.getModifiedItemAttr(attr))
