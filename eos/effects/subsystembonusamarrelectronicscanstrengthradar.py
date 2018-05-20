# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("scanRadarStrength", module.getModifiedItemAttr("subsystemBonusAmarrElectronic"),
                           skill="Amarr Electronic Systems")
