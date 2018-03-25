# shipShieldKineticResistance1CBC2
#
# Used by:
# Ship: Drake
# Ship: Nighthawk
# Ship: Vulture
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2"),
                           skill="Caldari Battlecruiser")
