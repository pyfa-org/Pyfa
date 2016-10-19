# shipBonusCarrierA1ArmorResists
#
# Used by:
# Ship: Archon
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusCarrierA1"),
                           skill="Amarr Carrier")
    fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusCarrierA1"),
                           skill="Amarr Carrier")
    fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusCarrierA1"),
                           skill="Amarr Carrier")
    fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusCarrierA1"),
                           skill="Amarr Carrier")
