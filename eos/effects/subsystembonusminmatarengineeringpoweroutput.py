# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("powerOutput", module.getModifiedItemAttr("subsystemBonusMinmatarCore"),
                           skill="Minmatar Core Systems")
