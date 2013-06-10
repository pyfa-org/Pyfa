# Used by:
# Variations of module: Information Warfare Link - Electronic Superiority I (2 of 2)
type = "active"
def handler(fit, module, context):
    module.multiplyItemAttr("commandBonusTD", module.getModifiedItemAttr("commandBonusHidden"))
    module.multiplyItemAttr("commandBonusECM", module.getModifiedItemAttr("commandBonusHidden"))
    module.multiplyItemAttr("commandBonusRSD", module.getModifiedItemAttr("commandBonusHidden"))
    module.multiplyItemAttr("commandBonusTP", module.getModifiedItemAttr("commandBonusHidden"))
