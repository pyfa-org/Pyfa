# overloadSelfSpeedBonus
#
# Used by:
# Modules from group: Propulsion Module (133 of 133)
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("speedFactor", module.getModifiedItemAttr("overloadSpeedFactorBonus"),
                         stackingPenalties=True)
