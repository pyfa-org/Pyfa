type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("warpSpeedMultiplier", module.getModifiedItemAttr("warpSpeedAdd"))
