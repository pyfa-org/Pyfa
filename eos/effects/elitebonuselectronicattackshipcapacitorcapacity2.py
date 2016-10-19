# eliteBonusElectronicAttackShipCapacitorCapacity2
#
# Used by:
# Ship: Kitsune
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("capacitorCapacity", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2"),
                           skill="Electronic Attack Ships")
