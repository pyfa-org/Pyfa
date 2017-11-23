# eliteBonusCoverOpsWarpVelocity1
#
# Used by:
# Ship: Pacifier
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("eliteBonusCovertOps1"), skill="Covert Ops")
