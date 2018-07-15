# boosterMaxVelocityPenalty
#
# Used by:
# Implants named like: Crash Booster (3 of 4)
# Items from market group: Implants & Boosters > Booster > Booster Slot 02 (9 of 13)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Velocity"

# Attribute that this effect targets
attr = "boosterMaxVelocityPenalty"


def handler(fit, booster, context):
    fit.ship.boostItemAttr("maxVelocity", booster.getModifiedItemAttr(attr))
