# boosterCapacitorCapacityPenalty
#
# Used by:
# Implants named like: Blue Pill Booster (3 of 5)
# Implants named like: Exile Booster (3 of 4)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Cap Capacity"

# Attribute that this effect targets
attr = "boosterCapacitorCapacityPenalty"


def handler(fit, booster, context):
    fit.ship.boostItemAttr("capacitorCapacity", booster.getModifiedItemAttr(attr))
