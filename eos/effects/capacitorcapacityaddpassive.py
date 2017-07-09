# capacitorCapacityAddPassive
#
# Used by:
# Items from category: Subsystem (20 of 48)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("capacitorCapacity", module.getModifiedItemAttr("capacitorCapacity") or 0)
