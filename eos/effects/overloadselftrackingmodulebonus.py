# overloadSelfTrackingModuleBonus
#
# Used by:
# Modules named like: Tracking Computer (19 of 19)
# Variations of module: Tracking Disruptor I (6 of 6)
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("maxRangeBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
    module.boostItemAttr("falloffBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
    module.boostItemAttr("trackingSpeedBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
