type = "passive"
def handler(fit, module, context):
    module.boostItemAttr("falloffBonus", module.getModifiedChargeAttr("falloffBonusBonus"))
