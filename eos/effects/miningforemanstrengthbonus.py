# miningForemanStrengthBonus
#
# Used by:
# Skill: Mining Director
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
