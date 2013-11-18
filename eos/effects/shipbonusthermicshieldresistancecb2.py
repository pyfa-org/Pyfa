# Used by:
# Ship: Rattlesnake
# Ship: Rokh
# Ship: Scorpion Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("shipBonus2CB") * level)
