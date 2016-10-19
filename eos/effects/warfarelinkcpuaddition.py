# warfareLinkCPUAddition
#
# Used by:
# Modules from group: Gang Coordinator (30 of 31)
type = "passive"


def handler(fit, module, context):
    module.increaseItemAttr("cpu", module.getModifiedItemAttr("warfareLinkCPUAdd") or 0)
