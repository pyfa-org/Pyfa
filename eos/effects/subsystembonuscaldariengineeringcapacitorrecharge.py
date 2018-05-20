# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("rechargeRate", module.getModifiedItemAttr("subsystemBonusCaldariCore"),
                           skill="Caldari Core Systems")
