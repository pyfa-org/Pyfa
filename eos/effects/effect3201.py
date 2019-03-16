# overloadSelfShieldBonusDurationBonus
#
# Used by:
# Modules from group: Ancillary Shield Booster (8 of 8)
# Modules from group: Shield Booster (97 of 97)
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus"))
    module.boostItemAttr("shieldBonus", module.getModifiedItemAttr("overloadShieldBonus"), stackingPenalties=True)
