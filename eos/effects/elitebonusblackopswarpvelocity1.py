type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("eliteBonusBlackOps1"), stackingPenalties=True, skill="Black Ops")
