# overloadSelfTrackingModuleBonus
#
# Used by:
# Modules from group: Drone Tracking Modules (8 of 8)
# Modules from group: Remote Tracking Computer (10 of 10)
# Modules from group: Tracking Computer (14 of 14)
# Variations of module: Tracking Disruptor I (6 of 6)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("maxRangeBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
    module.boostItemAttr("falloffBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
    module.boostItemAttr("trackingSpeedBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
