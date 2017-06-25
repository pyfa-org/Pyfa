# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("subsystemBonusAmarrElectronic2"),
                           skill="Amarr Electronic Systems")
