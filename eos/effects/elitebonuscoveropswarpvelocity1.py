type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("eliteBonusCoverOps1") * lvl, skill="Covert Ops")
