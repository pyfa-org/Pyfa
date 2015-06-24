type = "passive"
def handler(fit, module, context):
    module.boostItemAttr("explosionDelayBonus", module.getModifiedChargeAttr("explosionDelayBonusBonus"))
