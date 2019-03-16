# eliteBonusCommandDestroyerArmored1
#
# Used by:
# Ship: Magus
# Ship: Pontifex
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff2Value",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff3Value",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "buffDuration",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff4Value",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff1Value",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
