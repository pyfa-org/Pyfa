type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusMD2"), skill="Minmatar Destroyer")
