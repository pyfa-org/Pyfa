# eliteBonusCommandDestroyerShield1
#
# Used by:
# Ship: Bifrost
# Ship: Stork
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command Specialist"), "commandBonus", src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
