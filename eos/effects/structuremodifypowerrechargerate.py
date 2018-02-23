# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.multiplyItemAttr("rechargeRate", module.getModifiedItemAttr("capacitorRechargeRateMultiplier"))
