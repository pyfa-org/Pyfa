# shipBonusTitanG3WarpStrength
#
# Used by:
# Variations of ship: Erebus (2 of 2)
type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanG3"), skill="Gallente Titan")
