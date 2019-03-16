# cpuOutputAddCpuOutputPassive
#
# Used by:
# Subsystems from group: Offensive Systems (8 of 12)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("cpuOutput", module.getModifiedItemAttr("cpuOutput"))
