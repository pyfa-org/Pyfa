# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("cpuOutput", module.getModifiedItemAttr("subsystemBonusGallenteElectronic"),
                           skill="Gallente Electronic Systems")
