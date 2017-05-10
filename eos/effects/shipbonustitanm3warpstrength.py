# shipBonusTitanM3WarpStrength
#
# Used by:
# Ships from group: Titan (3 of 6)
type = "passive"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanM3"), skill="Minmatar Titan")
