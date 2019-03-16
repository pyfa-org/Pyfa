# cpuMultiplierPostMulCpuOutputShip
#
# Used by:
# Modules from group: CPU Enhancer (19 of 19)
# Variations of structure module: Standup Co-Processor Array I (2 of 2)
type = "passive"


def handler(fit, module, context):
    fit.ship.multiplyItemAttr("cpuOutput", module.getModifiedItemAttr("cpuMultiplier"))
