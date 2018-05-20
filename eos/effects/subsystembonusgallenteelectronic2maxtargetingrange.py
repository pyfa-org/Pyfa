# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("subsystemBonusGallenteElectronic2"),
                           skill="Gallente Electronic Systems")
