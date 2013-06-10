# Used by:
# Modules from group: Shield Amplifier (88 of 88)
# Modules from group: Shield Extender (37 of 37)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("shieldCapacity", module.getModifiedItemAttr("capacityBonus"))