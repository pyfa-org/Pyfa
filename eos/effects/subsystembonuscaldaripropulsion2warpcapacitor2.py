# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", module.getModifiedItemAttr("subsystemBonusCaldariPropulsion2"),
                           skill="Caldari Propulsion Systems")
