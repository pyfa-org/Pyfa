type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryA2"), skill="Amarr Carrier")
    fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryA2"), skill="Amarr Carrier")
    fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryA2"), skill="Amarr Carrier")
    fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryA2"), skill="Amarr Carrier")
