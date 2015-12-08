type = "overheat"
def handler(fit, module, context):
    for tgtAttr in (
        "aoeCloudSizeBonus",
        "explosionDelayBonus",
        "missileVelocityBonus",
        "aoeVelocityBonus"
    ):
        module.boostItemAttr(tgtAttr, module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))