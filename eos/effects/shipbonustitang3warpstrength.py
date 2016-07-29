# shipBonusTitanG3WarpStrength
#
# Used by:
# Ship: Erebus
# Ship: Vanquisher
type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanG3"), skill="Gallente Titan")
