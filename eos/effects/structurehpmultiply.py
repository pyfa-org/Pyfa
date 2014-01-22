# Used by:
# Modules from group: Nanofiber Internal Structure (14 of 14)
# Modules from group: Reinforced Bulkhead (12 of 12)
# Module: QA Multiship Module - 10 Players
# Module: QA Multiship Module - 20 Players
# Module: QA Multiship Module - 40 Players
# Module: QA Multiship Module - 5 Players
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("hp", module.getModifiedItemAttr("structureHPMultiplier"))