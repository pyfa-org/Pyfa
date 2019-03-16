# CovertCloakCPUAddition
#
# Used by:
# Modules named like: Covert Ops Cloaking Device II (2 of 2)
# Module: Covert Cynosural Field Generator I
type = "passive"


def handler(fit, module, context):
    module.increaseItemAttr("cpu", module.getModifiedItemAttr("covertCloakCPUAdd") or 0)
