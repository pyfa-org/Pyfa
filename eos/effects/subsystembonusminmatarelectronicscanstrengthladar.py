# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("scanLadarStrength", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic"),
                           skill="Minmatar Electronic Systems")
