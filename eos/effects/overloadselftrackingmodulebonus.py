# Used by:
# Modules from group: Drone Tracking Modules (7 of 7)
# Modules from group: Remote Tracking Computer (10 of 10)
# Modules from group: Tracking Computer (14 of 14)
# Modules from group: Tracking Disruptor (10 of 10)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("maxRangeBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
    module.boostItemAttr("falloffBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
    module.boostItemAttr("trackingSpeedBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
