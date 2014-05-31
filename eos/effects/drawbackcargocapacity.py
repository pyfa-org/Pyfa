# Used by:
# Modules named like: Transverse Bulkhead (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("capacity", module.getModifiedItemAttr("drawback"))
