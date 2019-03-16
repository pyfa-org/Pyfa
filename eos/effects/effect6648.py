# shipBonusTitanC3WarpStrength
#
# Used by:
# Variations of ship: Leviathan (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanC3"), skill="Caldari Titan")
