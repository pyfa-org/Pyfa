type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("subsystemBonusAmarrCore3"),
                           skill="Amarr Core Systems")
