# shipBonusForceAuxiliaryC2ShieldResists
#
# Used by:
# Ship: Loggerhead
# Ship: Minokawa
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                           skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                           skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                           skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                           skill="Caldari Carrier")
