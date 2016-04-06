# shipBonusTitanG3WarpStrength
#
# Used by:
# Ship: Erebus
type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanG3"), skill="Gallente Titan")
