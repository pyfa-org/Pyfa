# Used by:
# Items from category: Subsystem (80 of 80)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("hiSlots", module.getModifiedItemAttr("hiSlotModifier"))
    fit.ship.increaseItemAttr("medSlots", module.getModifiedItemAttr("medSlotModifier"))
    fit.ship.increaseItemAttr("lowSlots", module.getModifiedItemAttr("lowSlotModifier"))
