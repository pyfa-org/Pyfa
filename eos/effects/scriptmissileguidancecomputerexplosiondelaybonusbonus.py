# scriptMissileGuidanceComputerExplosionDelayBonusBonus
#
# Used by:
# Charges named like: Missile Script (4 of 4)
type = "passive"
def handler(fit, module, context):
    module.boostItemAttr("explosionDelayBonus", module.getModifiedChargeAttr("explosionDelayBonusBonus"))
