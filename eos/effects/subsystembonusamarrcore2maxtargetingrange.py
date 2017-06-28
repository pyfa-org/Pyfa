type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusAmarrCore2"),
                           skill="Amarr Core Systems")
