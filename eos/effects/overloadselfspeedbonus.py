# overloadSelfSpeedBonus
#
# Used by:
# Modules from group: Propulsion Module (114 of 114)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("speedFactor", module.getModifiedItemAttr("overloadSpeedFactorBonus"),
                         stackingPenalties=True)
