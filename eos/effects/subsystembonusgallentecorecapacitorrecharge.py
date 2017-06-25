type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("rechargeRate", src.getModifiedItemAttr("subsystemBonusGallenteCore"), skill="Gallente Core Systems")
