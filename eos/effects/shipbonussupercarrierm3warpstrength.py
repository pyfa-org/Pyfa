# shipBonusSupercarrierM3WarpStrength
#
# Used by:
# Ship: Hel
# Ship: Vendetta
type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusSupercarrierM3"), skill="Minmatar Carrier")
