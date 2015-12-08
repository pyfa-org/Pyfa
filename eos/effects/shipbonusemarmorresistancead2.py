type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")
