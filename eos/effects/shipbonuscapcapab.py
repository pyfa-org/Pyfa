# Used by:
# Ship: Apocalypse Imperial Issue
# Ship: Paladin
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.ship.boostItemAttr("capacitorCapacity", ship.getModifiedItemAttr("shipBonusAB2") * level)
