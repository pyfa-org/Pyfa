# shipBonusTitanC1ShieldResists
#
# Used by:
# Ship: Komodo
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
    fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
    fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
