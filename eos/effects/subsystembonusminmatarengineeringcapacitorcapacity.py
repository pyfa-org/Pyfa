# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("capacitorCapacity", module.getModifiedItemAttr("subsystemBonusMinmatarCore"),
                           skill="Minmatar Core Systems")
