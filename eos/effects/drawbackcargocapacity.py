type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("capacity", module.getModifiedItemAttr("drawback"))
