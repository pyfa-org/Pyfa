# Used by:
# Items from category: Subsystem (80 of 80)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("mass") or 0)
