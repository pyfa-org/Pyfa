type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("scanRadarStrength", src.getModifiedItemAttr("subsystemBonusAmarrCore"),
                           skill="Amarr Core Systems")
