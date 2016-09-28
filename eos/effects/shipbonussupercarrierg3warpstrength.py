# shipBonusSupercarrierG3WarpStrength
#
# Used by:
# Variations of ship: Nyx (2 of 2)
type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusSupercarrierG3"), skill="Gallente Carrier")
