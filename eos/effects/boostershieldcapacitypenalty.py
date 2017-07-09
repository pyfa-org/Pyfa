# boosterShieldCapacityPenalty
#
# Used by:
# Implants from group: Booster (12 of 62)
type = "boosterSideEffect"
activeByDefault = False


def handler(fit, booster, context):
    fit.ship.boostItemAttr("shieldCapacity", booster.getModifiedItemAttr("boosterShieldCapacityPenalty"))
