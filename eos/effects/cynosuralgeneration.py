# Used by:
# Modules from group: Cynosural Field (2 of 2)
type = "active"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"))
