# Used by:
# Module: 'Smokescreen' Covert Ops Cloaking Device II
# Module: Covert Cynosural Field Generator I
# Module: Covert Ops Cloaking Device II
type = "passive"
def handler(fit, module, context):
    module.increaseItemAttr("cpu", module.getModifiedItemAttr("covertCloakCPUAdd") or 0)
