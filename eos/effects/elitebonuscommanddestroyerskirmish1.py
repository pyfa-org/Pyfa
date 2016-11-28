# eliteBonusCommandDestroyerSkirmish1
#
# Used by:
# Ship: Bifrost
# Ship: Magus
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff3Value", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "buffDuration", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff1Value", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff4Value", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff2Value", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
