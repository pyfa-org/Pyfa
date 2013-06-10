# Used by:
# Variations of ship: Ferox (3 of 3)
# Ship: Drake
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battlecruiser").level
    fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2") * level)
