# eliteBonusReconWarpVelocity3
#
# Used by:
# Ship: Enforcer
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("eliteBonusReconShip3") * lvl, skill="Recon Ships")
