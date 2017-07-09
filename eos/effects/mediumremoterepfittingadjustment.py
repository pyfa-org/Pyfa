# mediumRemoteRepFittingAdjustment
#
# Used by:
# Variations of module: Medium Remote Armor Repairer I (12 of 12)
# Variations of module: Medium Remote Shield Booster I (11 of 11)
# Module: Medium Ancillary Remote Armor Repairer
# Module: Medium Ancillary Remote Shield Booster
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("power", module.getModifiedItemAttr("mediumRemoteRepFittingMultiplier"))
    module.multiplyItemAttr("cpu", module.getModifiedItemAttr("mediumRemoteRepFittingMultiplier"))
