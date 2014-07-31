# Used by:
# Charges from group: Tracking Disruption Script (2 of 2)
# Charges from group: Tracking Script (2 of 2)
type = "passive"
def handler(fit, module, context):
    module.boostItemAttr("trackingSpeedBonus", module.getModifiedChargeAttr("trackingSpeedBonusBonus"))
