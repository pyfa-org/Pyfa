# shipBonusAgilityCI2
#
# Used by:
# Ship: Badger
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusCI2"), skill="Caldari Industrial")
