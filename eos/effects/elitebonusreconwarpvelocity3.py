# eliteBonusReconWarpVelocity3
#
# Used by:
# Ship: Enforcer
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")
