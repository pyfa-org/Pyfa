# cloakingTargetingDelayBonusLRSMCloakingPassive
#
# Used by:
# Modules named like: Targeting Systems Stabilizer (8 of 8)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda module: module.item.requiresSkill("Cloaking"),
                                  "cloakingTargetingDelay", module.getModifiedItemAttr("cloakingTargetingDelayBonus"))
