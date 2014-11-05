# shipBonusCapCapAB
#
# Used by:
# Ships named like: Paladin (4 of 4)
# Ship: Apocalypse Imperial Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.ship.boostItemAttr("capacitorCapacity", ship.getModifiedItemAttr("shipBonusAB2") * level)
