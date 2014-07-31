# Used by:
# Ships named like: Rokh (3 of 3)
# Ship: Rattlesnake
# Ship: Scorpion Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("shipBonus2CB") * level)
