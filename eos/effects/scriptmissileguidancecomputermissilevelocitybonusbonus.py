type = "passive"
def handler(fit, module, context):
    module.boostItemAttr("missileVelocityBonus", module.getModifiedChargeAttr("missileVelocityBonusBonus"))
