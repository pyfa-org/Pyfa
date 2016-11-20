# shipBonusSupercarrierC3WarpStrength
#
# Used by:
# Ship: Revenant
# Ship: Wyvern
type = "passive"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusSupercarrierC3"),
                              skill="Caldari Carrier")
