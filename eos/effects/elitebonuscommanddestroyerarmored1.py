# eliteBonusCommandDestroyerArmored1
#
# Used by:
# Ship: Magus
# Ship: Pontifex
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Warfare Specialist"), "commandBonus", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
