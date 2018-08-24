# covertOpsWarpResistance
#
# Used by:
# Ships from group: Covert Ops (5 of 8)
type = "passive"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpFactor", src.getModifiedItemAttr("eliteBonusCovertOps1"), skill="Covert Ops")
