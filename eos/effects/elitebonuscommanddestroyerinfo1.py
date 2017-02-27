# eliteBonusCommandDestroyerInfo1
#
# Used by:
# Ship: Pontifex
# Ship: Stork
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), attrs,
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
