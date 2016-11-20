# shipArmorExplosiveResistance1ABC1
#
# Used by:
# Variations of ship: Prophecy (2 of 2)
# Ship: Absolution
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusABC1"),
                           skill="Amarr Battlecruiser")
