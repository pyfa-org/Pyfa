# shipShieldExplosiveResistanceCF2
#
# Used by:
# Variations of ship: Merlin (3 of 4)
# Ship: Cambion
# Ship: Whiptail
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusCF") * level)
