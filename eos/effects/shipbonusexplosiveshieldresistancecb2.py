# shipBonusExplosiveShieldResistanceCB2
#
# Used by:
# Ships named like: Rattlesnake (2 of 2)
# Ships named like: Rokh (3 of 3)
# Ship: Scorpion Navy Issue
# Ship: 响尾蛇级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonus2CB") * level)
