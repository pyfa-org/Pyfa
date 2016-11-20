# shipBonusAgilityMI2
#
# Used by:
# Ship: Wreathe
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusMI2"), skill="Minmatar Industrial")
