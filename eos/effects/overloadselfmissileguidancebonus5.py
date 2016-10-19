# overloadSelfMissileGuidanceBonus5
#
# Used by:
# Modules from group: Missile Guidance Computer (3 of 3)
type = "overheat"


def handler(fit, module, context):
    for tgtAttr in (
            "aoeCloudSizeBonus",
            "explosionDelayBonus",
            "missileVelocityBonus",
            "maxVelocityBonus",
            "aoeVelocityBonus"
    ):
        module.boostItemAttr(tgtAttr, module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
