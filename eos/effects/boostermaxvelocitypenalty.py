# boosterMaxVelocityPenalty
#
# Used by:
# Implants from group: Booster (12 of 39)
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.ship.boostItemAttr("maxVelocity", booster.getModifiedItemAttr("boosterMaxVelocityPenalty"))
