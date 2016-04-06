type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierA2"), skill="Amarr Carrier")
    fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierA2"), skill="Amarr Carrier")
    fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierA2"), skill="Amarr Carrier")
    fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierA2"), skill="Amarr Carrier")
