# Used by:
# Charge: Focused Warp Disruption Script
type = "passive"
def handler(fit, module, context):
    module.forceItemAttr("disallowInEmpireSpace", module.getModifiedChargeAttr("disallowInEmpireSpace"))
