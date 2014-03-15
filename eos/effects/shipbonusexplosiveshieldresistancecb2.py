# Used by:
# Ships named like: Rokh (2 of 2)
# Ship: Rattlesnake
# Ship: Scorpion Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonus2CB") * level)
