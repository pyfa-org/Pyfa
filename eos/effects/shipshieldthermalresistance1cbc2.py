# Used by:
# Variations of ship: Ferox (2 of 2)
# Ship: Drake
# Ship: Ferox Guristas Edition
# Ship: Nighthawk
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battlecruiser").level
    fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2") * level)
