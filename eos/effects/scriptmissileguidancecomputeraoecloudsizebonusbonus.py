# scriptMissileGuidanceComputerAOECloudSizeBonusBonus
#
# Used by:
# Charges from group: Tracking Script (2 of 2)
# Charges named like: Missile Script (4 of 4)
type = "passive"


def handler(fit, module, context):
    module.boostItemAttr("aoeCloudSizeBonus", module.getModifiedChargeAttr("aoeCloudSizeBonusBonus"))
