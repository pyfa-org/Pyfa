type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("shipRoleBonusWarpSpeed"))
