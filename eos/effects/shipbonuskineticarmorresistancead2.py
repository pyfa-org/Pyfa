type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")
