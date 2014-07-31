# Used by:
# Ships named like: Merlin (3 of 3)
# Variations of ship: Merlin (3 of 4)
# Ship: Cambion
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("shipBonusCF") * level)
