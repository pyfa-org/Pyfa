# shipBonusTitanA3WarpStrength
#
# Used by:
# Variations of ship: Avatar (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanA3"), skill="Amarr Titan")
