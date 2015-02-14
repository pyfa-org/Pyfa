# structureHPMultiply
#
# Used by:
# Modules from group: Nanofiber Internal Structure (7 of 7)
# Modules from group: Reinforced Bulkhead (8 of 8)
# Modules named like: QA Multiship Module Players (4 of 4)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("hp", module.getModifiedItemAttr("structureHPMultiplier"))