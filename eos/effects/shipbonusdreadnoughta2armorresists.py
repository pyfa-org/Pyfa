type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtA2"), skill="Amarr Dreadnought")
    fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtA2"), skill="Amarr Dreadnought")
    fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtA2"), skill="Amarr Dreadnought")
    fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtA2"), skill="Amarr Dreadnought")
