# freighterAgilityBonusA1
#
# Used by:
# Ship: Ark
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusA1"), skill="Amarr Freighter")
