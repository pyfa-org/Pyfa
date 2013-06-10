# Used by:
# Modules from group: Nanofiber Internal Structure (14 of 14)
# Modules from group: Reinforced Bulkhead (12 of 12)
# Modules named like: QA Multiship Module Players (4 of 4)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("hp", module.getModifiedItemAttr("structureHPMultiplier"))