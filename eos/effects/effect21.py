# shieldCapacityBonusOnline
#
# Used by:
# Modules from group: Shield Extender (36 of 36)
# Modules from group: Shield Resistance Amplifier (88 of 88)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("shieldCapacity", module.getModifiedItemAttr("capacityBonus"))
