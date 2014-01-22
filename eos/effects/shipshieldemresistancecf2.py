# Used by:
# Ship: Cambion
# Ship: Harpy
# Ship: Merlin
# Ship: Worm
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("shipBonusCF") * level)
