# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("mass") or 0)
