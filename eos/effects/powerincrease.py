# powerIncrease
#
# Used by:
# Modules from group: Auxiliary Power Core (5 of 5)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("powerOutput", module.getModifiedItemAttr("powerIncrease"))