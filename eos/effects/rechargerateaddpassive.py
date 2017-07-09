# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("rechargeRate", module.getModifiedItemAttr("rechargeRate"))
