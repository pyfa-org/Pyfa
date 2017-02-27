# eliteBonusCommandDestroyerSkirmish1
#
# Used by:
# Ship: Bifrost
# Ship: Magus
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), attrs,
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
