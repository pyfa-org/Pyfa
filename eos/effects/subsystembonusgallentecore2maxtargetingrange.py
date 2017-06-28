type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusGallenteCore2"),
                           skill="Gallente Core Systems")
