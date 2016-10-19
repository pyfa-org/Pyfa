# shipBonusCarrierC1ShieldResists
#
# Used by:
# Ship: Chimera
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusCarrierC1"),
                           skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusCarrierC1"),
                           skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusCarrierC1"),
                           skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusCarrierC1"),
                           skill="Caldari Carrier")
