# Used by:
# Modules from group: Auxiliary Power Core (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("powerOutput", module.getModifiedItemAttr("powerIncrease"))