# scriptMissileGuidanceComputerMissileVelocityBonusBonus
#
# Used by:
# Charges named like: Missile Script (4 of 4)
type = "passive"


def handler(fit, module, context):
    module.boostItemAttr("missileVelocityBonus", module.getModifiedChargeAttr("missileVelocityBonusBonus"))
