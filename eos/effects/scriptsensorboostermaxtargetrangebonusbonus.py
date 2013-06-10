# Used by:
# Charges from group: Sensor Booster Script (2 of 2)
# Charges from group: Sensor Dampener Script (2 of 2)
type = "passive"
def handler(fit, module, context):
    module.boostItemAttr("maxTargetRangeBonus", module.getModifiedChargeAttr("maxTargetRangeBonusBonus"))