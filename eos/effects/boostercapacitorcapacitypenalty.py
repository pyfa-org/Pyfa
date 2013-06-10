# Used by:
# Implants named like: Blue Pill Booster (3 of 5)
# Implants named like: Exile Booster (3 of 4)
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.ship.boostItemAttr("capacitorCapacity", booster.getModifiedItemAttr("boosterCapacitorCapacityPenalty"))
