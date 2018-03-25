# boosterShieldCapacityPenalty
#
# Used by:
# Implants from group: Booster (12 of 62)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Shield Capacity"

# Attribute that this effect targets
attr = "boosterShieldCapacityPenalty"


def handler(fit, booster, context):
    fit.ship.boostItemAttr("shieldCapacity", booster.getModifiedItemAttr(attr))
