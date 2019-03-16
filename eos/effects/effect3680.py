# freighterAgilityBonusC1
#
# Used by:
# Ship: Rhea
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusC1"), skill="Caldari Freighter")
