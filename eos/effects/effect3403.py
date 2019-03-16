# eliteBonusBlackOpsCloakVelocity2
#
# Used by:
# Ships from group: Black Ops (5 of 5)
type = "passive"


def handler(fit, ship, context):
    if fit.extraAttributes["cloaked"]:
        fit.ship.multiplyItemAttr("maxVelocity", ship.getModifiedItemAttr("eliteBonusBlackOps2"), skill="Black Ops")
