# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocity"))
