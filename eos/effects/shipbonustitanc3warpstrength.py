# shipBonusTitanC3WarpStrength
#
# Used by:
# Ship: Leviathan
type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanC3"), skill="Caldari Titan")
