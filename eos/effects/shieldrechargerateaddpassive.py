# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("shieldRechargeRate", module.getModifiedItemAttr("shieldRechargeRate") or 0)
