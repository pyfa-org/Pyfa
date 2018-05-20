# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", module.getModifiedItemAttr("subsystemBonusGallentePropulsion2"),
                           skill="Gallente Propulsion Systems")
