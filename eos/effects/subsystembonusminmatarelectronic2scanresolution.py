# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic2"),
                           skill="Minmatar Electronic Systems")
