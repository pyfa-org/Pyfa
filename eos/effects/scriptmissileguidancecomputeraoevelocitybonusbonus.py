type = "passive"
def handler(fit, module, context):
    module.boostItemAttr("aoeVelocityBonus", module.getModifiedChargeAttr("aoeVelocityBonusBonus"))
