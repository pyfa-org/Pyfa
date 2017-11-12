# shipBonusDreadnoughtC2ShieldResists
#
# Used by:
# Ship: Caiman
# Ship: Phoenix
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtC2"),
                           skill="Caldari Dreadnought")
    fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtC2"),
                           skill="Caldari Dreadnought")
    fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtC2"),
                           skill="Caldari Dreadnought")
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtC2"),
                           skill="Caldari Dreadnought")
