# Used by:
# Modules from group: Propulsion Module (107 of 107)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("speedFactor", module.getModifiedItemAttr("overloadSpeedFactorBonus"))