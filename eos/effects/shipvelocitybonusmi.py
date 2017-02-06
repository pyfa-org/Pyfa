# shipVelocityBonusMI
#
# Used by:
# Variations of ship: Mammoth (2 of 2)
# Ship: Hoarder
# Ship: Prowler
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusMI"), skill="Minmatar Industrial")
