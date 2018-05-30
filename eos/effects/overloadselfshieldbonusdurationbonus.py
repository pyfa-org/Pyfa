# overloadSelfShieldBonusDurationBonus
#
# Used by:
# Modules from group: Ancillary Shield Booster (5 of 5)
# Modules from group: Shield Booster (93 of 93)
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus"))
    module.boostItemAttr("shieldBonus", module.getModifiedItemAttr("overloadShieldBonus"), stackingPenalties=True)
