# shipShieldEmResistance1CBC2
#
# Used by:
# Variations of ship: Ferox (2 of 2)
# Ship: Drake
# Ship: Ferox Guristas Edition
# Ship: Nighthawk
# Ship: 幼龙级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battlecruiser").level
    fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2") * level)
