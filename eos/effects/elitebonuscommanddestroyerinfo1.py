# eliteBonusCommandDestroyerInfo1
#
# Used by:
# Ship: Pontifex
# Ship: Stork
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff1Value",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff3Value",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff2Value",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "buffDuration",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff4Value",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
