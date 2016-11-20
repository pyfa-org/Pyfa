# warfareLinkCPUAddition
#
# Used by:
# Modules from group: Command Burst (10 of 10)
# Modules from group: Gang Coordinator (6 of 6)
type = "passive"


def handler(fit, module, context):
    module.increaseItemAttr("cpu", module.getModifiedItemAttr("warfareLinkCPUAdd") or 0)
