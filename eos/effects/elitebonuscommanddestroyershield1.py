# eliteBonusCommandDestroyerShield1
#
# Used by:
# Ship: Bifrost
# Ship: Stork
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Value", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Value", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Value", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Value", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
