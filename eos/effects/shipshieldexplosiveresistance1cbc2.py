# shipShieldExplosiveResistance1CBC2
#
# Used by:
# Variations of ship: Drake (3 of 3)
# Ship: Vulture
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2"),
                           skill="Caldari Battlecruiser")
