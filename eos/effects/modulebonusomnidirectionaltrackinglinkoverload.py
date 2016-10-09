# moduleBonusOmnidirectionalTrackingLinkOverload
#
# Used by:
# Modules from group: Drone Tracking Modules (10 of 10)
type = "overheat"
def handler(fit, module, context):
    overloadBonus = module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus")
    module.boostItemAttr("maxRangeBonus", overloadBonus)
    module.boostItemAttr("falloffBonus", overloadBonus)
    module.boostItemAttr("trackingSpeedBonus", overloadBonus)
    module.boostItemAttr("aoeCloudSizeBonus", overloadBonus)
    module.boostItemAttr("aoeVelocityBonus", overloadBonus)