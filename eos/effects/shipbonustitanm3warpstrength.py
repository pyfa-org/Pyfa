# shipBonusTitanM3WarpStrength
#
# Used by:
# Ship: Ragnarok
# Ship: Vanquisher
type = "passive"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanM3"), skill="Minmatar Titan")
