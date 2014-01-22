# Used by:
# Implant: Improved Blue Pill Booster
# Implant: Improved Exile Booster
# Implant: Standard Blue Pill Booster
# Implant: Standard Exile Booster
# Implant: Strong Blue Pill Booster
# Implant: Strong Exile Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.ship.boostItemAttr("capacitorCapacity", booster.getModifiedItemAttr("boosterCapacitorCapacityPenalty"))
