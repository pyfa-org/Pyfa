# shipBonusSupercarrierC2ShieldResists
#
# Used by:
# Ship: Wyvern
type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierC2"), skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierC2"), skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierC2"), skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierC2"), skill="Caldari Carrier")
