# eliteBonusCommandDestroyerSkirmish1
#
# Used by:
# Ship: Bifrost
# Ship: Magus
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Warfare Specialist"), "commandBonus", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
