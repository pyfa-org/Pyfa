# shieldCapacityBonusOnline
#
# Used by:
# Modules from group: Shield Resistance Amplifier (88 of 88)
# Modules from group: Shield Extender (33 of 33)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("shieldCapacity", module.getModifiedItemAttr("capacityBonus"))