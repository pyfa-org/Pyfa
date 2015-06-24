type = "passive"
def handler(fit, module, context):
    module.boostItemAttr("aoeCloudSizeBonus", module.getModifiedChargeAttr("aoeCloudSizeBonusBonus"))
