# Used by:
# Modules from group: Fueled Shield Booster (4 of 4)
# Modules from group: Shield Booster (87 of 87)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus"))
    module.boostItemAttr("shieldBonus", module.getModifiedItemAttr("overloadShieldBonus"))
    