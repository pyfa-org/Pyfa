# boosterShieldCapacityPenalty
#
# Used by:
# Implants from group: Booster (12 of 47)
type = "boosterSideEffect"


def handler(fit, booster, context):
    fit.ship.boostItemAttr("shieldCapacity", booster.getModifiedItemAttr("boosterShieldCapacityPenalty"))
